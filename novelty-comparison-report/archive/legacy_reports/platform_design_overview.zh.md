# 两个 Novelty Platform 的设计说明

本文档用于在讨论交流时介绍本项目搭建的两个平台：

- `diffusion-novelty-platform`
- `energy-novelty-platform`

它们的核心目的不是重新实现 AI-Scientist，而是把原 AI-Scientist / AI-Scientist-v2 的前两步能力抽离出来，做成可运行、可记录、可比较的实验平台：

```text
生成 idea -> 执行 novelty check / literature search -> 记录 query 与检索证据 -> 审计 query 质量
```

## 1. 平台要解决的问题

原 AI-Scientist 会生成 idea，并尝试检查 idea 是否 novel。但这个过程里有一个关键风险：

```text
如果 LLM 生成的 literature-search query 不恰当，
或者 Semantic Scholar 检索失败，
系统可能没有发现已有相关工作，
却仍然把 idea 视为 novel。
```

因此，本平台关注的不是“AI 是否能写出一个看起来不错的 idea”，而是更细地观察：

- 它提出了什么 idea；
- 它为了检查 novelty 实际搜了什么 query；
- 检索返回了哪些论文；
- query 是否覆盖领域关键词；
- 检索失败时系统是否仍然继续；
- v1 和 v2 在 novelty 语义上有什么差异。

## 2. 两个平台的区别

### 2.1 Diffusion Platform

路径：

```text
E:\PycharmProject\diffusion-novelty-platform
```

用途：

- 面向 diffusion models / generative modeling。
- 属于机器学习内部领域，和原 AI-Scientist 的默认研究语境较接近。
- 作为“近域适配”对照组。

它主要测试：

- AI-Scientist 在熟悉的 ML 领域中能否生成合理 idea；
- novelty query 是否能覆盖 diffusion 相关术语；
- v1/v2 在同一个 ML 方向下的检索行为差异。

### 2.2 Energy Platform

路径：

```text
E:\PycharmProject\energy-novelty-platform
```

用途：

- 面向 energy and power systems。
- 涉及 optimal power flow、storage dispatch、demand response、grid resilience、microgrid、electricity markets 等电力系统概念。
- 作为“跨领域适配”测试组。

它主要测试：

- AI-Scientist 是否能横向迁移到非传统 ML 领域；
- 生成的 idea 是否真正使用能源电力语境；
- query 是否覆盖 power systems 术语，而不是只停留在泛化的 ML 词汇；
- novelty 判断是否会因为领域术语不足而出现虚假安全感。

## 3. 和原 AI-Scientist 的关系

两个 platform 的核心原则是：

```text
原 AI-Scientist 负责生成和判断；
platform 负责指定领域、启动流程、收集证据、整理比较。
```

也就是说，大部分 idea generation 和 novelty / literature search 逻辑仍然来自：

- `AI-Scientist`
- `AI-Scientist-v2`

platform 新增的是实验外壳和审计层：

- 统一 v1/v2 调用方式；
- 提供领域配置；
- 记录 query event；
- 汇总 query audit；
- 生成 v1/v2 对比结果；
- 支持 AutoDL.Art OpenAI-compatible API；
- 支持分开运行 v1/v2，避免互相卡住。

这使得实验结果更接近“观察原系统行为”，而不是评估一个完全重写的新系统。

## 4. 目录结构与作用

两个平台结构基本一致。下面以通用结构说明。

### 4.1 `configs/`

作用：保存运行配置。

典型文件：

```text
configs/autodl.smoke.json
configs/local.example.json
```

包含内容：

- 原 AI-Scientist v1 路径；
- 原 AI-Scientist-v2 路径；
- 使用的模型；
- OpenAI-compatible base URL；
- timeout / retry 设置；
- 最大 idea 数；
- v2 reflection 数；
- novelty check 最大轮数；
- Semantic Scholar 节流设置。

它决定一次实验怎么跑。

### 4.2 `workshops/`

作用：为 AI-Scientist-v2 提供研究方向描述。

Diffusion 示例：

```text
workshops/diffusion_models.md
```

Energy 示例：

```text
workshops/energy_power_systems.md
```

这些 markdown 文件描述：

- 研究主题；
- 关键词；
- 目标领域；
- 应该关注的相关文献方向；
- novelty search 时应包含的领域术语。

对于 v2 来说，这部分相当于“研究 workshop prompt”。修改这里可以引导 v2 生成不同领域的 idea。

### 4.3 `templates/`

主要存在于 energy 平台：

```text
energy-novelty-platform/templates/ai_scientist_v1_energy_power_systems
```

作用：为 AI-Scientist v1 提供一个可识别的实验模板。

