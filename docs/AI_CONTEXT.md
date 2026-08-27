# AI_CONTEXT.md — AITestingTraining 项目快速上手

## 项目定位

为测试团队（10人，混合型）设计的 **AI 辅助测试培训课程**，2 周自主学习，约 18 小时。  
托管方式：GitHub，Markdown 格式，全员在线阅读。

---

## 目录结构

```
AITestingTraining/
├── README.md                    ← 入口（维护者说明），课程站见下方 docs/
├── mkdocs.yml                   ← MkDocs 站点配置（docs_dir: docs）
├── tools/                       ← AI 提效小工具资产库（脚本 + prompt.md + README），不入站点构建
│   └── emmx-to-md/              ← TOOL-emmx2md：亿图 TXT → XMind 可导入 MD
└── docs/                        ← 课程正文，由 MkDocs 构建为站点
    ├── AI_CONTEXT.md            ← 本文件，项目快速上手
    ├── AITestingTraining_MindMap.md  ← 课程思维导图
    ├── Rovo_Agents.md           ← Rovo Agents 速查
    ├── toolbox.md               ← AI 提效工具箱（工具总索引，学员可见）
    ├── modules/                 ← 10 个学习模块，每模块 4 个文件
    │   ├── 01-ai-foundations/
    │   ├── 02-prompt-engineering/
    │   ├── 03-testcase-generation/
    │   ├── 04-bug-analysis/
    │   ├── 05-requirements-planning/
    │   ├── 06-database-testing/
    │   ├── 07-automation-playwright/
    │   ├── 08-api-testing/
    │   ├── 09-prompt-assets/
    │   └── 10-full-loop-roi/
    ├── prompt-templates/        ← 30+ 条可直接复用的 Prompt 模板（7 个分类）
    │   ├── README.md
    │   ├── testcase-design.md       T-01~T-06 + OP-T01
    │   ├── bug-report.md            B-01~B-05 + OP-B01
    │   ├── script-generation.md     AUTO-01~AUTO-05 + OP-AUTO01
    │   ├── sql-query.md             DB-01~DB-05（含 SOQL）
    │   ├── requirements-analysis.md R-01~R-06
    │   ├── report-writing.md        D-05, D-01~D-04
    │   └── rovo-test-case-generator-agent.md  ← Rovo Agent（测试用例生成）
    └── roadmap/
        └── 30-day-action-plan.md    ← 培训后的 30 天落地计划
```

每个模块下固定 4 个文件：
- `lecture.md` — 课件讲稿
- `lab-generic.md` — 通用实战练习（含参考答案）
- `lab-omnipeople.md` — OmniPeople 项目定制版 Lab
- `quiz.md` — 测验题（`<details>` 折叠答案，可在线自测）

---

## 课程结构（2 周 / 18 小时）

| 周次 | 模块 | 主题 | 时长 | 受众 |
|------|------|------|------|------|
| Week 1 | M1 | AI 认知基础 + 工具环境搭建 | 1.5h | 全员 |
| | M2 | Prompt 工程精讲（核心！） | 2h | 全员 |
| | M3 | 测试用例 AI 批量生成 | 2h | 全员 |
| | M4 | Bug 分析与报告规范化 | 1.5h | 全员 |
| | M5 | 需求评审 + 测试计划提效 | 1.5h | 全员 |
| Week 2 | M6 | 数据库测试 + AI 辅助 SQL/SOQL | 1.5h | 全员推荐 |
| | M7 | Playwright 自动化脚本生成 | 2h | 自动化工程师 |
| | M8 | API 测试 + 自动化进阶 | 2h | 自动化/API |
| | M9 | Prompt 资产体系建设 | 1.5h | 全员 |
| | M10 | 完整 AI 闭环演练 + ROI 汇报 | 2h | 全员 + Manager |

---

## 关键设计决策

| 决策 | 原因 |
|------|------|
| 双轨 Lab（通用 + OmniPeople 定制） | 通用题方便内部分享，OmniPeople 题直接与真实工作对接 |
| M6 包含 SOQL 专项 | 团队使用 Salesforce，标准 SQL 不适用 |
| Prompt 模板用 `OP-` 前缀区分 | OmniPeople 专属 Prompt 与通用 Prompt 分开管理 |
| M10 有 Manager ROI 专项 | 量化数据是争取后续 AI 工具预算的核心依据 |
| Quiz 用 `<details>` 折叠答案 | 支持在线自测，无需额外系统 |

