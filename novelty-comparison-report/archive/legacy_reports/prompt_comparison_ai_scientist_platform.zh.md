# 原 AI-Scientist 与 Platform Prompt 对比说明

本文档用于说明：原 AI-Scientist / AI-Scientist-v2 中哪些 prompt 决定 idea generation 与 novelty check，两个 platform 又通过哪些 prompt 或领域描述改变研究方向。重点是展示 prompt 在本实验中的作用。

## 1. 总体结论

两个 platform 并没有重写 AI-Scientist 的核心 LLM 推理流程。它们主要通过三类 prompt/context 影响系统行为：

1. v1 的 `prompt.json`
   - 决定 AI-Scientist v1 看到的实验任务是什么。
   - 包含 `system` 和 `task_description`。
2. v1 内置的 idea / novelty prompt 模板
   - 决定 v1 如何生成 idea、如何反思、如何生成 Semantic Scholar query、如何做 novelty decision。
   - 这部分主要保留原仓库逻辑。
3. v2 的 workshop markdown
   - 决定 AI-Scientist-v2 的 proposal 主题、关键词和文献检索方向。
   - diffusion / energy platform 主要通过这里改变 v2 的研究领域。

因此，platform 中 prompt 的作用可以概括为：

```text
原仓库 prompt 决定“怎么思考”；
platform 领域 prompt 决定“围绕什么领域思考、用什么领域词汇搜索”。
```

## 2. AI-Scientist v1 的 Prompt 结构

### 2.1 原始 v1 diffusion template

文件：

```text
AI-Scientist/templates/2d_diffusion/prompt.json
```

核心内容：

- `system`
  - 角色设定为想发表重要论文的 AI PhD student。
- `task_description`
  - 指定任务是低维 diffusion model。
  - 明确模型基于 DDPM。
  - 提示 controllable generation、mode bias、新 encoding 等方向可能有趣。

作用：

- 这是 v1 idea generation 的领域入口。
- LLM 并不是“自由发明任何方向”，而是在这个 task description 和 `experiment.py` 的代码上下文下提出可实现 idea。
- 因此原 diffusion 任务天然更容易产生 ML/diffusion 方向 idea。

### 2.2 v1 idea generation prompt 模板

文件：

```text
AI-Scientist/ai_scientist/generate_ideas.py
```

相关模板：

```text
idea_first_prompt
idea_reflection_prompt
```

其核心要求包括：

- 给出 `task_description`；
- 给出完整 `experiment.py`；
- 给出已有 idea 列表；
- 要求提出下一个有影响力、创新、可通过现有代码验证的 idea；
- 要求输出固定 JSON 字段：
  - `Name`
  - `Title`
  - `Experiment`
  - `Interestingness`
  - `Feasibility`
  - `Novelty`

作用：

- 约束 idea 必须可在现有代码中实现。
- 使 idea 更像“实验改动方案”，而不是纯理论 proposal。
- 评分字段会诱导模型显式考虑 interestingness、feasibility、novelty。

这解释了为什么 v1 输出通常较短、更像实验计划，而 v2 输出更像完整 proposal。

### 2.3 v1 novelty prompt 模板

文件：

```text
AI-Scientist/ai_scientist/generate_ideas.py
```

相关模板：

```text
novelty_system_msg
novelty_prompt
```

核心逻辑：

- 角色设定为严格检查 novelty 的 AI PhD student。
- 要求使用 Semantic Scholar survey literature。
- 每轮可以：
  - 生成一个 query；
  - 或提前决定 novel / not novel。
- 如果找到显著重叠论文，应判为 not novel。
- 如果经过充分搜索没有找到显著重叠论文，才判为 novel。

输出格式要求：

```json
{
  "Query": "..."
}
```

作用：

- v1 的 novelty check 是一个独立阶段。
- query 是由 LLM 根据当前 idea 和上一轮检索结果生成的。
- 这正是本实验关注的风险点：如果 LLM 生成的 query 不充分，novelty decision 就可能建立在不完整证据上。

## 3. Energy Platform 对 v1 Prompt 的修改

文件：

```text
energy-novelty-platform/templates/ai_scientist_v1_energy_power_systems/prompt.json
```

相比原 `2d_diffusion/prompt.json`，energy platform 修改了两部分。

### 3.1 system prompt

从泛化的 AI PhD student 改为能源系统、电力系统、优化、控制和机器学习方向的 expert researcher。

作用：

- 把模型角色从通用 ML 研究者转向 energy/power systems 研究者。
- 提醒模型不能只用泛化 ML 术语思考。
- 要求 idea 对 power-system operation、planning、markets、reliability、resilience 有意义。

### 3.2 task description

从低维 DDPM 任务改成轻量能源电力仿真 scaffold。

