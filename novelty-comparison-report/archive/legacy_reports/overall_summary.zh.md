# AI-Scientist Novelty/Query 审计阶段性总结

更新日期：2026-04-28

## 1. 核心问题

本实验关注一个具体风险：

```text
AI-Scientist 的 check_novelty / literature search 可能无法保证 100% novelty。
```

风险不只来自 LLM 最终判断，也来自更早的检索环节：

```text
LLM 生成的 query 可能不充分、不准确，或者检索 API 失败；
系统没有发现已有相关工作，却仍然把 idea 视为 novel。
```

因此本平台不只记录 `novel=True/False`，还记录：

- idea 内容；
- 实际生成的 query；
- Semantic Scholar 返回论文；
- 检索失败和 429；
- query 的领域术语覆盖；
- v1/v2 的 decision 差异。

## 2. 实验平台

目前有两个平台：

- `diffusion-novelty-platform`
  - 用于观察 AI-Scientist 在机器学习近域任务中的行为。
  - diffusion 仍属于 AI/ML 研究语境，和原 AI-Scientist 更接近。
- `energy-novelty-platform`
  - 用于观察 AI-Scientist 横向迁移到能源电力领域后的表现。
  - 重点关注 query 是否覆盖 power systems 术语和工程约束。

两个平台都调用原 AI-Scientist / AI-Scientist-v2 的主要 idea generation 与 novelty/literature-search 逻辑。平台本身主要负责领域配置、运行封装、query 日志、审计和结果归档。

## 3. 数据批次

当前报告仓库包含三批结果。

### 3.1 第一批：`data`

用于验证平台和日志流程。

主要现象：

- Diffusion v1 能检索到相关论文并判定部分 idea not novel。
- Diffusion v2 在检索返回不足时仍 finalize idea。
- Energy v2 能生成领域相关 idea，但 query 证据偏少。

### 3.2 最新完整重跑：`data_20260428`

这是目前最推荐分析的一批结果。运行配置仍使用昨天的 smoke 配置：

- AutoDL.Art OpenAI-compatible API；
- `model=gpt-5.4`；
- 未配置 `S2_API_KEY`；
- v1/v2 分开运行；
- 每个平台 `max_ideas=1`。

### 3.3 节流实验：`data_20260428_s2paced`

用于测试“原仓库 backoff + 平台层节流”是否能缓解 Semantic Scholar 429。

新增设置：

- `S2_REQUEST_INTERVAL=12`
- `S2_429_COOLDOWN=60`
- 仍未配置 `S2_API_KEY`

结果显示：60 秒冷却仍不能稳定解除匿名访问的 429 限制。

### 3.4 备用检索源对照：`data_backup_search_20260428`

这批结果不重新生成 idea，也不重新运行 novelty decision。它复用 `data_20260428` 中已经记录的 query，额外调用：

- OpenAlex；
- arXiv。

目标是观察 Semantic Scholar 429 或返回不足时，同一 query 在备用源中是否仍能找到候选文献。

### 3.5 事后独立 novelty decision：`data_posthoc_novelty_20260428`

这批结果把备用检索源正式纳入一个平台层 post-hoc decision。它不改变原 v2 输出，而是在原 v2 `novel=True (provisional)` 之后，额外给出：

```text
posthoc_novelty_status = novelty_not_established
decision = needs_human_review_before_accepting_novelty
```

当前只对 v2 最新两个 idea 做事后判断：

- `diversity_adaptive_guidance`
- `conformal_opf_reserve_activation`

### 3.6 Semantic Scholar 匿名访问探测：`data_semantic_scholar_probe_20260429`

2026-04-29 重新探测 diffusion v2。结果不是全部 429：

- queries=3；
- retrieved_titles=3；
- 其中一条 query 成功返回 `Adaptive Classifier-Free Guidance via Dynamic Low-Confidence Masking` 等相关标题；
- 同一次 run 中仍有 query 最终 429。

这说明匿名 Semantic Scholar 当前部分恢复，但仍不稳定。

## 4. 最新 Diffusion 结果：`data_20260428`

### 4.1 v1

v1 本轮结果：

- `learning_rate_schedule`：novel=False
- `cluster_conditioned_diffusion`：novel=True

query audit：

- `learning_rate_schedule`
  - queries=1
  - avg_query_len=8.0
  - retrieved_titles=10
- `cluster_conditioned_diffusion`
  - queries=2
  - avg_query_len=8.5
  - retrieved_titles=20

解释：Diffusion v1 本轮检索可用性较好。`cluster_conditioned_diffusion` 虽被判为 novel，但返回了 20 个标题，后续需要人工检查是否已有 pseudo-label、cluster-conditioned、self-supervised conditional diffusion 的近似工作。

