# Diffusion 平台 v1/v2 Query 审计对比解读

## 运行对象

- v1: `runs/autodl_smoke_v1_001`
- v2: `runs/autodl_smoke_v2_logged_002`

## 核心观察

v1 的独立 novelty check 对 `self_conditioned_mode_control` 发起了 1 个成功记录的 query，并检索到 8 个标题，其中包括强相关工作：

- `Why Are Conditional Generative Models Better Than Unconditional Ones?`

因此 v1 将该 idea 判为 `novel=False`。

v2 在 ideation 阶段对 `self_certified_guidance` 发起了 2 个 query，但由于 Semantic Scholar 无 key 模式频繁 429，这两个 query 没有检索到任何标题，最终仍然产出了 idea，并被平台暂记为 `novel=True (provisional)`。

## 对原始假设的意义

这正好暴露了要研究的问题：

```text
如果 query 没有拿到有效文献证据，v2 仍可能继续 finalize idea。
```

不过这里不能直接证明 idea 非 novel，因为失败原因主要是 Semantic Scholar 限流，而不是 query 语义一定错误。它说明的是：

- v2 的 novelty evidence 不完整；
- v2 缺少独立 novelty gate；
- 检索失败没有阻止 finalization；
- query/event logging 对判断 novelty 风险是必要的。

## 下一步建议

给 v2 加一个独立 novelty check，复用 v1 风格的多轮检索与 final decision。否则 v1/v2 的 `novel` 语义并不等价。