明确列出方向：

- optimal power flow；
- unit commitment；
- economic dispatch；
- demand response；
- renewable integration；
- microgrid control；
- energy storage；
- electricity markets；
- voltage stability；
- frequency regulation；
- grid resilience。

作用：

- 直接决定 v1 生成 idea 的领域。
- 让 v1 的 idea 从 diffusion 实验改动，转向能源电力实验改动。
- 但 v1 的 novelty prompt 模板本身仍然是原来的，所以 query 生成机制没有本质变化。

## 4. Diffusion Platform 对 v1 Prompt 的处理

diffusion platform 基本复用原 AI-Scientist 的 `2d_diffusion` template。

原因：

- diffusion 本身仍属于机器学习研究；
- 原仓库已有 `2d_diffusion` prompt 和实验代码；
- 不需要像 energy 那样新建完整 v1 template。

因此 diffusion platform 对 v1 prompt 的改动较少，更多是在 platform 层增加：

- 统一运行入口；
- query logging；
- query audit；
- v1/v2 comparison。

这也说明 diffusion platform 是近域适配，而 energy platform 是跨领域适配。

## 5. AI-Scientist-v2 的 Prompt 结构

文件：

```text
AI-Scientist-v2/ai_scientist/perform_ideation_temp_free.py
```

v2 的 prompt 结构和 v1 很不同。它更像 tool-using proposal generator。

### 5.1 v2 system prompt

核心要求：

- 生成高影响力 research ideas；
- proposal 要像 grant proposal；
- 要 novel；
- 要和 existing literature 区分；
- 资源需求不能超过 academic lab；
- 目标倾向 top ML conferences。

这部分是原 v2 自带逻辑，platform 没有重写。

作用：

- 让 v2 输出比 v1 更完整、更抽象、更 proposal-like。
- 强调 related work 和 novelty，但并不等价于独立 novelty gate。

### 5.2 v2 tools prompt

v2 暴露两个核心动作：

```text
SearchSemanticScholar
FinalizeIdea
```

模型必须用类似下面的格式回应：

```text
ACTION:
SearchSemanticScholar 或 FinalizeIdea

ARGUMENTS:
对应 JSON
```

作用：

- literature search 被嵌入 ideation 过程。
- 模型可以先搜索，再根据结果 refine proposal，最后 finalize。
- 但如果搜索失败，模型仍可能继续 finalize。

这就是 v2 与 v1 的关键差异：v2 的 search 是 ideation 工具，不是独立 novelty gate。

### 5.3 v2 idea_generation_prompt

v2 的初始 user prompt 会插入：

```text
{workshop_description}
```

也就是说，platform 通过 workshop markdown 决定 v2 研究方向。

## 6. Platform 为 v2 新增的 Workshop Prompt

### 6.1 Diffusion workshop

文件：

```text
diffusion-novelty-platform/workshops/diffusion_models.md
```

核心内容：

- 标题：Novel Research Ideas for Diffusion Models。
- 关键词：
  - diffusion models；
  - denoising；
  - score matching；
  - sampling；
  - generative modeling；
  - guidance；
  - mode coverage；
  - efficiency；
  - low-dimensional diffusion。
- 要求 proposal 关注：
  - sampling efficiency；
  - denoiser architecture；
  - guidance；
  - mode coverage；
  - uncertainty；
  - training objectives；
  - evaluation。
- 明确提醒 novelty search 要同时使用 generic ML phrasing 和 diffusion-specific terminology。

作用：

- 将 v2 的泛化 proposal generator 限定到 diffusion/generative modeling。
- 引导 query 包含 diffusion-specific terms。
- 使 v2 的 idea 更接近 diffusion 研究问题。

### 6.2 Energy workshop

文件：

```text
energy-novelty-platform/workshops/energy_power_systems.md
```

核心内容：

- 标题：Novel AI-Assisted Research Ideas for Energy and Power Systems。
- 关键词：
  - power systems；
  - smart grid；
  - renewable integration；
  - energy storage；
  - demand response；
  - electricity markets；
  - grid resilience；
  - optimal power flow；
  - forecasting；
  - control；
  - uncertainty。
- 明确要求：
  - idea 应该按 power-systems literature 评估，而不只是 ML literature；
  - contribution 应该体现 energy-system value、operational constraints、reliability、economics、deployability；
  - literature search 应包含 OPF、unit commitment、economic dispatch、N-1 security、voltage stability、DER coordination、virtual power plants、frequency regulation、demand response 等术语。

作用：

- 把 v2 从 top-ML-conference 默认语境拉向 energy/power systems。
- 明确告诉模型：不要只用机器学习术语检索。
- 直接影响本轮 energy v2 中 query 的术语覆盖，例如出现 `optimal power flow`、`N-1 security`、`renewable integration`。

