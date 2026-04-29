# 备用检索源对照实验：2026-04-28

## 1. 实验目的

本实验尝试在不改变 AI-Scientist 生成和判断逻辑的前提下，引入备用检索源作为对照。

核心问题是：

```text
当 Semantic Scholar 429 或返回不足时，同一个 query 在 OpenAlex / arXiv 中是否还能找到候选文献？
```

这可以帮助判断：某个 idea 的检索证据不足，究竟是因为 idea 真的新，还是因为 Semantic Scholar 当前不可用或 query 在某个检索源中效果不好。

## 2. 实验设置

输入 query 来自：

```text
data_20260428/*/*/novelty_events.jsonl
```

没有重新生成 idea，也没有重新运行 AI-Scientist 的 novelty decision。

备用检索源：

- OpenAlex
- arXiv

每个 query 每个来源最多返回 5 条结果。

结果归档：

```text
data_backup_search_20260428/
```

每个子目录包含：

- `backup_search_events.jsonl`
- `backup_search_audit.json`

## 3. Diffusion v1

输入 query 来自：

```text
data_20260428/diffusion/v1/novelty_events.jsonl
```

结果位置：

```text
data_backup_search_20260428/diffusion/v1
```

观察：

- `learning_rate_schedule`：
  - OpenAlex 返回 5 条，但部分结果明显偏泛，例如非 diffusion 或非 learning-rate 主题。
  - arXiv 返回 5 条，其中包含 learning rate schedule 相关标题。
- `cluster_conditioned_diffusion`：
  - OpenAlex 返回 5 条，但噪声较高。
  - arXiv 返回 5 条，包含 self-supervised clustering、conditional graph diffusion、pseudo-label refinement 等候选方向。

解释：

Diffusion v1 原本 Semantic Scholar 已有较多返回。备用检索进一步说明：即使 Semantic Scholar 可用，也应该人工检查多个来源，因为不同检索源返回的相关性差异很大。

## 4. Diffusion v2

输入 query 来自：

```text
data_20260428/diffusion/v2/novelty_events.jsonl
```

结果位置：

```text
data_backup_search_20260428/diffusion/v2
```

原 Semantic Scholar 情况：

```text
queries = 3
retrieved_titles = 0
主要原因：429
```

备用检索观察：

- Query 1：
  - OpenAlex 返回 0 条。
  - arXiv 返回 5 条，包括 guidance、Diffusion-GAN、self-attention guidance 等。
- Query 2：
  - OpenAlex 返回 2 条。
  - arXiv 返回 5 条，包括 `Rethinking Oversaturation in Classifier-Free Guidance via Low Frequency`、`Token Perturbation Guidance for Diffusion Models` 等。
- Query 3：
  - OpenAlex 返回 5 条，但部分结果较宽泛。
  - arXiv 返回 5 条，包括 `Classifier-Free Diffusion Guidance`。

解释：

这组是最关键的对照。Semantic Scholar 因 429 没有返回论文，但 arXiv 对同一 query 能返回多个明显相关标题。因此，Diffusion v2 的 `diversity_adaptive_guidance` 不能因为 Semantic Scholar 空返回而被视为有强 novelty 证据。备用检索说明：相关文献空间实际存在，需要进一步人工审查。

## 5. Energy v1

输入 query 来自：

```text
data_20260428/energy/v1/novelty_events.jsonl
```

结果位置：

```text
data_backup_search_20260428/energy/v1
```

观察：

- `adaptive_peak_shaving_dispatch`：
  - OpenAlex 返回 5 条，主题包含 flexibility market、EV demand response、active distribution network 等，相关性中等但不够精确。
  - arXiv 返回 5 条，包括 battery storage peak shaving、microgrid-PV peak shaving、residential load peak shaving 等。

解释：

Energy v1 的 Semantic Scholar 返回较少，但备用检索能找到更多 peak shaving / battery storage 相关候选。说明 v1 的 not novel 判断可能有一定外部证据支持，但也暴露 query 还需要更准确地区分 feeder constraint、SOC reservation、evening peak dispatch 等细节。

## 6. Energy v2

输入 query 来自：

```text
data_20260428/energy/v2/novelty_events.jsonl
```

结果位置：

```text
data_backup_search_20260428/energy/v2
```

原 Semantic Scholar 情况：

```text
queries = 3
retrieved_titles = 4
部分 query 受 429 影响
```

备用检索观察：

- Query 1：
  - OpenAlex 返回 renewable energy communities、microgrid optimization、smart grid review 等宽泛综述。
  - arXiv 返回 power flow、demand response、DER coordination 等候选。
- Query 2：
  - OpenAlex 返回 microgrid、smart distribution systems、HVDC 等宽泛结果。
  - arXiv 返回 smart grid resilience、demand-side management 等结果。
- Query 3：
  - OpenAlex 返回 smart grid / renewable forecasting 类宽泛结果。
  - arXiv 返回 `AC optimal power flow in the presence of renewable sources and uncertain loads`、hybrid AC/DC OPF 等候选。

解释：

Energy v2 的备用检索表明：OpenAlex 对长而宽的 energy query 容易返回综述或泛主题文献；arXiv 能返回一些技术上相关的 OPF / demand response 文献，但仍需要更精细的 query rewriting 才能准确检索 conformal prediction + OPF + uncertainty shift 的交叉工作。

## 7. 横向结论

### 结论 1：备用检索源能缓解 429 盲区

在 Diffusion v2 中，Semantic Scholar 因 429 没有返回结果，但 arXiv 返回了多个明显相关标题。这说明：

```text
Semantic Scholar 空结果不能直接解释为无相关工作。
```

### 结论 2：备用检索源也有噪声

OpenAlex 对部分长 query 返回了非常宽泛甚至偏题的标题。因此备用检索不是简单“越多越好”，还需要：

- query 重写；
- source-specific query 适配；
- 结果过滤；
- 排序和去重；
- 人工或 LLM-assisted relevance review。

### 结论 3：arXiv 对 ML/diffusion query 更有价值

Diffusion v2 中，arXiv 返回了 guidance、classifier-free guidance、oversaturation 等相关标题。这说明对于 ML 方向，arXiv 是 Semantic Scholar 的有效补充。

### 结论 4：Energy 需要更强领域检索策略

Energy query 在 OpenAlex/arXiv 中能返回候选，但常偏宽。对于 energy/power systems，后续需要加入：

- IEEE / IET / ACM metadata；
- OpenAlex concept/filter；
- domain-specific synonym expansion；
- OPF、DER、SCOPF、distribution restoration 等任务词表。

## 8. 对 Novelty 判断的意义

备用检索实验进一步支持本项目的核心观点：

```text
novelty 判断不能只依赖单一检索源，也不能把检索失败当成没有相关工作。
```

尤其对 v2：

- Semantic Scholar 失败时，v2 仍可 finalize proposal；
- 备用检索表明同一 query 仍可能找到相关候选；
- 因此 v2 的 `novel=True` 必须保持 provisional。

## 9. 后续建议

1. 将备用检索纳入平台正式流程，但与原 AI-Scientist decision 分开记录。
2. 对每个 query 做 source-specific rewrite：
   - Semantic Scholar query；
   - arXiv query；
   - OpenAlex query；
   - energy-domain query。
3. 加入 relevance review，判断返回标题是否真正与 idea overlap。
4. 增加本地缓存，避免重复请求。
5. 对 v2 增加 finalize 后的独立 multi-source novelty gate。
