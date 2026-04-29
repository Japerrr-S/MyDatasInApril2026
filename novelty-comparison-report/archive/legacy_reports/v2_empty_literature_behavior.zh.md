# AI-Scientist-v2 对空文献结果的处理说明

本文档单独说明一个关键现象：

```text
AI-Scientist-v2 在 Semantic Scholar 一直没有返回有效论文，或检索失败时，仍可能 finalize idea。
```

结论先行：

```text
原 AI-Scientist-v2 没有把“未找到任何相关文献”或“所有检索失败”作为硬错误处理。
它没有强制要求至少成功检索到 N 篇论文，才允许 FinalizeIdea。
```

这就是为什么在本实验中，v2 的结果只能标记为 `novel=True (provisional)`，而不能等价于 v1 的独立 novelty decision。

## 1. v2 的结构不是独立 novelty gate

AI-Scientist-v2 的 ideation 流程更像：

```text
生成 proposal
  -> 可选调用 SearchSemanticScholar
  -> 根据工具结果继续反思
  -> 调用 FinalizeIdea
```

而不是：

```text
生成 idea
  -> 强制检索
  -> 检索证据足够
  -> novelty=true/false
```

这一区别非常重要。v2 的 literature search 是 proposal generation 过程中的工具调用，不是一个单独的 novelty checker。

## 2. 原仓库代码证据一：空结果返回 `No papers found.`

文件：

```text
AI-Scientist-v2/ai_scientist/tools/semantic_scholar.py
```

关键位置：

- `SemanticScholarSearchTool.use_tool`
- 本地行号约为 102-112

相关逻辑：

```python
def use_tool(self, query: str) -> Optional[str]:
    try:
        papers = self.search_for_papers(query)
    except Exception as exc:
        log_novelty_event(query, [], error=str(exc))
        raise
    log_novelty_event(query, papers)
    if papers:
        return self.format_papers(papers)
    else:
        return "No papers found."
```

含义：

- 如果 `search_for_papers` 正常执行，但返回空或 `None`，工具不会抛出异常。
- 它只是把结果转换成字符串 `"No papers found."`。
- 这个字符串会被送回 LLM 上下文，供下一轮反思使用。
- 但这不是 hard failure。

也就是说，v2 没有在这里写：

```python
raise RuntimeError("No papers found; novelty is unknown")
```

也没有写：

```python
return SearchStatus.UNKNOWN
```

## 3. 原仓库代码证据二：Semantic Scholar `total == 0` 返回 `None`

同一文件：

```text
AI-Scientist-v2/ai_scientist/tools/semantic_scholar.py
```

关键位置：

- `SemanticScholarSearchTool.search_for_papers`
- 本地行号约为 120-146

相关逻辑：

```python
results = rsp.json()
total = results.get("total", 0)
if total == 0:
    return None

papers = results.get("data", [])
papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
return papers
```

含义：

- Semantic Scholar 正常返回但 `total == 0` 时，函数返回 `None`。
- 上层 `use_tool` 会把 `None` 解释成 `"No papers found."`。
- 这仍然不是异常，也不会阻止后续 finalize。

所以在 v2 中：

```text
没有论文返回
```

会被表示为：

```text
No papers found.
```

而不是：

```text
novelty cannot be determined
```

## 4. 原仓库代码证据三：检索异常只写入 `last_tool_results`

文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
```

关键位置：

- tool action 执行逻辑
- 本地行号约为 215-230

相关逻辑：

```python
if action in tools_dict:
    tool = tools_dict[action]
    arguments_json = json.loads(arguments_text)

    try:
        result = tool.use_tool(**arguments_json)
        last_tool_results = result
    except Exception as e:
        last_tool_results = f"Error using tool {action}: {str(e)}"
```

含义：

- 如果 `SearchSemanticScholar` 因 429 或网络问题失败，异常会被捕获。
- 捕获后只是把错误文本写入 `last_tool_results`。
- 代码没有设置一个全局失败状态，例如：

```python
search_failed = True
```

- 也没有禁止后续 `FinalizeIdea`。

因此，检索失败会变成下一轮 LLM 能看到的一段文本：

```text
Error using tool SearchSemanticScholar: ...
```

但它不会自动终止 ideation，也不会自动把 novelty 标成 unknown。

## 5. 原仓库代码证据四：FinalizeIdea 分支不检查检索是否成功

同一文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
```

关键位置：

- `FinalizeIdea` action 处理逻辑
- 本地行号约为 231-243

相关逻辑：

