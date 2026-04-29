# 06 结果文件索引

## 主阅读文件

- [README](../README.md)
- [01 实验总览](01_experiment_summary.zh.md)
- [02 实验方法](02_methodology.zh.md)
- [03 平台构成](03_platform_design.zh.md)
- [04 v2 机制与空文献风险](04_v2_mechanism_and_failure_modes.zh.md)
- [05 检索源与备用源](05_retrieval_and_backup_sources.zh.md)
- [07 GitHub 上传说明](07_github_upload.zh.md)

## 主结果：`data_20260428`

这是当前最重要的一批结果。

### Diffusion

- [diffusion comparison](../data_20260428/diffusion/comparison/comparison.zh.md)
- `data_20260428/diffusion/v1/ideas.json`
- `data_20260428/diffusion/v1/novelty_decisions.json`
- `data_20260428/diffusion/v1/novelty_events.jsonl`
- `data_20260428/diffusion/v1/query_audit.json`
- `data_20260428/diffusion/v2/ideas.json`
- `data_20260428/diffusion/v2/novelty_decisions.json`
- `data_20260428/diffusion/v2/novelty_events.jsonl`
- `data_20260428/diffusion/v2/query_audit.json`

### Energy

- [energy comparison](../data_20260428/energy/comparison/comparison.zh.md)
- `data_20260428/energy/v1/ideas.json`
- `data_20260428/energy/v1/novelty_decisions.json`
- `data_20260428/energy/v1/novelty_events.jsonl`
- `data_20260428/energy/v1/query_audit.json`
- `data_20260428/energy/v2/ideas.json`
- `data_20260428/energy/v2/novelty_decisions.json`
- `data_20260428/energy/v2/novelty_events.jsonl`
- `data_20260428/energy/v2/query_audit.json`

## Semantic Scholar 429 测试

目录：

```text
data_20260428_s2paced/
```

重点文件：

- `data_20260428_s2paced/diffusion/v1/novelty_events.jsonl`
- `data_20260428_s2paced/diffusion/v1/query_audit.json`
- `data_20260428_s2paced/energy/v2/novelty_events.jsonl`
- `data_20260428_s2paced/energy/v2/query_audit.json`

旧版分析归档：

- `archive/legacy_reports/semantic_scholar_429_retry_20260428.zh.md`

## 备用检索源

目录：

```text
data_backup_search_20260428/
```

重点文件：

- `data_backup_search_20260428/diffusion/v1/backup_search_audit.json`
- `data_backup_search_20260428/diffusion/v2/backup_search_audit.json`
- `data_backup_search_20260428/energy/v1/backup_search_audit.json`
- `data_backup_search_20260428/energy/v2/backup_search_audit.json`

旧版分析归档：

- `archive/legacy_reports/backup_search_control_20260428.zh.md`

## Post-hoc novelty decision

目录：

```text
data_posthoc_novelty_20260428/
```

重点文件：

- [posthoc_multi_source_novelty_decision.zh.md](../data_posthoc_novelty_20260428/posthoc_multi_source_novelty_decision.zh.md)
- `data_posthoc_novelty_20260428/diffusion_v2_posthoc_novelty.json`
- `data_posthoc_novelty_20260428/energy_v2_posthoc_novelty.json`

## 2026-04-29 Semantic Scholar 探测

目录：

```text
data_semantic_scholar_probe_20260429/
```

重点文件：

- [README](../data_semantic_scholar_probe_20260429/README.md)
- `data_semantic_scholar_probe_20260429/diffusion/v2/ideas.json`
- `data_semantic_scholar_probe_20260429/diffusion/v2/novelty_events.jsonl`
- `data_semantic_scholar_probe_20260429/diffusion/v2/query_audit.json`

## 旧版报告归档

旧版报告已移到：

```text
archive/legacy_reports/
```

这些文件包含更长的推理过程和中间版本说明，适合追溯细节，但不再作为主阅读路径。

## 历史 smoke run

目录：

```text
data/
```

这是第一批历史 smoke run，只建议在需要追溯平台早期结果时阅读。
