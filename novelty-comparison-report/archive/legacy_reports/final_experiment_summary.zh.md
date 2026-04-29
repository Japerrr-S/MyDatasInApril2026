# AI-Scientist Novelty 实验总总结

更新日期：2026-04-29

## 1. 实验目标

本项目围绕一个核心问题展开：

```text
AI-Scientist 的 idea novelty 判断是否可能因为 query 不充分、检索失败或检索源受限，而错误地把 idea 视为 novel？
```

为了回答这个问题，我们搭建了两个实验平台：

- `diffusion-novelty-platform`
  - 研究领域：diffusion model。
  - 这是 AI/ML 内部的近域迁移，和原 AI-Scientist 的研究语境较接近。
- `energy-novelty-platform`
  - 研究领域：能源电力系统。
  - 这是更明显的跨领域迁移，用来观察 AI-Scientist 在非纯 ML 领域里的 query 和 novelty 行为。

两个平台都尽量复用原 AI-Scientist / AI-Scientist-v2 的 idea generation 和 literature search 逻辑。平台本身主要增加了运行封装、领域 prompt、query/event 记录、query audit、备用检索源和结果归档。

## 2. 实验设计

实验比较两个版本：

- AI-Scientist v1
  - 先生成 idea。
  - 再进入相对独立的 `check_idea_novelty` 阶段。
  - LLM 生成 query，Semantic Scholar 返回论文，LLM 再做 `novel / not novel` 判断。
- AI-Scientist-v2
  - 没有与 v1 等价的独立 novelty gate。
  - 它在 ideation 过程中调用 `SearchSemanticScholar`。
  - 文献结果作为下一轮 proposal reflection 的上下文。
  - 最后通过 `FinalizeIdea` 输出 proposal。

因此，本项目中对 v2 的 `novel=True` 一律解释为：

```text
provisional novel
```

而不是：

```text
已经通过独立文献检索证明 novel
```

相关机制说明见：

- `reports/v2_empty_literature_behavior.zh.md`
- `reports/v2_ideation_and_novelty_mechanism.zh.md`
- `reports/prompt_comparison_ai_scientist_platform.zh.md`

## 3. 数据批次总览

当前报告仓库包含以下主要数据批次。

### 3.1 `data/`

第一批 smoke run，用于验证平台能否跑通、日志是否能记录 query 和 novelty event。

这批结果主要作为历史参考，不是当前最推荐分析的主结果。

### 3.2 `data_20260428/`

这是当前最重要的一批主结果。

配置要点：

- 使用 AutoDL.Art OpenAI-compatible API。
- 模型为 `gpt-5.4`。
- 未配置 `S2_API_KEY`。
- v1/v2 分开运行。
- 每个平台为 smoke 配置，小样本运行。

这批数据包含：

- diffusion v1/v2 结果；
- energy v1/v2 结果；
- query audit；
- comparison JSON/Markdown/中文 Markdown。

### 3.3 `data_20260428_s2paced/`

这一批用于测试 Semantic Scholar 429 限流问题。

新增设置：

- `S2_REQUEST_INTERVAL=12`
- `S2_429_COOLDOWN=60`
- 保留原仓库 backoff/retry 方式

结果显示，即使增加请求间隔和 429 冷却，匿名访问仍然可能持续 429。

### 3.4 `data_backup_search_20260428/`

这一批是备用检索源对照实验。

它不重新生成 idea，也不改变原 v1/v2 输出，而是复用 `data_20260428` 中已经记录下来的 query，再额外查询：

- OpenAlex
- arXiv

目的在于判断：

```text
Semantic Scholar 没有返回论文，是否真的意味着没有相关文献？
```

实验结果显示，答案是否定的。特别是 diffusion v2，Semantic Scholar 因 429 没有返回标题，但 arXiv 能返回多个相关候选文献。

### 3.5 `data_posthoc_novelty_20260428/`

这一批是事后独立 novelty decision。

它把 Semantic Scholar、OpenAlex、arXiv 的证据放到一起，对 v2 的 provisional novel 结果做平台层复核。

结果：