其中包含：

- `experiment.py`
  - 简化的能源电力实验 scaffold。
- `prompt.json`
  - v1 用来理解任务的 prompt。
- `seed_ideas.json`
  - 初始 idea 或对照 idea。

因为 v1 更依赖实验模板结构，所以跨到 energy 领域时，需要单独提供 v1 template。

Diffusion 平台则更多复用原 AI-Scientist 的 `2d_diffusion` 模板，因此改动较少。

### 4.4 `adapters/`

路径示例：

```text
novelty_platform/adapters/
energy_novelty_platform/adapters/
```

作用：把原 AI-Scientist v1/v2 包装成统一接口。

核心接口：

```python
generate_ideas(...)
check_novelty(...)
```

主要文件：

- `ai_scientist_v1.py`
  - 调用 AI-Scientist v1 的 idea generation 和 novelty check。
  - 读取 v1 输出的 `ideas.json`。
  - 收集 v1 novelty events。
- `ai_scientist_v2.py`
  - 调用 AI-Scientist-v2 的 ideation 流程。
  - 读取 v2 生成的 workshop json。
  - 收集 v2 literature search events。
- `base.py`
  - 定义适配器的共同接口。

adapter 的意义是屏蔽 v1/v2 原始代码结构差异，让平台可以用同一套 CLI 管理两个版本。

### 4.5 `cli.py`

作用：平台的命令行入口。

支持三个命令：

```text
init-run
audit-queries
compare-runs
```

#### `init-run`

完整运行一次实验：

```text
生成 idea -> check novelty / literature search -> 保存结果
```

支持：

```text
--only v1
--only v2
--only all
```

分开跑 v1/v2 的原因是：

- v2 literature search 更容易连续触发 429；
- 两个版本一起跑时，一个版本卡住会影响另一个版本；
- 分开跑更容易定位问题和保存中间结果。

#### `audit-queries`

读取 `novelty_events.jsonl`，生成 `query_audit.json`。

它会统计：

- query 数量；
- 平均 query 长度；
- 重复 query 比例；
- 返回论文标题；
- energy 平台中还会统计领域术语覆盖。

#### `compare-runs`

对比 v1/v2：

- v1 decisions；
- v2 decisions；
- v1 query audit；
- v2 query audit。

输出：

```text
comparison.json
comparison.md
```

中文版本目前整理在 report 仓库中。

### 4.6 `schemas.py`

作用：定义统一数据结构。

典型对象包括：

- idea；
- novelty decision；
- novelty event；
- query audit。

统一 schema 的意义是：v1 和 v2 的原始输出格式不同，但进入平台后可以被放在同一套数据结构里比较。

### 4.7 `io.py`

作用：统一读写 JSON / JSONL。

主要负责：

- 写 `ideas.json`；
- 写 `novelty_decisions.json`；
- 写 `novelty_events.jsonl`；
- 读回历史结果；
- 保证文件编码为 UTF-8。

### 4.8 `evaluation.py`

作用：对 query event 做审计。

它不是重新判断 novelty，而是评价检索过程本身：

- query 是否太少；
- query 是否重复；
- query 是否返回论文；
- energy query 是否包含领域术语；
- 是否存在检索失败。

这部分是平台的核心新增价值之一，因为它把原本不可见的 literature search 过程变成了可比较证据。

### 4.9 `runs/`

作用：保存每次运行的原始结果。

每个 run 通常包含：

```text
run_config.json
ideas.json
ideas_v1.json / ideas_v2.json
novelty_decisions.json
novelty_decisions_v1.json / novelty_decisions_v2.json
novelty_events.jsonl
novelty_events_v1.jsonl / novelty_events_v2.jsonl
query_audit.json
```

其中最重要的是：

- `ideas.json`
  - 生成了什么 idea。
- `novelty_decisions.json`
  - 每个 idea 是否被判为 novel。
- `novelty_events.jsonl`
  - 实际搜了什么 query，返回了什么论文，是否报错。
- `query_audit.json`
  - 对 query 质量的汇总。

### 4.10 `benchmarks/`

作用：保存测试或对照用 idea/event。

当前主要用于：

- 放置 adversarial ideas；
- 放置 sample novelty events；
- 后续可扩展为 known non-novel benchmark。

未来可以把“已知不 novel 的 idea”放在这里，用来测试 novelty checker 是否会误判。

### 4.11 `docs/`

作用：保存平台自身说明。

例如：

- 实验设计；
- instrumentation 说明；
- 相比原 AI-Scientist 的修改记录。

energy 平台中还包含：

```text
docs/original_ai_scientist_delta.zh.md
```

