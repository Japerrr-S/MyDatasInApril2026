# Query 事件索引

本文档说明 query 相关事件被整理在哪里，以及应该如何比较 query 质量。

## 最新推荐入口

优先看 2026-04-28 的完整重跑结果：

- `data_20260428/diffusion/comparison/comparison.zh.md`
- `data_20260428/energy/comparison/comparison.zh.md`
- `data_20260428/diffusion/v1/query_audit.json`
- `data_20260428/diffusion/v2/query_audit.json`
- `data_20260428/energy/v1/query_audit.json`
- `data_20260428/energy/v2/query_audit.json`

若要看 Semantic Scholar 429 节流实验：

- `data_20260428_s2paced/diffusion/v1/query_audit.json`
- `data_20260428_s2paced/energy/v2/query_audit.json`
- `reports/semantic_scholar_429_retry_20260428.zh.md`

若要看备用检索源对照实验：

- `data_backup_search_20260428/diffusion/v1/backup_search_audit.json`
- `data_backup_search_20260428/diffusion/v2/backup_search_audit.json`
- `data_backup_search_20260428/energy/v1/backup_search_audit.json`
- `data_backup_search_20260428/energy/v2/backup_search_audit.json`
- `reports/backup_search_control_20260428.zh.md`

若要看备用检索源如何进入事后 novelty decision：

- `data_posthoc_novelty_20260428/posthoc_multi_source_novelty_decision.zh.md`
- `data_posthoc_novelty_20260428/diffusion_v2_posthoc_novelty.json`
- `data_posthoc_novelty_20260428/energy_v2_posthoc_novelty.json`

## 原始 Query 事件

原始 query 事件保存在各实验分支下的 `novelty_events.jsonl` 中。最新完整归档包括：

- `data_20260428/diffusion/v1/novelty_events.jsonl`
- `data_20260428/diffusion/v2/novelty_events.jsonl`
- `data_20260428/energy/v1/novelty_events.jsonl`
- `data_20260428/energy/v2/novelty_events.jsonl`

节流实验归档包括：

- `data_20260428_s2paced/diffusion/v1/novelty_events.jsonl`
- `data_20260428_s2paced/energy/v2/novelty_events.jsonl`

这些文件是 JSON Lines 格式：每一行是一条独立事件。通常可以看到以下字段：

- `run_id`：本次运行编号。
- `checker`：来自 v1 还是 v2。
- `idea_name`：该 query 对应的 idea 名称。
- `round_index`：novelty check 或 literature search 中的轮次。
- `query`：LLM 实际提交给检索系统的 query。
- `papers`：检索返回论文。
- `error`：检索失败时记录错误，例如 Semantic Scholar 429。

## 汇总后的 Query 审计

`query_audit.json` 是从原始事件中提取的汇总结果，适合快速比较：

- query 数量。
- 平均 query 长度。
- 重复 query 比例。
- 领域关键词覆盖情况。
- 返回论文标题数量。

最新完整归档中，Diffusion v1 返回论文最多，Diffusion v2 检索全部受 429 影响。Energy v2 的 query 领域术语覆盖比第一批更好，但仍有 429。

## 横向比较文件

若目标是比较 v1/v2，不建议直接从 jsonl 开始。更清晰的入口是：

- `data_20260428/diffusion/comparison/comparison.zh.md`
- `data_20260428/energy/comparison/comparison.zh.md`

机器可读版本是：

- `data_20260428/diffusion/comparison/comparison.json`
- `data_20260428/energy/comparison/comparison.json`

## 解释原则

本实验必须区分三件事：

1. 没有搜到相关论文。
2. query 不足以覆盖相关论文。
3. 检索系统失败或被 429 限流。

只有第一种才比较接近“支持 novelty”的证据。第二、三种都不能直接支持 idea novel。当前 v2 多个结果属于第三种风险：query 被记录了，但检索证据不足，idea 仍然被 finalize。
