# 03 平台构成

## 设计目标

两个平台的目标不是替代原仓库，而是让原 AI-Scientist 的 novelty 行为可观察、可比较、可归档。

平台新增的能力包括：

- 统一运行 v1/v2；
- 记录每条 query；
- 记录检索返回和错误；
- 汇总 query audit；
- 归档 comparison；
- 支持备用检索源；
- 支持 post-hoc novelty decision。

## Diffusion 平台

仓库：

```text
diffusion-novelty-platform/
```

作用：

- 近域测试；
- diffusion 仍属于 AI/ML；
- 主要观察原 AI-Scientist 在熟悉语境下的 query 和 novelty 行为。

Diffusion 平台基本复用原 AI-Scientist 的 diffusion template，修改较少。

## Energy 平台

仓库：

```text
energy-novelty-platform/
```

作用：

- 跨领域测试；
- 研究方向改成 energy / power systems；
- 观察 AI-Scientist 是否能生成领域化 query。

### Energy template 来源

Energy template 不是原 AI-Scientist 自带，也不是某个专业开源 benchmark。它是本项目手工构造的轻量 starter template。

位置：

```text
energy-novelty-platform/templates/ai_scientist_v1_energy_power_systems/
energy-novelty-platform/workshops/energy_power_systems.md
```

它覆盖了一些常见 power systems 方向：

- optimal power flow；
- unit commitment；
- economic dispatch；
- demand response；
- renewable integration；
- energy storage；
- electricity markets；
- voltage stability；
- frequency regulation；
- grid resilience。

这个 template 足够用于初步跨领域压力测试，但不够作为严格能源电力科研 benchmark。

如果要提高专业性，建议未来基于真实开源电力系统环境构建：

- MATPOWER / PYPOWER；
- PGLib-OPF；
- RTS-GMLC；
- Grid2Op；
- pandapower；
- PowerModels.jl；
- UnitCommitment.jl。

## Audit 词表

Energy 平台额外有一个 audit 词表：

```text
energy-novelty-platform/energy_novelty_platform/evaluation.py
```

当前包含：

```text
optimal power flow
unit commitment
economic dispatch
demand response
voltage stability
frequency regulation
renewable integration
distributed energy resources
microgrid
electricity market
energy storage
load forecasting
n-1 security
```

这个词表不参与 v2 决策，也不会影响 LLM 输出。它只是平台层的事后审计工具，用来判断 query 是否显式覆盖 power systems 术语。

因此：

```text
energy_terms=none
```

不等于 query 一定不专业，只表示没有命中当前手写词表。当前词表仍偏窄，需要扩展。

## 为什么要加 audit

原 AI-Scientist 关心的是生成 idea 和执行检索。我们关心的是：

```text
它到底有没有用目标领域的语言去检索？
```

例如 energy idea 如果只搜：

```text
uncertainty neural network control learning
```

而没有搜：

```text
optimal power flow
N-1 security
demand response
reserve scheduling
```

就可能漏掉关键电力系统文献。

Audit 词表的作用是把这种风险显性化。

## 运行与归档

平台运行后会生成：

- `ideas.json`
- `novelty_decisions.json`
- `novelty_events.jsonl`
- `query_audit.json`
- `run_config.json`

结果随后复制到 `novelty-comparison-report/` 中统一归档。
