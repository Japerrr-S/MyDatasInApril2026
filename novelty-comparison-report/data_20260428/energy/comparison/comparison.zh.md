# Energy v1/v2 Query 对比：2026-04-28 重跑

## v1 结果

v1 本轮包含两个 idea：

- `forecast_aware_storage_dispatch`：novel=False
- `adaptive_peak_shaving_dispatch`：novel=False

query audit：

- `adaptive_peak_shaving_dispatch`
  - queries=1
  - avg_query_len=12.0
  - energy_terms=none
  - retrieved_titles=1

解释：v1 对新生成的 `adaptive_peak_shaving_dispatch` 判为 not novel，但本轮 query audit 只稳定记录到 1 条 query 和 1 个返回标题。虽然方向上与储能调度相关，但 energy 领域术语覆盖仍偏弱。

## v2 结果

v2 本轮生成：

- `conformal_opf_reserve_activation`：novel=True，provisional

query audit：

- `energy_power_systems`
  - queries=3
  - avg_query_len=20.0
  - energy_terms=demand response, electricity market, frequency regulation, n-1 security, optimal power flow, renewable integration
  - retrieved_titles=4

解释：相比第一批 energy v2，本轮 query 的能源电力术语覆盖明显更好，尤其包含 `optimal power flow`、`N-1 security`、`renewable integration` 等关键概念。但返回论文数量仍然有限，并且仍受 429 影响。因此 `conformal_opf_reserve_activation` 的 novelty 仍只能视为 provisional。

## 对比结论

Energy 本轮结果说明：

- v2 能够生成结构完整、领域术语更强的能源电力 proposal。
- 但 v2 的检索证据仍不足以独立支撑 novelty。
- v1 的判断更保守，但 query 覆盖不一定充分。

这说明跨领域适配不能只改 prompt，还需要领域 query 扩展、检索后端稳定性，以及独立 novelty gate。
