# 04 v2 机制与空文献风险

## v2 如何调用 Semantic Scholar

AI-Scientist-v2 的关键文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
AI-Scientist-v2/ai_scientist/tools/semantic_scholar.py
```

`perform_ideation_temp_free.py` 中先创建工具：

```python
semantic_scholar_tool = SemanticScholarSearchTool()

tools = [
    semantic_scholar_tool,
    {"name": "FinalizeIdea", ...},
]
```

然后 system prompt 要求 LLM 输出：

```text
ACTION:
SearchSemanticScholar
```

或：

```text
ACTION:
FinalizeIdea
```

程序解析 LLM 的 action：

```python
if action in tools_dict:
    tool = tools_dict[action]
    result = tool.use_tool(**arguments_json)
    last_tool_results = result
elif action == "FinalizeIdea":
    idea = arguments_json.get("idea")
    idea_str_archive.append(json.dumps(idea))
```

因此，是否继续 search 还是 finalize，主要由 LLM 输出的 `ACTION` 决定。

## 搜索结果如何进入下一轮

当 LLM 调用 `SearchSemanticScholar` 后，工具返回的文献结果会写入：

```python
last_tool_results
```

下一轮 prompt 包含：

```text
If you have new information from tools, such as literature search results,
incorporate them into your reflection and refine your proposal accordingly.

Results from your last action:
{last_tool_results}
```

所以 v2 是：

```text
检索结果 -> 下一轮 ideation reflection 上下文
```

而不是：

```text
检索结果 -> 独立 novelty classifier -> true/false
```

## v2 是否有 novel 布尔标签

原 v2 finalized idea 不包含原生 `novel: true/false`。

`FinalizeIdea` 要求输出：

- `Name`
- `Title`
- `Short Hypothesis`
- `Related Work`
- `Abstract`
- `Experiments`
- `Risk Factors and Limitations`

本项目中的 `is_novel=true` 是平台适配层为了统一 v1/v2 结果而添加的 provisional 标记。

它的含义是：

```text
v2 在要求生成 novel proposal 的 prompt 下 finalize 了这个 proposal。
```

不是：

```text
v2 执行了独立 novelty checker 并判定 novel。
```

## 文献为空时会怎样

`SemanticScholarSearchTool.use_tool()` 的逻辑是：

```python
papers = self.search_for_papers(query)
if papers:
    return self.format_papers(papers)
else:
    return "No papers found."
```

如果检索正常返回但没有论文，工具返回 `"No papers found."`，不会自动抛出“novelty unknown”。

如果发生 429 或网络错误，本项目记录到 `novelty_events.jsonl`。原流程中错误也主要变成 LLM 可见的工具错误文本，不会自动阻止所有后续 finalize。

## 关键风险

v2 原流程没有强制检查：

- 是否至少成功检索一次；
- 是否至少返回 N 篇论文；
- 是否所有 query 都失败；
- 是否有足够 evidence；
- 文献为空时是否必须输出 unknown；
- 是否禁止 `FinalizeIdea`。

因此可能出现：

```text
检索失败 / 文献为空
  -> LLM 仍然 finalize proposal
  -> 平台记录为 provisional novel
```

`data_20260428/diffusion/v2` 就出现了这种情况。

## 与 v1 的区别

v1 也可能误判 novelty，但 v1 至少有一个独立 novelty check loop：

```text
idea -> query -> papers with abstracts -> LLM decision -> idea["novel"]
```

v2 则是：

```text
workshop prompt -> tool-using ideation -> FinalizeIdea
```

所以两者都依赖 LLM，但风险形态不同。

## 建议修复

如果要改进 v2，建议在 `FinalizeIdea` 后增加独立 gate：

```text
FinalizeIdea
  -> extract core claims
  -> multi-query literature search
  -> Semantic Scholar + OpenAlex + arXiv
  -> relevance filtering
  -> novelty = novel / not_novel / unknown
```

并明确区分：

- `novel`
- `not_novel`
- `unknown_due_to_search_failure`
- `unknown_due_to_insufficient_evidence`

尤其要加入硬规则：

```python
if successful_search_count == 0:
    novelty_status = "unknown_due_to_search_failure"
```
