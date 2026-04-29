# 07 GitHub 上传说明

## 上传范围

只需要上传整个 `novelty-comparison-report` 目录。

不需要上传：

```text
AI-Scientist/
AI-Scientist-v2/
diffusion-novelty-platform/
energy-novelty-platform/
```

本仓库已经包含整理后的报告、实验结果、备用检索结果和归档材料。

## 建议保留的目录

建议保留以下内容：

```text
README.md
.gitattributes
.gitignore
docs/
data/
data_20260428/
data_20260428_s2paced/
data_backup_search_20260428/
data_posthoc_novelty_20260428/
data_semantic_scholar_probe_20260429/
archive/
tools/
```

其中：

- `docs/` 是主阅读路径；
- `data_20260428/` 是当前主实验结果；
- `data_backup_search_20260428/` 是备用检索源对照；
- `data_posthoc_novelty_20260428/` 是事后 novelty decision；
- `data_semantic_scholar_probe_20260429/` 是最新 Semantic Scholar 探测；
- `archive/legacy_reports/` 是旧版长报告归档。

## 手动提交命令

如果你还没有连接远程 GitHub 仓库，可以执行：

```powershell
cd E:\PycharmProject\novelty-comparison-report
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main
```

如果你后续又修改了文件，可以手动提交：

```powershell
cd E:\PycharmProject\novelty-comparison-report
git status
git add .
git commit -m "Update novelty audit report"
git push
```

## 上传前检查

建议上传前确认：

```powershell
git status
```

如果看到未提交文件，再决定是否 `git add` 和 `git commit`。

也可以检查是否误放入缓存文件：

```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__
```

当前 `.gitignore` 已忽略：

```text
__pycache__/
*.py[cod]
.DS_Store
Thumbs.db
```

## 关于旧报告路径

旧的 `reports/` 目录已经整理到：

```text
archive/legacy_reports/
```

如果 IDE 里还开着旧路径文件，可能需要重新从 `archive/legacy_reports/` 或 `docs/` 打开。

GitHub 首页建议读者从 `README.md` 开始，再按 `docs/01` 到 `docs/07` 顺序阅读。