用于记录相较于原 AI-Scientist 代码主要修改了什么、为什么修改。

## 5. 运行流程

一次完整运行可以理解为下面的流水线：

```text
读取 config
  -> 设置模型和 API 环境变量
  -> 选择 v1 或 v2 adapter
  -> 调用原 AI-Scientist 生成 idea
  -> 调用 novelty check / literature search
  -> 捕获 query event
  -> 写入 runs/
  -> 生成 query_audit.json
  -> 生成 v1/v2 comparison
  -> 归档到 novelty-comparison-report
```

这里最关键的是 query event logging。它把原本只存在于运行过程中的检索行为保存下来，使后续分析可以回答：

- 这个 idea 为什么被判为 novel？
- 它到底搜了什么？
- 有没有搜到相关论文？
- 如果没搜到，是因为 idea 真新，还是 query 不好，还是 API 失败？

## 6. v1 与 v2 在平台中的解释差异

### 6.1 v1

v1 的结构更接近：

```text
idea generation -> independent novelty check
```

因此 v1 的 `novel=True/False` 更接近一个独立 novelty gate 的结果。

但 v1 仍有风险：

- query 由 LLM 生成；
- query 可能不完整；
- Semantic Scholar 可能 429；
- 如果检索失败，也可能影响最终判断。

### 6.2 v2

v2 的结构更接近：

```text
literature search inside ideation -> finalized proposal
```

它会在生成 idea 的过程中主动搜索文献，但没有一个和 v1 完全对应的独立 novelty gate。

因此平台中把 v2 的 `novel=True` 解释为：

```text
provisional novel
```

也就是“生成流程产出了一个看似新的 proposal”，而不是“独立 novelty checker 已经确认 novel”。

## 7. 为什么需要 report 仓库

两个平台的 `runs/` 保存原始实验结果，但随着运行次数增多会变得分散。

因此新建了：

```text
novelty-comparison-report
```

它的作用是：

- 按批次归档结果；
- 把 diffusion 和 energy 放在同一结构下；
- 提供中文总结；
- 提供 query event 索引；
- 对比不同运行批次；
- 保留 429 节流实验记录。

当前主要批次：

- `data/`
  - 第一批 smoke run。
- `data_20260428/`
  - 2026-04-28 最新完整重跑。
- `data_20260428_s2paced/`
  - 2026-04-28 Semantic Scholar 节流实验。

## 8. 平台的主要贡献

这两个 platform 的贡献可以概括为四点。

### 8.1 把原系统变成可控实验

原 AI-Scientist 是一个完整自动科学家流程。platform 只抽取前两步：

```text
idea generation + novelty checking
```

这样实验更轻、更可重复，也更容易定位 novelty 风险。

### 8.2 把不可见的 query 过程变成可审计数据

原始输出通常只关注最终 idea 或 final decision。platform 记录：

- query；
- papers；
- error；
- round；
- checker；
- idea_name。

这让 novelty 判断可以被追溯。

### 8.3 支持 v1/v2 横向比较

v1 和 v2 的内部结构不同。platform 用 adapter 和 schema 把它们放到同一张表里比较。

这也揭示了一个关键结论：

```text
v1 的 novelty decision 和 v2 的 provisional novel 语义并不相同。
```

### 8.4 支持跨领域迁移实验

diffusion 平台测试近域迁移，energy 平台测试跨领域迁移。

这让我们能观察：

- AI-Scientist 在 ML 内部是否表现更稳定；
- 到能源电力领域后，query 是否仍然足够专业；
- prompt 适配是否足够，还是需要领域检索增强。

## 9. 当前局限

当前平台仍有局限：

- 样本量是 smoke run，不足以做统计结论；
- 未配置 Semantic Scholar API key，429 影响明显；
- v2 没有独立 novelty gate；
- energy 领域术语审计词表仍需扩充；
- query audit 只能辅助判断，不能替代专家文献审查。

## 10. 后续扩展方向

建议下一步扩展：

- 配置 `S2_API_KEY` 后重跑；
- 增加本地 query 缓存；
- 给 v2 添加 finalize 后独立 novelty check；
- 加入 OpenAlex / arXiv / Crossref 等备用检索源；
- 构造 known non-novel benchmark；
- 扩充 energy 领域同义词与任务词表；
- 增加人工标注，用于判断 query 是否真正覆盖已有工作。

## 11. 一句话介绍

这两个 platform 可以这样概括：

```text
它们是围绕 AI-Scientist v1/v2 搭建的 novelty-query 审计平台，
用于观察 idea 生成后，系统到底用什么 query 去证明 novelty，
以及当 query 不充分或检索失败时，novelty 判断是否仍然可靠。
```