### 4.2 v2

v2 本轮生成：

- `diversity_adaptive_guidance`
- platform 标记：novel=True，provisional

query audit：

- `diffusion_models`
  - queries=3
  - avg_query_len=17.3
  - retrieved_titles=0

解释：v2 生成了完整 proposal，但三个 Semantic Scholar query 都没有有效返回论文，主要受 429 影响。因此这里不能把 `novel=True` 当作严格 novelty 结论。

### 4.3 Diffusion 小结

Diffusion 结果显示：

- v1 更像独立 novelty gate；
- v2 更像 literature-informed ideation；
- v2 在检索失败时仍可 finalize idea；
- v1/v2 的 `novel=True` 语义不等价。

## 5. 最新 Energy 结果：`data_20260428`

### 5.1 v1

v1 本轮结果：

- `forecast_aware_storage_dispatch`：novel=False
- `adaptive_peak_shaving_dispatch`：novel=False

query audit：

- `adaptive_peak_shaving_dispatch`
  - queries=1
  - avg_query_len=12.0
  - energy_terms=none
  - retrieved_titles=1

解释：v1 判断较保守，但 query 领域覆盖仍然偏窄。`energy_terms=none` 说明当前 audit 词表或 query 本身没有充分捕捉 energy/power systems 术语。

### 5.2 v2

v2 本轮生成：

- `conformal_opf_reserve_activation`
- platform 标记：novel=True，provisional

query audit：

- `energy_power_systems`
  - queries=3
  - avg_query_len=20.0
  - energy_terms=demand response, electricity market, frequency regulation, n-1 security, optimal power flow, renewable integration
  - retrieved_titles=4

解释：Energy v2 本轮比第一批更好。query 覆盖了 `optimal power flow`、`N-1 security`、`renewable integration` 等关键术语，说明 prompt 和领域描述确实能引导 v2 生成更强领域 query。但返回论文仍少，且仍受 429 影响，因此 novelty 只能视为 provisional。

### 5.3 Energy 小结

Energy 结果显示：

- v2 能生成看起来合理且领域术语较强的能源电力 proposal；
- 但检索证据仍不足以支撑严格 novelty；
- v1 更保守，但 query 覆盖也可能不足；
- 横向适配不是单纯改 prompt，还需要领域 query 扩展和可靠检索后端。

## 6. 节流实验结果：`data_20260428_s2paced`

本轮尝试尽量保留原 AI-Scientist 的处理方式，只增加轻量请求治理：

- 原仓库仍使用 `backoff.expo + HTTPError retry`；
- 平台传入请求间隔和 429 冷却；
- 未修改 query 生成和 novelty 判断。

已运行两个代表性实验：

- Diffusion v1：`autodl_smoke_20260428_s2paced_v1`
- Energy v2：`autodl_smoke_20260428_s2paced_v2`

观察：

- Diffusion v1 即使每次 429 后等待 60 秒，仍持续 429。
- Energy v2 记录到 2 条 query，但两条均 429，`retrieved_titles=0`。
- 说明无 key 匿名访问已经进入较长时间窗口限制，温和节流不足以稳定解决。

这批结果记录在：

- `reports/semantic_scholar_429_retry_20260428.zh.md`
- `data_20260428_s2paced/diffusion/v1`
- `data_20260428_s2paced/energy/v2`

## 7. 备用检索源对照结果

备用检索实验记录在：

- `data_backup_search_20260428/`
- `reports/backup_search_control_20260428.zh.md`

主要观察如下。

### 7.1 Diffusion v2 是最关键样本

在 `data_20260428/diffusion/v2` 中，Semantic Scholar 对 3 条 query 的返回标题数为 0，主要原因是 429。

但备用检索显示：

- arXiv 对 3 条 query 都返回了候选文献；
- 返回标题包括 `Classifier-Free Diffusion Guidance`、`Rethinking Oversaturation in Classifier-Free Guidance via Low Frequency`、`Improving Sample Quality of Diffusion Models Using Self-Attention Guidance` 等；
- OpenAlex 对部分 query 也有返回，但相关性不如 arXiv 稳定。

这说明 Semantic Scholar 空返回不能被解释为“没有相关文献”。`diversity_adaptive_guidance` 的 novelty 仍需要进一步人工审查。

### 7.2 Energy 备用检索能补充候选，但噪声更高

Energy v1/v2 的备用检索能返回 peak shaving、battery storage、OPF、demand response、DER coordination 等候选标题。

但 OpenAlex 对长 energy query 容易返回宽泛综述或泛 smart grid 文献。arXiv 能返回一些技术相关标题，但覆盖 IEEE / power systems 主流文献仍不充分。

