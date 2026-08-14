# AITestingTraining（仓库维护者说明）

> 本文件是 **GitHub 仓库首页**，面向**维护者 / 培训组织者 / 协作者**。  
> 学员请访问已发布的课程站：https://JennyHasACat.github.io/AITestingTraining/  
> 课程正文在 `docs/` 目录，由 MkDocs 构建，**不在此 README**。

---

## 🔧 自动部署链路

本站点采用 **推 `main` 即自动发布** 模式，无需手动构建部署：

```
┌─────────────┐
│  本地 commit │  (git commit)
└──────┬──────┘
       │  git push origin main
       ▼
┌─────────────────────────────────────────────┐
│            GitHub (main 分支更新)              │
└──────────────────────┬──────────────────────┘
                       │ 触发 webhook
                       ▼
┌─────────────────────────────────────────────┐
│        GitHub Actions  (.github/workflows/    │
│                       deploy.yml)             │
│                                               │
│   1. checkout 代码                            │
│   2. 安装 Python + mkdocs / mkdocs-material    │
│   3. mkdocs build  (把 .md 构建成静态站点)     │
│   4. mkdocs gh-deploy --force                  │
│        └─▶ 推到 gh-pages 分支                  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│   gh-pages 分支  (GitHub Pages 发布源)         │
└──────────────────────┬──────────────────────┘
                       │  自动发布
                       ▼
        ┌──────────────────────────┐
        │  https://Jennyhasacat.    │
        │  github.io/AITesting      │
        │  Training/   (站点上线)    │
        └──────────────────────────┘
```

要点：维护者只需执行最上面的 `commit + push` 两步，下面整条（Actions 构建 → gh-pages → Pages 上线）全部由 GitHub 按既定工作流自动完成，**无需手动触发任何部署命令**。

---

## 💻 本地预览（不发布）

改完 `docs/` 下的内容想先看效果，无需推送：

```bash
pip install mkdocs mkdocs-material
mkdocs serve          # 打开 http://127.0.0.1:8000 本地预览
```

---

## 📌 提交与发布约定

- **仅 `main` 分支会触发自动发布**，请确认内容无误后再推送 `main`。
- 若远程 `main` 领先本地，用 `git pull --rebase origin main` 整合，避免强推。
- 课程正文改动请遵循 `.codebuddy/rules/training-content-consistency.mdc` 的一致性护栏。

---

*本仓库为 AI 辅助软件测试团队培训课程源码。课程内容与学习路径见已发布站点。*