---

## Prompt 模板命名规范

| 前缀 | 含义 |
|------|------|
| `T-` | 测试用例设计 |
| `B-` | Bug 分析报告 |
| `R-` | 需求分析 |
| `DB-` | 数据库 SQL/SOQL |
| `AUTO-` | 自动化脚本 |
| `D-` | 文档报告 |
| `OP-` | OmniPeople 项目专属 |

---

## 推荐工具组合

| 任务 | 首选工具 |
|------|---------|
| 需求分析、长文档 | Kimi |
| 代码生成、SQL、逻辑推理 | DeepSeek |
| IDE 内实时补全 | GitHub Copilot |
| 通用场景 | 通义千问 / DeepSeek |

---

## 后续维护

- Prompt 贡献：GitHub Issues → `[prompt-new]` 标签 → PR → 2 人验证后合并
- 课件更新：直接 PR，无需特殊审批
- 失效 Prompt 标记：Issues → `[prompt-invalid]` 标签
- 建议频率：每月 Review Prompt 库；每季度 Review 课件内容

---

## 如何扩展课件（持续"加肉"约定）

本课件采用统一节奏，新增内容只需在目标模块的 `lecture.md` 追加一个「第 N 节」，套用以下骨架，无需改动既有编号、导航与小结。

### 标准小节骨架

```markdown
## 第 N 节：[小节标题]（X min）

### 它解决什么问题
[一句话说明痛点]

### 核心思路 / 提示词骨架
[可直接复制改的 Prompt 或伪步骤；私有内容只写思路，不贴内部代码]

### 使用示例
[一个最小可运行示例]

### 注意事项
[踩坑点 / 数据安全 / 人工兜底]
```

### "AI 提效小工具"类内容的统一标题约定

所有工具型补充统一用以下小节名，便于全局检索与后续批量更新：

```markdown
## 第 N 节：AI 提效小工具 —— [工具名]（X min）
> 待补充：具体工具 / 链接 / 进阶用法（由维护者持续更新）
```

全局搜索 `AI 提效小工具` 即可定位全部此类小节。

### 一键加肉规则

项目内置规则 `training-content-add-flesh.mdc`（触发词「喵喵喵加肉」）：说出"喵喵喵加肉：在 M6 加一个『AI 自然语言转 SQL 工具』小节，内容是……"即可自动定位模块、套骨架插入、并提示跑「喵喵喵培训自检」回归。

### 工具入课规则（喵喵喵加肉-工具）

有「Python 脚本 + 生成它的原始 Prompt」要入课时，说"喵喵喵加肉-工具：脚本 xxx.py 入 M某，原始 Prompt 如下……"，自动走全链路：`tools/<tool-id>/` 三件套入库（TOOL-xxx 语义 ID）→ `docs/toolbox.md` 索引登记 → 指定模块 lecture.md 追加选学小节（10 min，不计入总时长）→ 跑「喵喵喵培训自检」。首个样板：TOOL-emmx2md（M3 第九节）。

### 护栏提醒

- 新增 Prompt 模板必须走 `M9` 标准格式，且编号不得与现有 `T-/B-/R-/DB-/AUTO-/D-/OP-` 重复（见 `training-content-consistency` 护栏）。
- 每次扩展后运行「喵喵喵培训自检」确认 quiz 题号、模板编号、引用无回归。
- 私有实现只写"思路 + 伪步骤"，符合公开课件 + 私有代码约定。

---

## 关联项目

- `OmniPeopleAIUIAutomation/` — OmniPeople 自动化测试项目（Lab 定制版练习材料的来源）
  - `fixtures/omniPeople/` — YAML 测试数据（M3 OmniPeople Lab 参考）
  - `page_objects/omniPeople/` — Page Object（M7 OmniPeople Lab 参考）
  - `Screenshot/` — 失败截图（M4 OmniPeople Lab 参考）
  - `salesforceAPI.py` — Salesforce API 封装（M8 OmniPeople Lab 参考）