```python
elif action == "FinalizeIdea":
    arguments_json = json.loads(arguments_text)
    idea = arguments_json.get("idea")
    if not idea:
        raise ValueError("No idea provided in FinalizeIdea arguments.")

    idea_str_archive.append(json.dumps(idea))
    print(f"Proposal finalized: {idea}")
    idea_finalized = True
    break
```

含义：

- `FinalizeIdea` 只检查 JSON 里有没有 `idea`。
- 它不检查：
  - 是否至少调用过一次 Semantic Scholar；
  - 是否至少一次检索成功；
  - 是否返回过至少一篇论文；
  - 是否全部 query 都失败；
  - 是否 query audit 为空；
  - 是否 evidence 足够支持 novelty。

缺失的逻辑大概是这种：

```python
if successful_search_count == 0:
    raise RuntimeError("Cannot finalize idea without successful literature search.")
```

但原 v2 没有这样的 gate。

## 6. Prompt 只是软约束，不是程序约束

v2 的 system prompt 中确实有提醒。

文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
```

关键位置：

- 本地行号约为 94-96

相关文本：

```text
Note: You should perform at least one literature search before finalizing your idea to ensure it is well-informed by existing research.
```

这句话的作用是 prompt-level instruction。

但它不是程序级约束：

- 没有变量记录“是否成功检索”；
- 没有检查返回论文数量；
- 没有在 finalize 前校验；
- 没有失败时抛出不可判定状态。

所以这条 prompt 可以让模型倾向于先 search，但不能保证：

```text
search 成功
```

也不能保证：

```text
search 失败时不 finalize
```

## 7. 本实验中的对应现象

在本项目的 `data_20260428/diffusion/v2` 中，v2 记录到 3 条 query：

```text
queries = 3
retrieved_titles = 0
```

对应文件：

```text
novelty-comparison-report/data_20260428/diffusion/v2/query_audit.json
novelty-comparison-report/data_20260428/diffusion/v2/novelty_events.jsonl
```

Semantic Scholar 结果为空主要是 429。

但 v2 仍 finalize 了：

```text
diversity_adaptive_guidance
```

并在 platform 适配层被记录为：

```text
novel=True (provisional)
```

备用检索实验进一步显示，同样的 query 在 arXiv 中可以找到相关候选文献，例如：

- `Classifier-Free Diffusion Guidance`
- `Rethinking Oversaturation in Classifier-Free Guidance via Low Frequency`
- `Improving Sample Quality of Diffusion Models Using Self-Attention Guidance`

这说明 Semantic Scholar 空返回不等价于没有相关文献。

## 8. 为什么这不是简单 bug，而是机制问题

这不是某一行代码写错，而是 v2 机制设计上的选择：

- search 是 tool；
- tool result 是 LLM 上下文；
- finalization 由 LLM action 触发；
- 程序只检查 action 格式，不检查证据充分性。

因此，只要 LLM 最终输出：

```text
ACTION:
FinalizeIdea
```

并提供合法 idea JSON，程序就会接受。

## 9. 对 novelty 解释的影响

因此，v2 的 `novel=True` 不能解释为：

```text
已经通过充分文献检索证明 novel
```

更准确的解释是：

```text
v2 ideation 流程 finalize 了一个自认为有 novelty 的 proposal。
```

在检索失败或文献为空时，它应该被标成：

```text
provisional novel
```

甚至在更严格系统中应标成：

```text
novelty_unknown_due_to_insufficient_evidence
```

## 10. 建议的修复方向

如果要让 v2 的 novelty 更可靠，可以增加一个 finalize 前 gate：

```python
if successful_search_count == 0:
    status = "novelty_unknown_due_to_search_failure"
    do_not_finalize_as_novel()
```

也可以增加更细的状态：

```text
search_successful = true/false
num_returned_papers = N
num_failed_queries = M
novelty_status = novel / not_novel / unknown
```

更完整的改法是：

```text
FinalizeIdea
  -> independent multi-source novelty check
  -> query audit
  -> novelty decision with evidence status
```

这样才能把：

- 没有相关论文；
- query 不好；
- 检索失败；
- 检索源限流；

这四种情况区分开。

## 11. 小结

原 AI-Scientist-v2 没有针对“文献列表一直为空”或“所有检索失败”设置硬性失败条件。代码证据显示：

- 空结果被转换为 `"No papers found."`；
- 检索异常被写入 `last_tool_results`；
- `FinalizeIdea` 不检查是否成功检索到论文；
- prompt 中“至少检索一次”的要求只是软约束。

因此，在 Semantic Scholar 429 或检索为空时，v2 仍可能 finalize idea。这正是本平台将 v2 结果标记为 `provisional`，并额外记录 query event / backup search 的原因。
