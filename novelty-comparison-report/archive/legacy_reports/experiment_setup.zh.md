# 实验设置

## 目标

本实验尝试回答一个具体问题：

```text
AI-Scientist 的 novelty check 是否可能因为 LLM 生成的 query 不恰当或检索失败，而错误地通过一个并不 novel 的 idea？
```

为了观察这个问题，我们搭建了两个平台：

- diffusion 领域平台：仍在机器学习内部，作为较接近原始 AI-Scientist 语境的对照。
- energy/power systems 领域平台：跨到能源电力领域，用于观察横向适配能力和领域术语检索问题。

## 使用的模型和接口

使用 AutoDL.Art 的 OpenAI-compatible API：

```text
base_url = https://www.autodl.art/api/v1
model = gpt-5.4
```

原 AI-Scientist 的 OpenAI client 已被补充为支持：

- `OPENAI_BASE_URL`
- `OPENAI_TIMEOUT`
- `OPENAI_MAX_RETRIES`

## Semantic Scholar

本次没有配置 `S2_API_KEY`，因此按原 AI-Scientist 的方式使用无 key Semantic Scholar 请求。

这会导致：

- 频繁 429 rate limit；
- 部分查询失败；
- query audit 中可能出现“query 发出但无返回论文”的情况。

这不是平台代码错误，而是当前实验条件的一部分。它同时也是 novelty check 的现实风险：如果检索后端失败，系统是否仍然 finalize idea？

## v1 与 v2 的关键差异

AI-Scientist v1：

- idea generation 与 novelty check 是两个相对独立步骤；
- novelty check 会多轮生成 query、调用 Semantic Scholar、再做 final decision；
- 因此 v1 的 `novel=False/True` 更接近独立 novelty gate。

AI-Scientist v2：

- literature search 嵌入 ideation 过程；
- 没有独立 novelty gate；
- 因此本报告把 v2 的 `novel=True` 记为 provisional，而不是等价于 v1 的 novelty decision。

## 本次新增 instrumentation

为了比较 query 质量，我们为 v1/v2 都增加了 query event logging：

```json
{
  "idea_name": "...",
  "checker": "ai_scientist_v1 或 ai_scientist_v2",
  "round_index": 1,
  "query": "...",
  "papers": [],
  "error": "可选，记录检索失败原因"
}
```

这些事件被整理为：

- `novelty_events.jsonl`
- `query_audit.json`

## 结果批次

当前报告仓库包含三批结果：

- `data/`
  - 第一批 smoke run，用于验证平台、日志和比较流程。
- `data_20260428/`
  - 2026-04-28 改善网络后按同一 smoke 配置重跑的完整结果。
  - 这是目前最推荐优先分析的一批。
- `data_20260428_s2paced/`
  - 2026-04-28 加入 Semantic Scholar 请求间隔和 429 冷却后的代表性测试。
  - 用于观察原仓库 backoff 结合平台层节流是否能缓解 429。
- `data_backup_search_20260428/`
  - 2026-04-28 备用检索源对照实验。
  - 复用 `data_20260428` 中已记录 query，额外调用 OpenAlex 和 arXiv。
- `data_posthoc_novelty_20260428/`
  - 2026-04-28 事后独立 novelty decision。
  - 基于 v2 finalized ideas、Semantic Scholar 结果、OpenAlex/arXiv 备用结果，给出保守证据状态。

## 2026-04-28 节流设置

为了尽量保留原 AI-Scientist 的行为，本次节流实验没有修改 query 生成、idea 生成或 novelty 判断，只增加：

```text
S2_REQUEST_INTERVAL = 12
S2_429_COOLDOWN = 60
```

观察结果显示：在未配置 `S2_API_KEY` 的情况下，温和节流仍不足以稳定解决 429。因此后续若要做更严格评估，建议优先配置 Semantic Scholar API key，或加入本地 query 缓存和备用检索源。

## 备用检索源对照

备用检索实验不改变原 AI-Scientist 的 prompt、idea generation 或 novelty decision。它只把已经记录下来的 query 发送到 OpenAlex 和 arXiv，用作对照证据。

该实验的解释原则是：

- 备用源返回相关标题，说明 Semantic Scholar 空返回或 429 不能直接视为没有相关工作。
- 备用源返回宽泛标题，说明 query 还需要 source-specific rewrite 和结果过滤。
- 备用源不能直接替代 novelty decision，只能帮助诊断检索证据是否不足。

## Post-hoc novelty decision

由于原 v2 没有 finalize 后的独立 novelty gate，本项目额外整理了一个 post-hoc multi-source novelty decision。

该步骤不改变原 v2 输出，而是新增平台层判断：

```text
original_v2_status = novel=True (provisional)
posthoc_novelty_status = novelty_not_established
decision = needs_human_review_before_accepting_novelty
```

当前 post-hoc decision 主要基于 query、标题和少量元数据，因此采取保守策略：只要备用检索显示存在明显相关候选，就不接受原 v2 的 provisional novel 作为强 novelty 结论。