- `diversity_adaptive_guidance`
  - 原 v2：`novel=True (provisional)`
  - 事后判断：`novelty_not_established`
  - 建议：`needs_human_review_before_accepting_novelty`
- `conformal_opf_reserve_activation`
  - 原 v2：`novel=True (provisional)`
  - 事后判断：`novelty_not_established`
  - 建议：`needs_human_review_before_accepting_novelty`

注意：这并不是证明它们一定不 novel，而是说明现有证据不足以接受 strong novelty claim。

### 3.6 `data_semantic_scholar_probe_20260429/`

这是 2026-04-29 对 Semantic Scholar 匿名访问状态的再次探测。

diffusion v2 的结果显示：

- 不是全部 429；
- 3 条 query 中有 1 条成功返回 3 篇文献标题；
- 同一轮中仍有 query 最终 429；
- 返回标题包括 `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking`。

这说明 Semantic Scholar 匿名访问有局部恢复，但仍不稳定，不适合直接支撑大规模完整 run。

energy v2 同日也做过临时探测，但 3 条 query 全部 429，没有拿到文献，因此按照实验约定没有归档进报告仓库。

## 4. Diffusion 平台结果总结

### 4.1 v1 结果

`data_20260428/diffusion/v1` 中，v1 得到：

- `learning_rate_schedule`: `novel=False`
- `cluster_conditioned_diffusion`: `novel=True`

query audit 显示：

- `learning_rate_schedule`
  - queries=1
  - retrieved_titles=10
- `cluster_conditioned_diffusion`
  - queries=2
  - retrieved_titles=20

解释：

- v1 在这轮 diffusion 实验里成功检索到了文献。
- `cluster_conditioned_diffusion` 虽被判定为 novel，但这不等于“没有任何相关工作”。
- 更合理的解释是：LLM 根据返回论文和 idea 描述判断其核心组合或研究 framing 仍有增量。
- 后续人工阅读应重点检查是否已有 cluster-conditioned、pseudo-label conditional diffusion 或 self-supervised conditional diffusion 的近似工作。

### 4.2 v2 结果

`data_20260428/diffusion/v2` 中，v2 生成：

- `diversity_adaptive_guidance`
- 平台记录：`is_novel=True`
- 解释：`provisional`

但对应 query event 显示：

- queries=3
- retrieved_titles=0
- 三条 Semantic Scholar query 均因 429 或检索失败没有返回有效论文

这正是本项目最关键的观察之一：

```text
在没有检索到任何文献的情况下，AI-Scientist-v2 仍然可以 finalize idea，并被平台记录为 provisional novel。
```

备用检索进一步显示，同样的 query 在 arXiv 中可以找到 classifier-free guidance、oversaturation、self-attention guidance 等相关候选文献。因此，Semantic Scholar 空返回不能被解释成“没有相关文献”。

### 4.3 2026-04-29 diffusion v2 探测

`data_semantic_scholar_probe_20260429/diffusion/v2` 中，Semantic Scholar 不是全部 429。

query audit 显示：

- queries=3
- retrieved_titles=3

返回标题包括：

- `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking`
- `Fast and faithful: accelerating data-free knowledge distillation via confidence-aware adaptive diffusion`
- `Navigating with Annealing Guidance Scale in Diffusion Space`

解释：

- 这说明匿名访问偶尔可用。
- 但同一轮仍有 query 最终 429。
- 因此当前网络条件仍不足以支撑稳定大规模完整 run。

## 5. Energy 平台结果总结

### 5.1 v1 结果

`data_20260428/energy/v1` 中，v1 得到：

- `forecast_aware_storage_dispatch`: `novel=False`
- `adaptive_peak_shaving_dispatch`: `novel=False`

query audit 中一个关键现象是：

- `adaptive_peak_shaving_dispatch`
  - queries=1
  - retrieved_titles=1
  - `energy_terms=none`

这里的 `energy_terms=none` 不是说 query 一定不属于能源领域，而是说当前 audit 词表没有匹配到预定义能源电力术语。它暴露了两个问题：

- audit 词表需要扩展；
- v1 在跨领域迁移时，query 的领域覆盖可能偏窄。

### 5.2 v2 结果

