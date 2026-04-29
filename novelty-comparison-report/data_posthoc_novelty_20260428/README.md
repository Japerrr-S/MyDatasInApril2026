# Post-hoc Multi-source Novelty Decision：2026-04-28

本目录保存基于现有结果的事后独立 novelty decision。

## 设计原则

本批次不重新生成 idea，也不修改原 AI-Scientist-v2 的输出。它复用：

- `data_20260428` 中的 v2 ideas；
- Semantic Scholar query events / query audit；
- `data_backup_search_20260428` 中的 OpenAlex / arXiv 备用检索结果。

目标是补上原 v2 缺少的一个步骤：

```text
finalized idea -> multi-source evidence review -> independent novelty status
```

## 重要限制

当前 post-hoc decision 主要基于 query、标题和少量元数据，而不是完整论文正文或专家审查。因此它采用保守状态：

- `novelty_not_established`
- `needs_human_review`

这表示“不能接受原 v2 的 provisional novel 作为强 novelty 结论”，不等价于已经严格证明 idea 不 novel。

## 文件

- `diffusion_v2_posthoc_novelty.json`
- `energy_v2_posthoc_novelty.json`
- `posthoc_multi_source_novelty_decision.zh.md`
