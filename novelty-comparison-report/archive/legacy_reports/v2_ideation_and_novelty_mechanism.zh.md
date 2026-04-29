# 番外：AI-Scientist-v2 如何做 Ideation 与 Novelty

本文档解释一个容易误会的点：

```text
AI-Scientist-v2 并不是像 v1 那样先生成 idea，再执行一个独立 check_novelty。
```

更准确地说，v2 是把文献搜索嵌入 idea generation / ideation 过程中。它通过工具调用让模型一边搜索、一边反思、一边完善 proposal，最后调用 `FinalizeIdea`。因此，v2 的 novelty 更像是“proposal 生成过程中的自我声明和文献启发”，而不是一个独立 novelty gate 的结论。

## 1. 一句话对比 v1 与 v2

v1 的结构更接近：

```text
generate idea
  -> check_idea_novelty
  -> LLM 多轮生成 query
  -> Semantic Scholar 返回论文
  -> LLM 明确决定 novel / not novel
```

v2 的结构更接近：

```text
generate proposal
  -> 在 ideation 过程中可调用 SearchSemanticScholar
  -> 把检索结果放回下一轮反思
  -> LLM 调用 FinalizeIdea
```

所以 v2 没有和 v1 完全对应的：

```text
check_novelty(idea) -> true/false
```

这也是本项目把 v2 的 `novel=True` 标为 `provisional` 的原因。

## 2. v1 的独立 novelty check 代码证据

文件：

```text
AI-Scientist/ai_scientist/generate_ideas.py
```

v1 明确有 `check_idea_novelty` 函数。本地代码中可以看到：

```python
def check_idea_novelty(
        ideas,
        base_dir,
        client,
        model,
        max_num_iterations=10,
        engine="semanticscholar",
):
```

它对每个 idea 单独循环：

```python
for idx, idea in enumerate(ideas):
    if "novel" in idea:
        print(f"Skipping idea {idx}, already checked.")
        continue

    print(f"\nChecking novelty of idea {idx}: {idea['Name']}")
```

并且在 novelty prompt 中明确要求模型做决定：

```python
if "decision made: novel" in text.lower():
    print("Decision made: novel after round", j)
    novel = True
    break
if "decision made: not novel" in text.lower():
    print("Decision made: not novel after round", j)
    break
```

这说明 v1 的 novelty check 是一个显式阶段。它的输出会写回：

```python
idea["novel"] = novel
```

因此，v1 的 `novel=True/False` 更接近独立 novelty gate 的结果。

## 3. v2 的 ideation 入口：工具式 proposal generation

文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
```

v2 首先定义了两个核心工具/动作：

```python
tools = [
    semantic_scholar_tool,
    {
        "name": "FinalizeIdea",
        "description": """Finalize your idea by providing the idea details.
        ...
        """,
    },
]
```

这里很关键：`SearchSemanticScholar` 和 `FinalizeIdea` 在同一个 action 框架下。也就是说，搜索文献不是独立 novelty checker，而是 ideation agent 可以选择的一个工具。

## 4. v2 system prompt：要求 proposal novel，但这是软约束

同一文件中，v2 的 `system_prompt` 要求模型生成高影响力、novel 的 proposal：

```python
system_prompt = f"""You are an experienced AI researcher who aims to propose high-impact research ideas resembling exciting grant proposals. Feel free to propose any novel ideas or experiments; make sure they are novel.
...
Clearly clarify how the proposal distinguishes from the existing literature.
...
Note: You should perform at least one literature search before finalizing your idea to ensure it is well-informed by existing research."""
```

这段 prompt 说明 v2 确实“希望”模型检索文献，并在 related work 中区分已有工作。

但它是 prompt 约束，不是程序约束。代码没有在 finalize 前强制检查：

- 是否至少成功检索一次；
- 是否至少返回一篇论文；
- 是否所有 query 都失败；
- 是否有足够 related work evidence。

所以这里的 novelty 要求是 soft instruction，不是 hard gate。

## 5. v2 的初始 prompt 来自 workshop description

v2 的 `idea_generation_prompt` 是：

```python
idea_generation_prompt = """{workshop_description}

Here are the proposals that you have already generated:

'''
{prev_ideas_string}
'''

Begin by generating an interestingly new high-level research proposal that differs from what you have previously proposed.
"""
```

这说明 v2 的研究方向主要由：

```text
workshop_description
```

决定。

在本项目中：

- diffusion platform 给 v2 输入 `diffusion_models.md`；
- energy platform 给 v2 输入 `energy_power_systems.md`。

因此，platform 对 v2 的主要 prompt 适配点就是 workshop markdown。

## 6. v2 的反思 prompt 会接收工具结果

v2 后续轮次使用 `idea_reflection_prompt`：

```python
idea_reflection_prompt = """Round {current_round}/{num_reflections}.

In your thoughts, first carefully consider the quality, novelty, and feasibility of the proposal you just created.
...
If you have new information from tools, such as literature search results, incorporate them into your reflection and refine your proposal accordingly.

Results from your last action (if any):

{last_tool_results}
"""
```

这说明文献搜索结果会进入下一轮 LLM 上下文。v2 的机制是：

```text
search result -> last_tool_results -> reflection prompt -> refine proposal
```

而不是：

```text
search result -> independent novelty classifier -> true/false
```

这也是 v2 与 v1 的根本区别。

## 7. v2 主循环：每轮让 LLM 选择一个 ACTION

在 `generate_temp_free_idea` 中，v2 对每轮 response 解析 action：

```python
action_pattern = r"ACTION:\s*(.*?)\s*ARGUMENTS:"
arguments_pattern = r"ARGUMENTS:\s*(.*?)(?:$|\nTHOUGHT:|\n$)"
...
action = action_match.group(1).strip()
arguments_text = arguments_match.group(1).strip()
```

然后根据 action 执行不同分支：

```python
if action in tools_dict:
    ...
