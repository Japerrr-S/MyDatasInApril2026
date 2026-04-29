# 结果索引

本文档是当前所有结果文件的导航。若要看最新分析，请优先阅读 `data_20260428` 和 `data_20260428_s2paced`。

## 总报告

- `reports/final_experiment_summary.zh.md`
- `reports/overall_summary.zh.md`
- `reports/platform_design_overview.zh.md`
- `reports/prompt_comparison_ai_scientist_platform.zh.md`
- `reports/query_event_index.zh.md`
- `reports/backup_search_control_20260428.zh.md`
- `reports/v2_empty_literature_behavior.zh.md`
- `reports/v2_ideation_and_novelty_mechanism.zh.md`
- `reports/semantic_scholar_probe_20260429.zh.md`
- `reports/semantic_scholar_429_retry_20260428.zh.md`

## 方法说明

- `methodology/experiment_setup.zh.md`

## 第一批归档：data

这批结果来自最初的 smoke run，用于验证平台、日志和比较流程。

### Diffusion

- `data/diffusion/v1/ideas.json`
- `data/diffusion/v1/novelty_decisions.json`
- `data/diffusion/v1/novelty_events.jsonl`
- `data/diffusion/v1/query_audit.json`
- `data/diffusion/v2/ideas.json`
- `data/diffusion/v2/novelty_decisions.json`
- `data/diffusion/v2/novelty_events.jsonl`
- `data/diffusion/v2/query_audit.json`
- `data/diffusion/comparison/comparison.zh.md`
- `data/diffusion/comparison/comparison.json`

### Energy

- `data/energy/v1/ideas.json`
- `data/energy/v1/novelty_decisions.json`
- `data/energy/v1/novelty_events.jsonl`
- `data/energy/v1/query_audit.json`
- `data/energy/v2/ideas.json`
- `data/energy/v2/novelty_decisions.json`
- `data/energy/v2/novelty_events.jsonl`
- `data/energy/v2/query_audit.json`
- `data/energy/comparison/comparison.zh.md`
- `data/energy/comparison/comparison.json`

## 最新完整归档：data_20260428

这是 2026-04-28 改善网络后重新运行的结果，也是目前最值得逐条分析的一批。

### Diffusion

- `data_20260428/diffusion/v1/ideas.json`
- `data_20260428/diffusion/v1/novelty_decisions.json`
- `data_20260428/diffusion/v1/novelty_events.jsonl`
- `data_20260428/diffusion/v1/query_audit.json`
- `data_20260428/diffusion/v2/ideas.json`
- `data_20260428/diffusion/v2/novelty_decisions.json`
- `data_20260428/diffusion/v2/novelty_events.jsonl`
- `data_20260428/diffusion/v2/query_audit.json`
- `data_20260428/diffusion/comparison/comparison.zh.md`
- `data_20260428/diffusion/comparison/comparison.json`

### Energy

- `data_20260428/energy/v1/ideas.json`
- `data_20260428/energy/v1/novelty_decisions.json`
- `data_20260428/energy/v1/novelty_events.jsonl`
- `data_20260428/energy/v1/query_audit.json`
- `data_20260428/energy/v2/ideas.json`
- `data_20260428/energy/v2/novelty_decisions.json`
- `data_20260428/energy/v2/novelty_events.jsonl`
- `data_20260428/energy/v2/query_audit.json`
- `data_20260428/energy/comparison/comparison.zh.md`
- `data_20260428/energy/comparison/comparison.json`

## 节流实验归档：data_20260428_s2paced

这批结果用于观察“原仓库 backoff + 平台层请求间隔/429 冷却”是否能缓解 Semantic Scholar 429。

- `data_20260428_s2paced/diffusion/v1/ideas.json`
- `data_20260428_s2paced/diffusion/v1/novelty_decisions.json`
- `data_20260428_s2paced/diffusion/v1/novelty_events.jsonl`
- `data_20260428_s2paced/diffusion/v1/query_audit.json`
- `data_20260428_s2paced/energy/v2/ideas.json`
- `data_20260428_s2paced/energy/v2/novelty_decisions.json`
- `data_20260428_s2paced/energy/v2/novelty_events.jsonl`
- `data_20260428_s2paced/energy/v2/query_audit.json`

## 备用检索源对照：data_backup_search_20260428

这批结果复用 `data_20260428` 中已记录的 query，额外调用 OpenAlex 和 arXiv，不改变原 AI-Scientist 的 idea generation 或 novelty decision。

- `data_backup_search_20260428/README.md`
- `data_backup_search_20260428/diffusion/v1/backup_search_events.jsonl`
- `data_backup_search_20260428/diffusion/v1/backup_search_audit.json`
- `data_backup_search_20260428/diffusion/v2/backup_search_events.jsonl`
- `data_backup_search_20260428/diffusion/v2/backup_search_audit.json`
- `data_backup_search_20260428/energy/v1/backup_search_events.jsonl`
- `data_backup_search_20260428/energy/v1/backup_search_audit.json`
- `data_backup_search_20260428/energy/v2/backup_search_events.jsonl`
- `data_backup_search_20260428/energy/v2/backup_search_audit.json`

## 事后独立 Novelty Decision：data_posthoc_novelty_20260428

这批结果基于 v2 finalized ideas、Semantic Scholar query audit、OpenAlex/arXiv backup search audit，额外做一个平台层独立 novelty decision。

- `data_posthoc_novelty_20260428/README.md`
- `data_posthoc_novelty_20260428/posthoc_multi_source_novelty_decision.zh.md`
- `data_posthoc_novelty_20260428/diffusion_v2_posthoc_novelty.json`
- `data_posthoc_novelty_20260428/energy_v2_posthoc_novelty.json`

## Semantic Scholar 匿名访问探测：data_semantic_scholar_probe_20260429

这批结果用于检查 2026-04-29 匿名 Semantic Scholar 是否仍然全部 429。本次不是全部 429，因此保留。

- `data_semantic_scholar_probe_20260429/README.md`
- `data_semantic_scholar_probe_20260429/diffusion/v2/ideas.json`
- `data_semantic_scholar_probe_20260429/diffusion/v2/novelty_decisions.json`
- `data_semantic_scholar_probe_20260429/diffusion/v2/novelty_events.jsonl`
- `data_semantic_scholar_probe_20260429/diffusion/v2/query_audit.json`
- `reports/semantic_scholar_probe_20260429.zh.md`