这说明 energy 领域更需要 source-specific query rewrite 和领域检索源补充。

### 7.3 对 novelty 判断的意义

备用检索进一步支持本实验的核心观点：

```text
检索失败或单一检索源空返回，不能作为 novelty 的强证据。
```

如果要让 novelty check 更可靠，平台应把 Semantic Scholar、OpenAlex、arXiv 等多源结果分开记录，并在 final decision 前进行相关性过滤。

### 7.4 事后独立 novelty decision

备用检索源确实没有进入原 v2 novelty decision，这是 v2 机制决定的：v2 没有 finalize 后的独立 novelty gate。

本项目额外补了一层 post-hoc multi-source novelty gate，结果记录在：

```text
data_posthoc_novelty_20260428/
```

结果如下：

- `diversity_adaptive_guidance`
  - 原 v2：`novel=True (provisional)`
  - 事后判断：`novelty_not_established`
  - 原因：arXiv 返回多个 classifier-free guidance、oversaturation、guidance perturbation 相关候选。
- `conformal_opf_reserve_activation`
  - 原 v2：`novel=True (provisional)`
  - 事后判断：`novelty_not_established`
  - 原因：备用源返回 OPF、renewable uncertainty、demand response、DER coordination 等相邻候选，但标题级证据不足以确认 strict novelty。

这不是证明两者一定不 novel，而是说明现有多源证据不足以接受 strong novel。

## 8. 当前结论

### 结论 1：不能只看最终 novel 字段

`novel=True/False` 必须结合 query 和检索结果解释。尤其是检索失败时，`novel=True` 不能视为可靠证据。

### 结论 2：v1 与 v2 的 novelty 语义不同

v1 有更明确的 novelty check。v2 的 search 是 ideation 内部工具，finalized idea 更像“经过文献启发的 proposal”，不是独立 novelty gate 输出。

更具体的代码证据见：

```text
reports/v2_empty_literature_behavior.zh.md
reports/v2_ideation_and_novelty_mechanism.zh.md
```

### 结论 2.5：备用源可以进入独立 novelty gate，但不能直接替代人工判读

本次新增的 post-hoc decision 显示：当把 OpenAlex / arXiv 备用结果纳入证据后，两个 v2 idea 都不应直接接受为 strong novel，而应降级为：

```text
novelty_not_established
needs_human_review_before_accepting_novelty
```

这不是证明它们一定不 novel，而是说明现有证据不足以确认 novel。

### 结论 3：429 是系统性风险

Semantic Scholar 429 不只是运行故障，也是 novelty-check pipeline 的脆弱点。当前 v2 在检索失败时仍可 finalize idea，这正是需要审计的风险。

### 结论 4：能源领域横向适配仍然不足

Energy v2 的 query 已能覆盖部分 power systems 术语，但证据仍少。Energy v1 的 query 覆盖也偏窄。跨领域适配需要领域术语扩展、检索 query 重写、后端冗余和独立 novelty gate。

### 结论 5：query audit 是必要模块

如果没有 `novelty_events.jsonl` 和 `query_audit.json`，无法区分：

- 真正没有相关工作；
- query 没搜到相关工作；
- 检索 API 失败；
- LLM 在证据不足时仍然给出自信 proposal。

## 9. 当前限制

- 样本量仍是 smoke run，不能给出统计结论。
- 未配置 `S2_API_KEY`，429 对结果影响显著。
- v2 尚无独立 novelty gate。
- Energy audit 词表仍需扩充。
- 当前比较主要基于标题和 query 层面，尚未做人类专家级 novelty 判读。

## 10. 下一步建议

1. 配置 `S2_API_KEY` 后重跑同样配置。
2. 给 v2 增加 finalize 后的独立 novelty gate。
3. 增加本地 query 缓存，避免重复 query 触发 429。
4. 为 Energy 增加领域同义词扩展，例如：
   - service restoration；
   - repair crew dispatch；
   - feeder reconfiguration；
   - DER coordination；
   - non-wires alternatives；
   - voltage stability；
   - unit commitment。
5. 构造 oracle non-novel idea benchmark，用已知重复 idea 检测 false novel。

## 11. 总结

当前最新结果进一步支持初始判断：

```text
AI-Scientist 的 novelty 判断不能脱离 query 和检索证据单独解释。
```

v1 在检索成功时更像可审计的 novelty gate；v2 能生成更完整 proposal，但当检索失败或证据不足时仍可能 finalize idea。对 diffusion 这种近域任务，这个风险已经可见；对 energy/power systems 这种跨领域任务，风险更明显，因为领域术语覆盖、检索稳定性和 novelty gate 都更脆弱。
