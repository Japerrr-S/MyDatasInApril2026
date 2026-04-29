# 05 检索源与备用源

## 为什么需要备用检索源

AI-Scientist 原流程主要依赖 Semantic Scholar。

但本实验中多次遇到：

- 429 rate limit；
- query 返回空；
- abstract 缺失；
- top results 不够相关。

如果只看 Semantic Scholar 返回为空，就可能误以为：

```text
没有相关文献，因此 idea novel。
```

这在逻辑上不成立。

## Semantic Scholar

优点：

- 原 AI-Scientist 默认使用；
- 返回结构化字段；
- 可返回 title、authors、venue、year、citationCount、abstract；
- 适合和原仓库行为保持一致。

缺点：

- 匿名访问容易触发 429；
- 没有 API key 时不稳定；
- 一次只看 top 10 可能漏掉关键文献；
- 检索失败时 v2 原流程不会自动给出 unknown。

## OpenAlex

优点：

- 覆盖面广；
- 可作为 Semantic Scholar 的独立对照；
- 对部分 query 能返回候选文献。

缺点：

- 对长 query 或跨领域 query 可能返回宽泛结果；
- 标题相关不等于核心 novelty overlap；
- 需要进一步 relevance filtering。

## arXiv

优点：

- 对 diffusion / ML 方向尤其有用；
- 在 Semantic Scholar 429 时，仍能返回 classifier-free guidance、oversaturation、self-attention guidance 等相关候选；
- 适合补充近期预印本。

缺点：

- 覆盖能源电力主流 IEEE 文献不足；
- 不适合完全替代 Semantic Scholar；
- 仍需要人工判断标题和摘要是否真正重叠。

## 备用源实验结论

`data_backup_search_20260428/` 显示：

- Diffusion v2 是最关键样本。Semantic Scholar 没有返回论文，但 arXiv 返回多个相关候选。
- Energy 领域中，OpenAlex / arXiv 能补充 smart grid、OPF、demand response、DER coordination 等候选，但噪声较高。

因此：

```text
备用源能降低“单一检索源失败”的风险，
但不能直接替代人工 novelty 判断。
```

## post-hoc novelty decision

本项目把备用检索结果纳入事后判断：

```text
data_posthoc_novelty_20260428/
```

结果：

- `diversity_adaptive_guidance`
  - 原 v2：`novel=True (provisional)`
  - post-hoc：`novelty_not_established`
- `conformal_opf_reserve_activation`
  - 原 v2：`novel=True (provisional)`
  - post-hoc：`novelty_not_established`

这不是证明它们一定不 novel，而是说明现有证据不足以接受 strong novelty claim。

## 2026-04-29 探测

`data_semantic_scholar_probe_20260429/` 中，diffusion v2 的 Semantic Scholar 匿名访问不是全部 429：

- 3 条 query；
- 1 条成功；
- 返回 3 篇标题；
- 同一轮仍有 query 429。

Energy v2 同日临时探测中，3 条 query 全部 429，因此没有归档。

结论：

```text
Semantic Scholar 匿名访问有局部恢复，但仍不足以支撑稳定完整 run。
```
