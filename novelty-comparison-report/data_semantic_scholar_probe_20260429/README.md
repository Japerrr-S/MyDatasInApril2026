# Semantic Scholar Probe：2026-04-29

本目录保存 2026-04-29 对匿名 Semantic Scholar 可用性的临时 v2 探测结果。

## 运行规则

用户要求：

```text
如果依然被限制导致无法查阅文献，也就是全部 429，则不用记录数据。
```

本次运行结果不是全部 429：

- 第 1 条 query：先遇到 429，重试后返回 `200 total=0`。
- 第 2 条 query：返回 `200 total=3`，成功拿到 3 个标题。
- 第 3 条 query：最终仍为 429。

因此本批次被保留。

## 结果位置

```text
data_semantic_scholar_probe_20260429/diffusion/v2/
```

包含：

- `ideas.json`
- `novelty_decisions.json`
- `novelty_events.jsonl`
- `query_audit.json`
- `run_config.json`

## 核心观察

本次 v2 生成 idea：

```text
uncertainty_aware_cfg
Uncertainty-Aware Classifier-Free Guidance for Diffusion Sampling
```

query audit：

```text
queries = 3
retrieved_titles = 3
```

返回标题包括：

- `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking`
- `Navigating with Annealing Guidance Scale in Diffusion Space`
- `Fast and faithful: accelerating data-free knowledge distillation via confidence-aware adaptive diffusion`

## 解释

匿名 Semantic Scholar 当前不是完全不可用，但仍然不稳定。它已经可以偶尔返回有效结果，但同一次 v2 run 中仍然出现 429。

因此，这次结果说明：

```text
当前条件比全部 429 更好，但仍不足以支撑大规模完整 run。
```

对于 v2 的 novelty 解释，本次返回的 `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking` 与生成 idea 的 `Uncertainty-Aware Classifier-Free Guidance` 高度相关。因此该 idea 不应直接接受为 strong novel，仍应进入 post-hoc novelty review。