`data_20260428/energy/v2` 中，v2 生成：

- `conformal_opf_reserve_activation`
- 平台记录：`is_novel=True`
- 解释：`provisional`

query audit 显示：

- queries=3
- retrieved_titles=4
- 匹配到多个能源电力术语：
  - demand response
  - electricity market
  - frequency regulation
  - n-1 security
  - optimal power flow
  - renewable integration

解释：

- v2 在 energy 平台中生成的 query 更接近 power systems 语境。
- 这说明领域 prompt 对 v2 有明显影响。
- 但 retrieved_titles 仍然较少，且 novelty 没有经过独立 gate，因此只能视为 provisional。

### 5.3 2026-04-29 energy v2 探测

同日临时试跑 energy v2 时：

- 3 条 query 全部 429；
- 没有返回任何文献；
- 因此没有归档进报告仓库。

这说明 energy 平台对 Semantic Scholar 可用性更敏感。其 query 通常较长、领域术语较多，匿名访问下更容易遇到不稳定返回。

## 6. 关于 retrieved_titles 的解释

`retrieved_titles` 指检索接口实际返回的论文标题。

它的含义是：

```text
LLM 生成 query
  -> 平台调用 Semantic Scholar / 备用检索源
  -> 检索源返回论文列表
  -> 平台抽取 title 字段
  -> 形成 retrieved_titles
```

它可以帮助判断：

- query 是否真的搜到东西；
- 搜到的文献是否属于正确领域；
- novelty 判断是否建立在足够证据上；
- 是否存在“query 太偏导致没有搜到关键论文”的问题；
- 是否存在“API 失败导致文献为空”的问题。

因此，本实验不只看最终 `novel=True/False`，而是同时看 query、retrieved_titles 和 error。

## 7. 关于 LLM novelty 判断的解释

AI-Scientist 的 novelty 判断并不是简单规则：

```text
有相关文献 -> 不 novel
没有相关文献 -> novel
```

更接近：

```text
idea 描述 + query 检索结果 + LLM 对差异性的推理
  -> 判断核心贡献是否已被已有工作充分覆盖
```

因此，一个 idea 有相关文献并不必然不新颖。学术 novelty 通常不是“没有任何相关研究”，而是：

- 是否提出了新的问题 framing；
- 是否组合了已有组件但形成新的研究对象；
- 是否已有工作只覆盖邻近概念，没有覆盖核心 claim；
- 是否实验设定、应用场景、方法机制有实质增量。

但这也说明 LLM 判断依赖两个前提：

- 检索证据要足够；
- LLM 要正确理解 retrieved titles / abstracts 与 idea 的关系。

如果 query 错误、检索失败或文献为空，LLM 的 novelty 判断就会显著变弱。

## 8. v2 空文献仍可 finalize 的关键发现

原 AI-Scientist-v2 没有把以下情况作为硬错误：

- 没有找到任何论文；
- Semantic Scholar query 全部失败；
- 所有检索都返回 429；
- retrieved_titles 为空；
- related work evidence 不足。

代码结构上，`SearchSemanticScholar` 的结果只是进入后续 LLM 上下文。`FinalizeIdea` 分支只检查是否提供了合法 idea JSON，不检查检索是否成功。

因此，v2 可能出现：

```text
没有有效文献证据
  -> LLM 仍然 finalize proposal
  -> 平台记录为 is_novel=True
```

本项目将这种情况解释为：

```text
novel=True (provisional)
```

并进一步通过 post-hoc gate 将其降级为：

```text
novelty_not_established
needs_human_review_before_accepting_novelty
```

## 9. Semantic Scholar 429 的影响

Semantic Scholar 429 不是单纯的运行故障，而是 novelty pipeline 的系统性风险。

原因是：

- novelty 判断依赖检索证据；
- 匿名访问可能长期 429；
- v2 在检索失败时仍可能 finalize idea；
- 单一检索源为空不能证明没有相关文献。

2026-04-28 的节流实验显示：

- 12 秒请求间隔；
- 60 秒 429 cooldown；
- 原仓库 backoff；

仍不足以稳定解除匿名访问限制。

