# AI 提效工具箱

> 收录课程中提到的「AI 提效小工具」：每个工具 = 脚本 + 生成它的原始 Prompt + 使用说明。
> 脚本统一存放在仓库 `tools/` 目录，本页为总索引。

| 工具 ID | 名称 | 解决什么问题 | 所属模块小节 | 脚本位置 |
|---------|------|-------------|-------------|---------|
| TOOL-emmx2md | 思维导图 TXT 转 MD（XMind 导入） | 亿图导出的 Tab 缩进 TXT → XMind 可导入的 Markdown 大纲，零丢字保真校验 | [M3 第九节](modules/03-testcase-generation/lecture.md) | [tools/emmx-to-md/](https://github.com/JennyHasACat/AITestingTraining/tree/main/tools/emmx-to-md) |

## 工具登记规范（维护者）

1. 每个工具一个语义 ID（`TOOL-xxx`，不用序号），目录名 = ID 后缀；
2. 仓库根 `tools/<tool-id>/` 下固定三件套：脚本本体、`prompt.md`（生成它的原始 Prompt）、`README.md`（用途 / 用法 / 边界）；
3. 入课走「喵喵喵加肉-工具」：登记本页索引 + 对应模块 `lecture.md` 追加选学小节（10 min，不计入模块总时长）；
4. 三者一致性（`tools/` ↔ 本页 ↔ 课件小节）由「喵喵喵培训自检」第 ⑦ 项护栏保障；
5. 公开 / 私有策略：纯通用工具公开入库；含敏感实现的只在本页写「思路 + 伪步骤」，脚本留私有仓库。
