# 02 实验方法

## 平台目标

本项目不是重新实现 AI-Scientist，而是把原 AI-Scientist v1/v2 包装成可审计平台。

平台关注的不是“能否生成一个看起来合理的 idea”，而是：

- LLM 生成了什么 query；
- query 是否覆盖目标领域；
- 检索源返回了哪些论文；
- 是否发生 429 或空结果；
- 最终 novelty 判断是否有足够证据支撑。

## 版本对比

### v1

v1 使用原仓库中的 `check_idea_novelty` 风格流程：

```text
生成 idea
  -> LLM 生成检索 query
  -> Semantic Scholar 返回 top 10 papers with abstracts
  -> LLM 判断 significant overlap
  -> 写入 novel true/false
```

v1 的判断依据不仅是标题。原仓库会把以下字段传给 LLM：

- title
- authors
- venue
- year
- citation count
- abstract

### v2

v2 使用 action/tool loop：

```text
LLM 输出 ACTION:
  SearchSemanticScholar
或
  FinalizeIdea
```

是否继续 search、是否 finalize，主要由 LLM 在当前轮输出的 `ACTION` 决定。代码没有强制要求：

- 至少成功检索到 N 篇论文；
- 所有 query 不得失败；
- 文献为空时禁止 finalize；
- evidence 不足时输出 unknown。

因此 v2 的结果需要被解释为 proposal generation 结果，而不是独立 novelty decision。

## 实验批次

### `data/`

第一批 smoke run，用于验证平台、日志和对比流程。

### `data_20260428/`

当前最重要的主结果。包含 diffusion 和 energy 两个平台的 v1/v2 分开运行结果。

配置特点：

- AutoDL.Art OpenAI-compatible API；
- `model=gpt-5.4`；
- 未配置 `S2_API_KEY`；
- smoke 配置；
- v1/v2 分别运行。

### `data_20260428_s2paced/`

Semantic Scholar 429 节流测试。

新增：

- `S2_REQUEST_INTERVAL=12`
- `S2_429_COOLDOWN=60`

结果显示，在无 API key 的情况下，温和节流仍不能稳定解除 429。

### `data_backup_search_20260428/`

备用检索源对照。复用已经记录的 query，额外查询：

- OpenAlex
- arXiv

目的：判断 Semantic Scholar 空返回是否等价于没有相关文献。

### `data_posthoc_novelty_20260428/`

事后独立 novelty decision。它不改变原 v2 输出，而是在多源证据基础上给出更谨慎的判断。

### `data_semantic_scholar_probe_20260429/`

2026-04-29 对 Semantic Scholar 匿名访问状态的探测。

diffusion v2 有一条 query 成功返回 3 篇标题，但同一轮仍有 query 429。energy v2 同日临时探测全部 429，因此未归档。

## 记录字段

### `novelty_events.jsonl`

逐条记录检索事件：

- idea name；
- checker；
- round index；
- query；
- returned papers；
- error。

这是判断“文献为空”到底是检索不到、query 不佳还是 API 失败的核心文件。

### `query_audit.json`

从 `novelty_events.jsonl` 汇总而来：

- `num_queries`
- `avg_query_len`
- `repeated_query_fraction`
- `retrieved_titles`
- energy 平台额外包含 `energy_terms_covered`

注意：`retrieved_titles` 只是审计摘要，不代表原 AI-Scientist 只看标题。

### `novelty_decisions.json`

统一记录平台输出。对 v2 来说，`is_novel=true` 是 provisional 标记，不是原仓库独立 novelty 布尔标签。

## 方法限制

- 当前样本量是 smoke run，不适合做统计结论。
- 无 Semantic Scholar API key，429 对结果影响很大。
- Energy template 和 audit 词表是手工构造的轻量材料，不是经过领域验证的 benchmark。
- 多数判断仍基于 query、标题和摘要，没有进行全文专家审稿。