2026-04-29 的 probe 显示匿名访问有局部恢复，但仍不稳定。因此当前条件下，最可靠的数据形态仍是：

- smoke run；
- query/event audit；
- backup search；
- post-hoc novelty review；
- 人工重点复核。

## 10. 主要结论

### 结论 1：不能只看 `novel=True/False`

`novel=True` 必须结合 query、retrieved_titles、error 和检索源状态解释。

尤其是 v2，如果检索失败或 retrieved_titles 为空，`novel=True` 只能视为 provisional。

### 结论 2：v1 与 v2 的 novelty 语义不同

v1 更像一个独立 novelty gate。

v2 更像：

```text
literature-informed ideation
```

它能生成更完整的 proposal，但其 novelty 声明不是独立审稿式判定。

### 结论 3：备用检索源证明“空返回不等于无相关文献”

diffusion v2 是最清晰的样本：

- Semantic Scholar 返回 0；
- arXiv 能返回多个相关候选；
- 因此不能把 Semantic Scholar 失败解释为 idea novel。

### 结论 4：跨领域迁移需要更多 than prompt

Energy 平台显示，prompt 能显著影响 v2 的 query 术语和 proposal framing。

但仅靠 prompt 不足以保证可靠 novelty check。还需要：

- 领域 query rewrite；
- 更完整的 power systems 术语表；
- 领域检索源；
- 多源 evidence aggregation；
- finalize 后独立 novelty gate。

### 结论 5：query audit 是必要模块

没有 `novelty_events.jsonl` 和 `query_audit.json`，就无法区分：

- 真的没有相关研究；
- query 没搜到相关研究；
- Semantic Scholar API 失败；
- LLM 在证据不足时仍然自信输出 proposal。

## 11. 当前局限

当前实验仍有明显限制：

- 主要是 smoke run，样本量小；
- 未配置 Semantic Scholar API key；
- Semantic Scholar 429 对结果影响显著；
- v2 原生没有独立 novelty gate；
- Energy audit 词表仍需扩展；
- 多数比较仍停留在标题、摘要和 query 层面；
- 尚未进行专家级全文判读。

因此，当前结果应被视为机制审计和风险定位，而不是统计意义上的最终性能评估。

## 12. 后续建议

建议后续按以下方向推进：

1. 配置 `S2_API_KEY` 后复跑同一配置。
2. 给 v2 增加 finalize 后独立 novelty gate。
3. 对 `retrieved_titles` 做 relevance filtering，而不是只统计标题数量。
4. 对每个 idea 生成多组 query，包括：
   - broad query
   - exact mechanism query
   - negative-control query
   - domain-specific query
5. 引入多源检索：
   - Semantic Scholar
   - OpenAlex
   - arXiv
   - 能源领域可进一步考虑 IEEE / power systems 专门数据库。
6. 构建 oracle non-novel benchmark，用已知重复 idea 检测 false novel。
7. 对 `cluster_conditioned_diffusion`、`diversity_adaptive_guidance`、`conformal_opf_reserve_activation` 做人工文献复核。

## 13. 最终总结

本项目的实验结果支持以下判断：

```text
AI-Scientist 的 novelty 输出不能脱离 query 和检索证据单独解释。
```

v1 在检索成功时更接近可审计的 novelty gate。v2 能生成更完整、更像研究 proposal 的 idea，但其 literature search 嵌入 ideation 流程，缺少独立 evidence-gated novelty decision。

最关键的风险是：

```text
当检索失败、query 不充分或 retrieved_titles 为空时，系统仍可能产出看似 novel 的 proposal。
```

因此，若要把 AI-Scientist 用作科研 idea novelty 的可靠辅助工具，必须补充：

- query audit；
- 多源检索；
- 检索失败状态；
- evidence sufficiency 判断；
- finalize 后独立 novelty gate；
- 人工复核流程。

在当前实验条件下，最稳妥的结论不是“AI-Scientist 无法判断 novelty”，而是：

```text
AI-Scientist 可以生成有价值的候选 idea 和初步 related-work reasoning，
但 novelty claim 必须经过独立、多源、可审计的证据链校验。
```
