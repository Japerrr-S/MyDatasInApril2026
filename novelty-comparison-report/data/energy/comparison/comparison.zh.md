# Energy 平台 v1/v2 Query 审计对比解读

## 运行对象

- v1: `runs/autodl_smoke_v1_001`
- v2: `runs/autodl_smoke_v2_logged_001`

## 核心观察

v1 对能源模板生成/检查后，将两个 idea 都判为 `novel=False`。成功记录的 query 覆盖到的能源领域词主要是：

- `microgrid`

检索返回了 10 个标题，说明至少有一定文献证据支撑 novelty rejection。

v2 生成了 `counterfactual_restoration_probes`，平台暂记为 `novel=True (provisional)`。v2 的成功 query 也主要覆盖：

- `microgrid`

并返回 2 个标题，包括：

- `Coordinated Repair Crew Dispatch Problem for Cyber–Physical Distribution System`
- `A Parallel Fast-Track Service Restoration Strategy Relying on Sectionalized Interdependent Power-Gas Distribution Systems`

## 对横向适配的意义

能源平台的结果比 diffusion 更能说明横向适配问题：

- v2 确实能生成能源电力领域 idea；
- 但 query 的领域词覆盖仍然窄，审计只稳定检测到 `microgrid`；
- 对 `distribution restoration`、`repair crew dispatch`、`intentional islanding` 这类关键概念有一定命中，但当前 audit 词表还需要扩充；
- v2 的 final idea 中 Related Work 写得像已经判断 novel，但实际检索证据很有限。

## 下一步建议

扩充 energy query audit 词表，例如加入：

- `distribution restoration`
- `service restoration`
- `repair crew dispatch`
- `intentional islanding`
- `feeder reconfiguration`
- `critical load restoration`
- `resilience`

同时给 v2 加独立 novelty gate，否则 v2 的 `novel=True` 只能看作 ideation 阶段的暂定结果。

