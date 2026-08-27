# tools/ — AI 提效小工具资产库（维护者视角）

每个子目录是一个工具，目录名 = 工具 ID 后缀（语义 ID，风格 `TOOL-xxx`，不用序号）。

## 固定三件套

- 脚本本体（如 `emmx_to_md.py`）
- `prompt.md` — 生成该脚本的原始 Prompt 原文（溯源，后续迭代可复现）
- `README.md` — 用途 / 用法 / 边界（课件小节的素材来源）

## 关联约定

- 学员可见的站点索引：`docs/toolbox.md`（AI 提效工具箱）
- 入课流程：`.codebuddy/rules/training-content-add-flesh.mdc`「喵喵喵加肉-工具」分支
- 一致性护栏：`training-content-consistency.mdc` 第 ⑦ 项（tools/ ↔ toolbox.md ↔ 课件小节三者一致 + TOOL- 编号唯一）
- 公开/私有默认策略：纯通用工具、无公司信息即可公开入库；含敏感实现的只在索引写「思路 + 伪步骤」，脚本留私有仓库
