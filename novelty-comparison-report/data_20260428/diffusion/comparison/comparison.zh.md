# Diffusion v1/v2 Query 对比：2026-04-28 重跑

## v1 结果

v1 本轮包含两个 idea：

- `learning_rate_schedule`：novel=False
- `cluster_conditioned_diffusion`：novel=True

query audit：

- `learning_rate_schedule`
  - queries=1
  - avg_query_len=8.0
  - retrieved_titles=10
- `cluster_conditioned_diffusion`
  - queries=2
  - avg_query_len=8.5
  - retrieved_titles=20

解释：v1 在本轮中能够从 Semantic Scholar 拿到较多返回。`cluster_conditioned_diffusion` 虽被判为 novel，但其 query 返回了 20 个标题，后续应人工检查这些标题中是否已有足够接近的 pseudo-label / cluster-conditioned diffusion 工作。

## v2 结果

v2 本轮生成：

- `diversity_adaptive_guidance`：novel=True，provisional

query audit：

- `diffusion_models`
  - queries=3
  - avg_query_len=17.3
  - retrieved_titles=0

解释：v2 生成的 idea 结构完整，但 3 个 Semantic Scholar query 都没有有效返回论文，主要受 429 rate limit 影响。因此这里的 `novel=True` 不能视为严格 novelty 判断，只能说明 v2 在 literature search 失败或证据不足时仍然 finalize 了 proposal。

## 对比结论

本轮 diffusion 结果强化了一个关键差异：

- v1 的 novelty check 更接近独立 gate，能把 query、返回论文和最终 decision 分开审计。
- v2 更像 literature-informed ideation，proposal 质量可能更高，但检索失败不会阻止 finalize。

因此，v1/v2 的 `novel=True` 不应直接等价比较。v2 需要额外的独立 novelty gate 才能和 v1 公平对照。
