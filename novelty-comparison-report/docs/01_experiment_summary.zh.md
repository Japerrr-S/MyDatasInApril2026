# 01 实验总览

## 研究问题

本项目审计 AI-Scientist v1/v2 的 idea generation 与 novelty / literature search 流程，核心问题是：

```text
当 query 不充分、检索源受限或文献返回为空时，AI-Scientist 是否仍可能把 idea 视为 novel？
```

我们搭建了两个平台：

- `diffusion-novelty-platform`：近域任务，仍属于 AI/ML。
- `energy-novelty-platform`：跨领域任务，面向能源电力系统。

两个平台尽量复用原 AI-Scientist / AI-Scientist-v2 的主要逻辑。平台新增的是运行封装、领域配置、query event 记录、query audit、备用检索源和结果归档。

## 关键发现

### 1. v1 和 v2 的 novelty 语义不同

v1 有相对独立的 novelty check：

```text
idea -> check_idea_novelty -> query -> papers -> LLM decision -> novel true/false
```

v2 不是这个结构。v2 的文献搜索嵌入 ideation：

```text
workshop prompt -> LLM action loop -> SearchSemanticScholar 或 FinalizeIdea
```

因此 v2 的 finalized proposal 不能等价为“通过独立 novelty checker 的 novel idea”。

### 2. v2 原仓库没有原生 novelty 布尔标签

原 AI-Scientist-v2 的 `FinalizeIdea` 输出字段包括：

- `Name`
- `Title`
- `Short Hypothesis`
- `Related Work`
- `Abstract`
- `Experiments`
- `Risk Factors and Limitations`

它不包含原生 `novel: true/false`。本项目中的 `is_novel=true` 是平台为了统一 v1/v2 比较而加入的 provisional 标记。

### 3. 检索失败时 v2 仍可能 finalize

在 `data_20260428/diffusion/v2` 中，3 条 Semantic Scholar query 都没有返回有效文献，主要原因是 429。但 v2 仍生成了完整 proposal，并被平台记录为 provisional novel。

这说明：

```text
文献为空或检索失败，不会在 v2 原流程中自动阻止 FinalizeIdea。
```

### 4. 备用源证明空返回不等于没有相关文献

在 diffusion v2 中，Semantic Scholar 返回为空，但 arXiv 能返回 classifier-free guidance、oversaturation、self-attention guidance 等相关候选。

所以不能把单一检索源的空返回解释成“没有相关工作”。

### 5. Energy 平台显示跨领域适配风险更明显

Energy v2 在一次 smoke run 中生成了带有 OPF、N-1 security、demand response 等术语的 query，但只成功返回 4 条标题，且另外两条 query 都发生 429。

人工审查认为 `conformal_opf_reserve_activation` 并不够新颖，这与 post-hoc 多源判断一致：该 idea 应标为 `novelty_not_established`，需要人工复核。

## 当前主结果

### Diffusion v1

位置：`data_20260428/diffusion/v1`

- `learning_rate_schedule`: `novel=False`
- `cluster_conditioned_diffusion`: `novel=True`

`cluster_conditioned_diffusion` 有相关研究但可能仍有一定增量。这个结果说明 AI-Scientist 的 novelty 判断不是简单的“有相关文献就不 novel”，而是由 LLM 判断是否有 significant overlap。

### Diffusion v2

位置：`data_20260428/diffusion/v2`

- idea: `diversity_adaptive_guidance`
- 平台标记：`is_novel=true`
- 解释：provisional
- query 数：3
- retrieved titles：0
- 问题：3 条 query 均未返回有效文献，主要受 429 影响。

### Energy v1

位置：`data_20260428/energy/v1`

- `forecast_aware_storage_dispatch`: `novel=False`
- `adaptive_peak_shaving_dispatch`: `novel=False`

其中 `adaptive_peak_shaving_dispatch` 的 query audit 显示 `energy_terms=none`。这不代表 query 必然不属于能源领域，只代表没有命中当前手写 audit 词表。

### Energy v2

位置：`data_20260428/energy/v2`

- idea: `conformal_opf_reserve_activation`
- 平台标记：`is_novel=true`
- 解释：provisional
- query 数：3
- 成功返回标题：4
- 失败：第 1、3 条 query 发生 429

人工审查认为该 idea 不够新颖。当前 post-hoc 判断也将其降级为 `novelty_not_established`。

## 最终判断

当前最稳妥的结论是：

```text
AI-Scientist 可以生成有价值的候选 idea 和初步 related-work reasoning，
但 novelty claim 不能脱离 query、检索结果和错误状态单独解释。
```

尤其对 v2：

```text
FinalizeIdea 不等于独立 novelty decision。
```

如果要把 AI-Scientist 用作科研 novelty 辅助工具，需要补充：

- query audit；
- 多源检索；
- 检索失败状态；
- evidence sufficiency 判断；
- finalize 后独立 novelty gate；
- 人工复核流程。
