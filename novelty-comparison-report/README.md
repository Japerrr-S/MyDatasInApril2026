# AI-Scientist Novelty Audit Report

这个仓库整理了两个实验平台的结果：

- `diffusion-novelty-platform`
- `energy-novelty-platform`

目标是审计 AI-Scientist v1/v2 在生成科研 idea 和进行 novelty / literature search 时的可靠性，尤其关注一个风险：

> 如果 LLM 生成的 query 不充分，或 Semantic Scholar 检索失败，系统是否仍可能把 idea 当作 novel？

## 结论先读

当前实验支持以下判断：

- v1 也可能误判 novelty，但它至少有一个相对独立的 `check_idea_novelty` 阶段。
- v2 没有与 v1 等价的独立 novelty gate。它是在 ideation 过程中调用 `SearchSemanticScholar`，然后由 LLM 自行决定继续搜索还是 `FinalizeIdea`。
- v2 原仓库的 finalized proposal 没有原生 `novel: true/false` 布尔标签。本仓库中的 `is_novel=true` 是平台适配层为了统一比较而加的 provisional 标记。
- 在检索失败、返回文献为空或 query 覆盖不足时，v2 仍可能 finalize idea。因此 v2 的 novelty 只能视为 `provisional`，需要独立 post-hoc 检索和人工复核。
- 备用检索源显示：Semantic Scholar 空返回或 429 不等于没有相关文献。

## 推荐阅读顺序

1. [实验总览](docs/01_experiment_summary.zh.md)
2. [实验方法](docs/02_methodology.zh.md)
3. [平台构成](docs/03_platform_design.zh.md)
4. [v2 机制与空文献风险](docs/04_v2_mechanism_and_failure_modes.zh.md)
5. [检索源与备用源](docs/05_retrieval_and_backup_sources.zh.md)
6. [结果文件索引](docs/06_result_index.zh.md)
7. [GitHub 上传说明](docs/07_github_upload.zh.md)

旧版长报告已归档到：

```text
archive/legacy_reports/
```

它们保留作为证据链和写作材料，不再作为 GitHub 首页的主阅读路径。

## 仓库结构

```text
docs/
  01_experiment_summary.zh.md
  02_methodology.zh.md
  03_platform_design.zh.md
  04_v2_mechanism_and_failure_modes.zh.md
  05_retrieval_and_backup_sources.zh.md
  06_result_index.zh.md
  07_github_upload.zh.md

data_20260428/
  当前最重要的一批 v1/v2 smoke run 结果。

data_20260428_s2paced/
  Semantic Scholar 429 节流/冷却测试。

data_backup_search_20260428/
  OpenAlex / arXiv 备用检索源对照。

data_posthoc_novelty_20260428/
  基于多源证据的事后 novelty decision。

data_semantic_scholar_probe_20260429/
  2026-04-29 Semantic Scholar 匿名访问探测。

archive/legacy_reports/
  旧版长报告与原始说明文档归档。

tools/
  辅助脚本。
```

## 最重要的数据入口

- Diffusion 主对比：  
  [data_20260428/diffusion/comparison/comparison.zh.md](data_20260428/diffusion/comparison/comparison.zh.md)

- Energy 主对比：  
  [data_20260428/energy/comparison/comparison.zh.md](data_20260428/energy/comparison/comparison.zh.md)

- v2 事后多源 novelty decision：  
  [data_posthoc_novelty_20260428/posthoc_multi_source_novelty_decision.zh.md](data_posthoc_novelty_20260428/posthoc_multi_source_novelty_decision.zh.md)

- 2026-04-29 Semantic Scholar 探测：  
  [data_semantic_scholar_probe_20260429/README.md](data_semantic_scholar_probe_20260429/README.md)

## 注意事项

- 当前结果主要是 smoke run，不是大样本统计实验。
- 未配置 Semantic Scholar API key，429 限流是本实验的重要变量。
- Energy 平台的 template 和 audit 词表是手工构造的轻量领域适配材料，不是经过领域验证的专业 benchmark。
- `retrieved_titles` 是审计汇总字段，只列出检索返回标题；原 AI-Scientist 判断时还会看到 abstract 等字段。
- 对于 `novel=True`，请同时查看 query、retrieved_titles、error、备用检索结果和 post-hoc decision。
- 本仓库只归档实验报告和数据，不包含原 `AI-Scientist` / `AI-Scientist-v2` 源码仓库。
