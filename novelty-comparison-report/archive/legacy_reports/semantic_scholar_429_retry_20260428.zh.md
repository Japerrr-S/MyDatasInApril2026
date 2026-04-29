# Semantic Scholar 429 节流实验记录

日期：2026-04-28

## 实验目的

在尽量保留原 AI-Scientist 检索行为的前提下，尝试降低 Semantic Scholar 429 限流对 novelty check / literature search 的影响。

## 修改方式

本次没有修改 idea generation prompt、query 生成逻辑或 novelty 判断标准。只在 Semantic Scholar 请求附近增加了轻量节流：

- 仍使用原仓库的 `backoff.expo + HTTPError retry`。
- 每次 Semantic Scholar 请求前支持最小间隔等待。
- 如果返回 429，优先读取 `Retry-After`；如果没有，则按配置等待。
- v1 额外补充失败 query 日志，避免全 429 时 `novelty_events.jsonl` 为空。

本次配置：

- `S2_REQUEST_INTERVAL=12`
- `S2_429_COOLDOWN=60`
- `max_tries=3`
- 未配置 `S2_API_KEY`

## 已运行结果

### Diffusion v1

运行目录：

- `diffusion-novelty-platform/runs/autodl_smoke_20260428_s2paced_v1`
- `novelty-comparison-report/data_20260428_s2paced/diffusion/v1`

观察：

- 生成 idea：`unsupervised_mode_conditioning`
- Semantic Scholar 请求持续返回 429。
- 即使每次 429 后等待 60 秒，仍未恢复。
- 由于本次运行发生在 v1 失败 query 日志补丁之前，归档的 `query_audit.json` 为空；后续 v1 run 会记录失败 query。

### Energy v2

运行目录：

- `energy-novelty-platform/runs/autodl_smoke_20260428_s2paced_v2`
- `novelty-comparison-report/data_20260428_s2paced/energy/v2`

观察：

- 生成 idea：`market_calibrated_flexibility_opf`
- 记录到 2 条 query。
- 两条 query 均持续返回 429。
- 由于 v2 会记录失败 query，因此 `query_audit.json` 中可以看到 query 数量、领域术语覆盖情况，但 `retrieved_titles` 为空。

## 初步结论

这次结果说明：在没有 `S2_API_KEY` 的情况下，单靠原仓库式 backoff 加 12 秒请求间隔和 60 秒 429 冷却，仍不足以稳定恢复 Semantic Scholar 检索。

这更像是匿名额度在较长时间窗口内被限制，而不是瞬时请求过快。因此，若要做稳定实验，推荐下一步优先使用：

- Semantic Scholar API key；
- 更长冷却时间；
- 本地 query 缓存；
- 或备用检索源。

对 novelty 实验本身而言，这次结果仍有价值：它进一步显示当检索失败时，v2 仍会继续 finalize idea，因此必须在平台层把“检索失败”和“未发现相关论文”明确区分。
