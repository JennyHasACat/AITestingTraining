# AI 提效工具箱

> 收录课程中提到的「AI 提效小工具」：每个工具 = 生成它的原始 Prompt + 使用说明（脚本型另含脚本本体）。
> 资产统一存放在仓库 `tools/` 目录，本页为总索引。

| 工具 ID | 名称 | 解决什么问题 | 所属模块小节 | 资产位置 |
|---------|------|-------------|-------------|---------|
| TOOL-emmx2md | 思维导图 TXT 转 MD（XMind 导入） | 亿图导出的 Tab 缩进 TXT → XMind 可导入的 Markdown 大纲，零丢字保真校验 | [M3 第九节](modules/03-testcase-generation/lecture.md) | [tools/emmx-to-md/](https://github.com/JennyHasACat/AITestingTraining/tree/main/tools/emmx-to-md) |
| TOOL-postman-param | Postman Collection 参数化生成 | 硬编码 Collection → 变量化 + 上下游传参 + 动态 UUID + Tests 断言，导入 Postman 配好环境变量即可 Runner 批量迭代 | [M8 第六节](modules/08-api-testing/lecture.md) | [tools/postman-param/](https://github.com/JennyHasACat/AITestingTraining/tree/main/tools/postman-param) |
| TOOL-framework-reverse | 框架逆向：代码库透视 + System Prompt 提炼 | 接手陌生框架读懂慢、经验留不住 → 两段式流水线：先透视代码库产出理解报告，再蒸馏为可复用的通用 System Prompt 资产 | [M9 第七节](modules/09-prompt-assets/lecture.md) | [tools/framework-reverse/](https://github.com/JennyHasACat/AITestingTraining/tree/main/tools/framework-reverse) |

## 工具登记规范（维护者）

1. 每个工具一个语义 ID（`TOOL-xxx`，不用序号），目录名 = ID 后缀；
2. 仓库根 `tools/<tool-id>/` 下按形态入库：形态 A（脚本型）= 脚本本体 + `prompt.md` + `README.md`；形态 B（纯提示词型）= `prompt.md` + `README.md`（可选 `sample/` 样例）；
3. 入课走「喵喵喵加肉-工具」：登记本页索引 + 对应模块 `lecture.md` 追加选学小节（10 min，不计入模块总时长）；
4. 三者一致性（`tools/` ↔ 本页 ↔ 课件小节）由「喵喵喵培训自检」第 ⑦ 项护栏保障；
5. 公开 / 私有策略：纯通用工具公开入库；含敏感实现的只在本页写「思路 + 伪步骤」，脚本留私有仓库。
