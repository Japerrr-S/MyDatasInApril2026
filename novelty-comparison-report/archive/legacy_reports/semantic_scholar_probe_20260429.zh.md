# Semantic Scholar 匿名访问探测：2026-04-29

## 1. 探测目的

本次探测用于回答：

```text
现在 Semantic Scholar 匿名访问是否仍然全部 429？
```

探测方式：

- 只跑 diffusion platform 的 v2；
- 输出先放在临时 run 目录；
- 如果全部 query 都是 429，则删除、不归档；
- 如果至少有有效返回，则保留并整理。

## 2. 结果结论

本次不是全部 429，因此已保留数据。

结果位置：

```text
data_semantic_scholar_probe_20260429/diffusion/v2/
```

query audit：

```text
queries = 3
avg_query_len = 14.0
retrieved_titles = 3
```

## 3. Query 结果概况

### Query 1

内容：

```text
diffusion models adaptive guidance uncertainty score norm confidence classifier-free guidance dynamic schedule fast sampling denoiser self-estimated uncertainty mode coverage
```

结果：

```text
先 429，重试后 200 total=0
```

解释：

这说明匿名访问没有完全封锁，但该 query 没返回论文。

### Query 2

内容：

```text
"diffusion" dynamic classifier-free guidance confidence OR uncertainty OR adaptive guidance sampling
```

结果：

```text
200 total=3
```

返回标题：

- `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking`
- `Navigating with Annealing Guidance Scale in Diffusion Space`
- `Fast and faithful: accelerating data-free knowledge distillation via confidence-aware adaptive diffusion`

解释：

这条 query 成功返回了高度相关候选，尤其第一篇与本次 idea 的主题非常接近。

### Query 3

内容：

```text
"diffusion model" uncertainty estimation sampling denoiser disagreement dropout ensemble score confidence adaptive step size
```

结果：

```text
429 after retries
```

解释：

同一次 v2 run 中仍然有 query 被 429 限制。

## 4. 本次生成的 idea

v2 生成：

```text
uncertainty_aware_cfg
Uncertainty-Aware Classifier-Free Guidance for Diffusion Sampling
```

该 idea 主张用 denoiser disagreement / stochastic perturbation 来估计局部不确定性，并据此调节 classifier-free guidance 强度。

## 5. 对 novelty 的影响

本次 Semantic Scholar 返回的候选文献已经显示该方向存在非常接近的相关工作，尤其是：

```text
Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking
```

这不等于已经严格证明 `uncertainty_aware_cfg` 完全不 novel，因为还需要阅读摘要和正文比较具体机制。但它足以说明：

```text
不能把该 idea 直接接受为 strong novel。
```

更合适的状态仍然是：

```text
novelty_not_established
needs_human_review_before_accepting_novelty
```

## 6. 对完整 run 的影响

本次结果比“全部 429”更好，但还不能说明当前适合大规模完整 run。

原因：

- 同一次 v2 run 里仍然出现多个 429；
- 匿名访问稳定性不足；
- v2 会连续调用 Semantic Scholar，query 数量增加后仍很容易触发限制。

因此当前更适合：

- 小批量 probe；
- query logging；
- backup search；
- post-hoc novelty review；

而不是大规模 full run。
