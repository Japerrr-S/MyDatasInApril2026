# 事后多源 Novelty Decision：2026-04-28

## 1. 为什么需要这一步

你观察到的现象是正确的：备用检索源没有进入原 AI-Scientist-v2 的 novelty decision。原因是 v2 的机制决定的。

原 v2 的流程是：

```text
literature search inside ideation -> FinalizeIdea
```

而不是：

```text
FinalizeIdea -> independent multi-source novelty check -> final novelty decision
```

因此，OpenAlex / arXiv 备用检索只能作为我们平台新增的对照证据。若要让它们影响 novelty，就必须额外做一个事后独立判断。

## 2. 本次 post-hoc decision 的输入

本次没有重新生成 idea，也没有改变原 v2 prompt。输入包括：

- v2 finalized ideas；
- Semantic Scholar query events；
- Semantic Scholar query audit；
- OpenAlex / arXiv backup search audit。

对应目录：

```text
data_20260428/
data_backup_search_20260428/
```

输出目录：

```text
data_posthoc_novelty_20260428/
```

## 3. 判断原则

由于当前备用检索主要是标题级证据，而不是完整论文阅读，因此本次采用保守判断：

```text
novelty_not_established
```

它的含义是：

```text
不能接受原 v2 的 provisional novel 作为强 novelty 结论。
```

它不等价于：

```text
已经严格证明该 idea 不 novel。
```

换句话说，本次 post-hoc gate 的作用是把“看起来 novel”降级为“需要人工文献审查后才能确认”。

## 4. Diffusion v2：diversity_adaptive_guidance

原 v2 状态：

```text
novel=True (provisional)
```

事后多源判断：

```text
posthoc_novelty_status = novelty_not_established
decision = needs_human_review_before_accepting_novelty
```

理由：

- Semantic Scholar 原始检索因 429 返回 0 个标题。
- arXiv 备用检索返回多个明显相关标题。
- 相关候选包括：
  - `Classifier-Free Diffusion Guidance`
  - `Rethinking Oversaturation in Classifier-Free Guidance via Low Frequency`
  - `Bridging the Gap: Addressing Discrepancies in Diffusion Model Training for Classifier-Free Guidance`
  - `Improving Sample Quality of Diffusion Models Using Self-Attention Guidance`
  - `Token Perturbation Guidance for Diffusion Models`

解释：

`diversity_adaptive_guidance` 的 idea 不是被标题级证据直接证明为重复，但它显然落在已有 classifier-free guidance、oversaturation、guidance perturbation、self-attention guidance 等文献空间中。因此不能把 Semantic Scholar 空返回解释为 novelty 证据。

## 5. Energy v2：conformal_opf_reserve_activation

原 v2 状态：

```text
novel=True (provisional)
```

事后多源判断：

```text
posthoc_novelty_status = novelty_not_established
decision = needs_human_review_before_accepting_novelty
```

理由：

- Semantic Scholar 返回证据有限，且部分 query 受 429 影响。
- OpenAlex / arXiv 返回了 OPF、renewable uncertainty、demand response、smart grid、resilience 等候选。
- 相关候选包括：
  - `AC optimal power flow in the presence of renewable sources and uncertain loads`
  - `hynet: An Optimal Power Flow Framework for Hybrid AC/DC Power Systems`
  - `Online Algorithm for Demand Response with Inelastic Demands and Apparent Power Constraint`
  - `Data-driven Coordination of Distributed Energy Resources for Active Power Provision`

解释：

当前标题级证据没有直接证明 `conformal_opf_reserve_activation` 与已有工作完全重合。但该 idea 的 novelty 取决于一个细粒度组合：

```text
conformal prediction
+ network-aware uncertainty set
+ security-constrained OPF
+ reserve activation
+ forecast shift
```

仅靠当前 query 和标题级结果无法确认这个组合足够 novel，因此应标记为 `novelty_not_established`。

## 6. 与原 v2 结果的关系

原 v2 的输出仍然保留：

```text
novel=True (provisional)
```

本次新增的是平台层独立判断：

```text
posthoc_novelty_status = novelty_not_established
```

二者并不冲突。它们表达的是不同层次：

- 原 v2：proposal generation 流程成功 finalize。
- post-hoc gate：基于多源检索证据，尚不能接受其 novelty。

## 7. 结论

备用检索源没有用于原 v2 novelty decision，确实是 v2 生成机制导致的：v2 没有 finalize 后的独立 novelty gate。

当我们补上一个事后多源 gate 后，两个 v2 idea 都不应直接接受为 strong novel，而应标为：

```text
novelty_not_established
needs_human_review_before_accepting_novelty
```

这进一步支持本项目的核心结论：

```text
v2 的 novel=True 只能作为 provisional 标记；
真正的 novelty 判断需要独立、多源、可审计的检索证据。
```