elif action == "FinalizeIdea":
    ...
```

这说明 v2 每轮不是固定执行“检索 -> 判断”，而是让 LLM 自己选择：

- 搜索文献；
- 或 finalize idea；
- 或在下一轮根据工具结果继续调整。

## 8. SearchSemanticScholar 分支：结果只是进入 last_tool_results

如果 action 是工具，例如 `SearchSemanticScholar`，代码会执行：

```python
result = tool.use_tool(**arguments_json)
last_tool_results = result
```

如果工具异常，例如 429，代码会捕获异常并写入：

```python
last_tool_results = f"Error using tool {action}: {str(e)}"
```

注意这里没有：

```python
novelty_status = "unknown"
```

也没有：

```python
cannot_finalize = True
```

所以工具结果只是下一轮 prompt 的上下文。它不自动变成 final novelty decision。

## 9. Semantic Scholar 工具：空结果不是 hard error

文件：

```text
AI-Scientist-v2/ai_scientist/tools/semantic_scholar.py
```

`use_tool` 的核心逻辑是：

```python
papers = self.search_for_papers(query)
...
if papers:
    return self.format_papers(papers)
else:
    return "No papers found."
```

这说明如果搜索成功但没有论文，工具返回的是：

```text
No papers found.
```

而不是抛出异常。

`search_for_papers` 里也有对应逻辑：

```python
total = results.get("total", 0)
if total == 0:
    return None
```

所以在 v2 中：

```text
没有返回论文
```

会变成：

```text
No papers found.
```

进入下一轮 LLM 反思，而不会阻止 finalize。

## 10. FinalizeIdea 分支：不检查文献证据是否充分

当 action 是 `FinalizeIdea` 时，代码执行：

```python
arguments_json = json.loads(arguments_text)
idea = arguments_json.get("idea")
if not idea:
    raise ValueError("Missing 'idea' in arguments.")

idea_str_archive.append(json.dumps(idea))
print(f"Proposal finalized: {idea}")
idea_finalized = True
break
```

这个分支只检查：

```text
有没有合法 idea JSON
```

它没有检查：

- 是否成功执行过 `SearchSemanticScholar`；
- `last_tool_results` 是否包含论文；
- 是否所有检索都 429；
- 是否有最少 N 篇相关文献；
- 是否有明确 not-overlap 证据。

因此，只要 LLM 输出合法的 `FinalizeIdea`，v2 就会接受 proposal。

## 11. v2 的 novelty 到底在哪里？

v2 的 novelty 主要体现在三个位置：

### 11.1 Prompt 层

system prompt 要求：

```text
make sure they are novel
Clearly clarify how the proposal distinguishes from the existing literature
```

### 11.2 Tool 层

模型可以调用：

```text
SearchSemanticScholar
```

并在下一轮反思中使用检索结果。

### 11.3 Proposal 字段层

`FinalizeIdea` 要求输出：

```text
Related Work
Risk Factors and Limitations
```

这让 v2 生成的 idea 看起来更像完整 proposal。

但这三层都不等于独立 novelty checker。它们共同形成的是：

```text
literature-informed ideation
```

而不是：

```text
evidence-gated novelty decision
```

## 12. 为什么容易误以为 v2 和 v1 一样？

因为 v2 也会：

- 调用 Semantic Scholar；
- 写 Related Work；
- 让模型说明和 existing literature 的区别；
- 输出一个看起来很完整的 proposal。

这些行为很像 novelty check。

但从代码结构看，差异在于：

```text
v1: novelty check 是独立函数和独立阶段。
v2: literature search 是 ideation action 的一部分。
```

所以 v2 的检索更像“写 proposal 前查资料”，而不是“写完 idea 后做严格审稿式 novelty 判定”。

## 13. 对本项目实验结果的解释

在本项目中，v2 生成了：

- `diversity_adaptive_guidance`
- `conformal_opf_reserve_activation`

原 platform 适配层记录为：

```text
novel=True (provisional)
```

这里的 `provisional` 很重要。它表示：

```text
v2 ideation 流程 finalize 了一个 proposal。
```

而不是：

```text
v2 独立 novelty checker 已经证明该 idea novel。
```

后来我们加入备用检索和 post-hoc novelty decision 后，两个 v2 idea 都被降级为：

```text
novelty_not_established
needs_human_review_before_accepting_novelty
```

这正是因为 v2 原机制没有把备用源、失败检索、空文献结果纳入一个严格 final gate。

## 14. 可以怎样改进 v2？

如果希望 v2 和 v1 更公平比较，可以在 `FinalizeIdea` 之后加一层独立 gate：

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

这样才不会把：

```text
检索失败
```

误解释为：

```text
没有相关文献，因此 novel
```

## 15. 小结

AI-Scientist-v2 的 ideation 和 novelty 是一体化的：

```text
它在生成 proposal 的过程中搜索文献；
但没有在生成后执行独立 novelty check。
```

这与 v1 不同。v1 更像：

```text
idea -> check_novelty -> decision
```

v2 更像：

```text
workshop prompt -> tool-using ideation -> FinalizeIdea
```

因此，本项目中对 v2 的正确解释是：

```text
v2 能生成 literature-informed proposal，
但其 novelty=True 只能视为 provisional，
需要额外 post-hoc 或独立多源 novelty gate 才能作为强结论。
```
