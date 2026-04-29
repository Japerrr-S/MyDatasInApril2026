# Backup Search Control：2026-04-28

本目录保存备用检索源对照实验结果。

## 实验设计

本实验不重新生成 idea，也不重新运行 AI-Scientist 的 novelty decision。它只复用 `data_20260428` 中已经记录的 query，额外调用两个备用检索源：

- OpenAlex
- arXiv

目标是观察：

```text
当 Semantic Scholar 429 或返回不足时，同一个 query 在备用检索源中是否还能找到候选文献。
```

## 目录结构

```text
diffusion/
  v1/
  v2/
energy/
  v1/
  v2/
```

每个目录包含：

- `backup_search_events.jsonl`
  - 原始备用检索事件。
- `backup_search_audit.json`
  - 每条 query 在各备用源中的返回标题汇总。

## 解释注意

备用检索结果不能直接证明 novelty 或 non-novelty。它们的作用是提供对照证据：

- 如果 Semantic Scholar 因 429 失败，而 arXiv/OpenAlex 能返回相关标题，说明“无返回”不能解释为“无相关文献”。
- 如果 OpenAlex 返回很宽泛或明显偏题的标题，说明备用检索源也需要 query 重写、过滤和排序。
- 如果 arXiv 返回高度相关标题，说明对 ML/diffusion 类 query，arXiv 可作为有用补充。