## 7. Prompt 对实验结果的影响

### 7.1 Prompt 决定 idea 的研究方向

原 v1 `2d_diffusion/prompt.json` 会自然生成 diffusion 相关 idea，例如 mode control、cluster conditioning、learning rate schedule。

energy v1 `prompt.json` 则引导模型生成 storage dispatch、peak shaving、feeder stress 等能源方向 idea。

v2 的 workshop markdown 更明显：diffusion workshop 生成 guidance/diversity/sampling 类 proposal；energy workshop 生成 OPF、reserve、flexibility、market、grid operation 类 proposal。

### 7.2 Prompt 决定 query 的词汇空间

query 不是随机出现的，而是受 prompt 中关键词影响。

例如 energy workshop 明确列出：

- optimal power flow；
- N-1 security；
- frequency regulation；
- demand response；
- renewable integration。

因此最新 energy v2 的 query audit 中确实出现了这些术语覆盖。

这说明 prompt 对 query 质量有直接作用。

### 7.3 Prompt 不能保证检索充分

即使 prompt 写明了领域术语，也不能保证 novelty check 可靠。

原因包括：

- LLM 可能只选择部分术语；
- query 可能过宽或过窄；
- Semantic Scholar 可能 429；
- v2 搜索失败后仍可能 finalize；
- prompt 无法替代真正的多 query 检索策略和独立 novelty gate。

因此 prompt 是必要条件，但不是充分条件。

## 8. 原仓库 Prompt 与 Platform Prompt 的对比表

| 位置 | 原仓库作用 | Platform 改动 | 对结果的影响 |
|---|---|---|---|
| v1 `prompt.json` | 定义任务领域和角色 | energy 新增 power systems template；diffusion 基本复用原 template | 决定 v1 idea 的领域 |
| v1 `idea_first_prompt` | 要求基于代码生成可实验 idea | 基本保留 | 保持原 v1 idea 生成机制 |
| v1 `idea_reflection_prompt` | 多轮改进 idea | 基本保留 | 保持原 v1 reflection 行为 |
| v1 `novelty_system_msg` | 要求严格检查 novelty 并使用 Semantic Scholar | 基本保留，只补 query logging | 保持原 novelty gate 语义 |
| v1 `novelty_prompt` | 要求每轮给出 query 或 decision | 基本保留 | query 仍由 LLM 自行归纳 |
| v2 `system_prompt` | 生成 high-impact grant-like proposal | 基本保留 | v2 输出更完整、更 proposal-like |
| v2 tool prompt | 允许 SearchSemanticScholar / FinalizeIdea | 基本保留，只补日志与 parser 兼容 | search 嵌入 ideation，不是独立 gate |
| v2 workshop description | 原 v2 的领域输入入口 | diffusion / energy 分别新增 workshop markdown | 决定 v2 idea 和 query 的领域方向 |

## 9. 用于展示的核心观点

对外交流时，可以把 prompt 的作用分成三层：

### 第一层：领域选择

prompt 告诉系统“研究什么领域”。例如：

- diffusion prompt 让模型围绕 diffusion model、guidance、sampling、mode coverage；
- energy prompt 让模型围绕 OPF、storage、demand response、grid resilience。

### 第二层：输出形态

prompt 告诉系统“输出什么形式”。

- v1 输出实验型 JSON idea；
- v2 输出 grant-proposal-like idea；
- novelty prompt 输出 query 或 decision。

### 第三层：证据路径

prompt 告诉系统“应该如何寻找 novelty 证据”。

- v1 novelty prompt 要求 query Semantic Scholar；
- v2 tool prompt 要求至少一次 literature search；
- energy workshop 要求使用 power-systems terminology。

但这层也是最脆弱的：prompt 可以要求 search，却不能保证 search 一定充分、API 一定成功、LLM 一定选择正确 query。

## 10. 对本实验的意义

本实验通过 platform 暴露了一个关键事实：

```text
prompt 确实能显著改变 idea 方向和 query 词汇，
但 prompt 本身不能保证 novelty check 完全可靠。
```

也就是说，prompt 对系统行为有强影响：

- 决定生成 diffusion 还是 energy idea；
- 决定 query 更像 ML 术语还是 power systems 术语；
- 决定输出是短实验计划还是完整 proposal。

但 novelty 可靠性还需要额外机制：

- query logging；
- query audit；
- 多 query 扩展；
- 检索缓存；
- 稳定检索后端；
- 独立 novelty gate；
- 人工或 oracle benchmark 验证。

因此，本平台的价值正是在 prompt 之外增加了证据层，让我们能观察 prompt 产生的 query 是否真的支撑 novelty 判断。
