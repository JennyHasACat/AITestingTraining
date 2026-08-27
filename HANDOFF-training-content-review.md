# Handoff — 培训内容一致性审查

> 创建时间：2026-07-21
> 最后更新：2026-08-27
> 状态：**审查已完成（7 项已推送 `main`）；N1/N2 经核对已随 `fcd3090` 推送；2026-08-27 新增「工具入课流水线」落地（TOOL-emmx2md 首个样板），本地待推送**
> 范围：AITestingTraining 培训站全部 10 个模块 + Prompt 模板库 + roadmap

---

## 1. 背景

培训站已部署上线（GitHub Pages，Public）：
`https://Jennyhasacat.github.io/AITestingTraining/`

部署链路已打通：`main` 分支推送 → `.github/workflows/deploy.yml` → `mkdocs gh-deploy` → `gh-pages`。Sample 真实代码留在公司 Bitbucket（私有），培训站只含课件与实验说明，无代码外泄。

部署完成后，用户要求"挨个检查培训内容，列出优缺点"。已完成全量通读（10 模块 × 4 文件 + 8 个 Prompt 模板 + roadmap），产出优缺点清单，并提炼出 7 项需修复的一致性问题。

---

## 2. 当前进度

| 阶段 | 状态 |
|------|------|
| GitHub Pages 部署 | ✅ 完成 |
| 全量内容通读与优缺点分析 | ✅ 完成 |
| 一致性问题登记（7 项） | ✅ 完成（见下） |
| 修复文档（方案 A+D） | ✅ 完成（7 项全修 + 护栏 + 根 README，已推送 `main`） |
| 一致性护栏规则 | ✅ 完成（`.codebuddy/rules/training-content-consistency.mdc`） |
| 维护者根 README | ✅ 完成（`README.md`，不进课程站） |

---

## 3. 已登记的一致性问题（全部已修复 ✅）

> 修复于 2026-07-22，提交 `128ee11` 已推送 `main`，站点自动重建。涉及文件共 11 个（含新增护栏规则与 HANDOFF）。

### 高优先级

**H1 — README 模板数量虚标** ✅ 已修复
- 位置：`docs/prompt-templates/README.md` 第 3 行
- 现状：`> 共 6 个场景分类，60+ 条经验证的可复用 Prompt 模板`
- 实际：仅 6 个模板文件 + 1 个 Rovo Agent 文件，约 33 条模板，远不到 60+。
- 修复结果：README 顶部、课程总览 `docs/README.md`、`docs/AI_CONTEXT.md` 三处统一改为"30+ 条"。

**H2 — 贡献门槛自相矛盾** ✅ 已修复
- 位置：
  - `docs/prompt-templates/README.md` 第 5 行写"2 人以上验证通过"，第 41 行又写"等待 1 位以上成员确认使用有效"
  - `docs/modules/09-prompt-assets/lecture.md` 第 120 行写"经过 2+ 人验证后，去掉 [需要验证] 标签"
- 现状：README 内部（2人 vs 1人）不一致，且 README 与 M9 lecture（2+人）也不一致。
- 修复结果：README 第 41 行"1 位以上"→"2 位以上"，与 M9 lecture 口径统一。

**H3 — M10 quiz 缺 Q6 编号** ✅ 已修复
- 位置：`docs/modules/10-full-loop-roi/quiz.md`
- 现状：页头写"题目数量：6 题"，但实际 Q5 之后直接跳到 Q7（综合题），无 Q6。
- 修复结果：跳号的 `Q7（综合题）`→`Q6（综合题）`，页头"6 题"口径自洽。

### 中优先级

**M4 — M10 ROI 时间基线 lecture 与 lab 不一致** ✅ 已修复
- 位置：`docs/modules/10-full-loop-roi/lecture.md` vs `lab-omnipeople.md` / `lab-generic.md`
- 现状：lecture 写"需求 30min / 脚本 4h"，lab 写"需求 20min / 脚本 120min"，影响 ROI 计算基准。
- 修复结果：`lab-generic.md` 传统预估对齐 lecture 基线（需求 30 / 用例 120 / 脚本 240 / 总结 60 min，合计 450 min）。`lab-omnipeople.md` 原口径本就与 lecture 一致，无需改。

**M5 — T-05 编号在两文件重复** ✅ 已修复
- 位置：`docs/prompt-templates/testcase-design.md` 第 87 行（`## T-05 CSV 导出`）与 `report-writing.md` 第 7 行（`## T-05 测试总结报告生成`）
- 修复结果：report-writing 的 `T-05`→`D-05`，并同步 6 处引用（M2 lecture、M10 lecture/lab、AI_CONTEXT 目录树、README 导航表）。testcase-design 的 `T-05 CSV 导出` 保留（合法，属 CSV 列名）。

**M6 — M1 命名不一致（smartClick vs smartWait）** ✅ 已修复
- 位置：`docs/modules/01-ai-foundations/lab-generic.md` 第 65 行用 `page.smartClick()`，quiz.md 第 119 行用 `page.smartWait()` 作为"不存在的方法"示例。
- 现状：两者均为虚构方法，但学员易困惑哪个是真/哪个是教学反例。
- 修复结果：quiz.md 示例方法名改为 `page.smartClick()`，与 lab 对齐（两者均为示意性虚构方法）。

### 低优先级

**L7 — Rovo Agent 未入 README 目录** ✅ 已修复
- 位置：`docs/prompt-templates/README.md` 模板索引表未收录 `rovo-test-case-generator-agent.md`
- 修复结果：README 导航表补 `rovo-test-case-generator-agent.md` 一行（场景：Rovo Agent 测试用例生成）。

---

## 4. 结构性依赖（非 bug，需知会）

所有 OmniPeople 版 Lab 强依赖真实项目仓库路径（`fixtures/`、`page_objects/`、`Screenshot/`、`salesforceAPI.py`）。对**有 Bitbucket 权限的内部员工**无碍；若未来有外部学员，动手环节会卡住。当前维持"公开课件 + 私有代码"方案，无需改动。

---

## 5. 用户意图（已确认）

- 培训站已上线，暂不新增内容，优先把**已发布内容做准确、一致**。
- 初始 handoff 阶段用户较忙，要求"先只产出 handoff 与方案、不要改代码"；**后续（2026-07-22）用户选定方案 A+D，已实际修复并推送**。
- 偏好约定：推送 `main`（一推即上线）前先贴 diff 给用户过目再执行（本次会话口头约定，未固化为持久记忆）。

---

## 6. 后续可选方案（已选定并执行）

- **方案 A — 一次性批量修复**：把 H1–L7 共 7 项在一个 commit 内全部修正，最快收口。 → ✅ **已执行**（2026-07-22，提交 `128ee11`）
- **方案 B — 高优优先**：先修 H1/H2/H3（影响准确性最直观），中/低优先级留待下次内容更新顺手改。
- **方案 C — 随内容迭代顺带修**：不单独开 pass，每次改到对应模块/文件时顺手修正，避免一次性大改。
- **方案 D — 加一致性检查护栏**：在 `.codebuddy/rules/` 或 CI 中加一条检查（如 quiz 题号连续、模板编号唯一、README 数量声明与实际文件数一致），防止回归。 → ✅ **已执行**（新增 `.codebuddy/rules/training-content-consistency.mdc`，触发词"喵喵喵培训自检"）

> 用户最终选择 **A + D** 组合：7 项一次性批量修复，并补一致性护栏防止回归。

### 本会话额外新增（非原 7 项）

- 新增仓库根 `README.md`：面向维护者/培训组织者，含自动部署链路 ASCII 图、`mkdocs serve` 本地预览、提交发布约定。**不进 `docs/` 故不会被课程站发布**。
- 注：根 `README.md` 创建后**尚未 commit/push**（按用户"推 `main` 前先过目"约定暂留本地）。

---

## 7. 2026-08-14 新增修复记录（文档滞后，非原 7 项）

> 状态：**已修复（本地未推送）** | 范围：`docs/AI_CONTEXT.md`、`docs/prompt-templates/README.md`
> 触发：用户核对实际文件与 `AI_CONTEXT.md` 描述不一致 → 执行「喵喵喵培训自检」确认无回归

### 背景

原 HANDOFF（2026-07-22）记录 7 项已修复，但后续新增了 3 个文件（`mkdocs.yml`、`AITestingTraining_MindMap.md`、`Rovo_Agents.md`，其中 Rovo Agent 已在 L7 入模板目录但文档树未同步），导致 `AI_CONTEXT.md` 目录树与实际布局再次脱节。本次为补登这些滞后项。

### 新增修复项

**N1 — `AI_CONTEXT.md` 目录树与实际布局脱节** ✅ 已修复（本地）
- 位置：`docs/AI_CONTEXT.md` 第 12–36 行（目录结构代码块）
- 现状：
  - 目录树把 `modules/`、`prompt-templates/`、`roadmap/` 画在仓库根，实际均位于 `docs/` 下；
  - 遗漏 `mkdocs.yml`、`docs/AITestingTraining_MindMap.md`、`docs/Rovo_Agents.md` 三个文件；
  - Prompt 模板仍写「30+ 条」且分类只列 6 个（未含 Rovo Agent 文件）。
- 修复结果：目录树补 `docs/` 前缀，新增上述 3 个文件行，Prompt 模板标注「7 个分类」并补 `rovo-test-case-generator-agent.md` 一行。

**N2 — `prompt-templates/README.md` 场景分类计数未更新** ✅ 已修复（本地）
- 位置：`docs/prompt-templates/README.md` 第 3 行
- 现状：顶部写「共 **6 个场景分类**」，但下方导航表实际列了 7 行（含 Rovo Agent），与 L7 修复后状态自相矛盾。
- 修复结果：第 3 行「6 个场景分类」→「7 个场景分类」。

### 一致性自检结果（同日「喵喵喵培训自检」）

护栏 6 项全部通过，确认 N1/N2 修复未引入回归：

| # | 检查项 | 结果 |
|---|--------|------|
| ① | quiz 题号连续 + 页头题数 | ✅ 10 模块全连续，题数自洽 |
| ② | 模板编号全目录唯一 | ✅ 40 条无重复 |
| ③ | README 数量声明 | ✅ 实际 40 条 ≥「30+ 条」 |
| ④ | 贡献门槛统一 | ✅ README 与 M9 lecture 均为 2 人以上 |
| ⑤ | M10 ROI 基线一致 | ✅ lecture 与 lab-generic 逐环节一致 |
| ⑥ | 模板引用有效 | ✅ 各模块引用编号均真实存在 |

### 待办（按"推 `main` 前先过目"约定）

- [x] ~~`docs/AI_CONTEXT.md`（N1）、`docs/prompt-templates/README.md`（N2）改动尚未 commit/push~~ → 2026-08-27 核对：`origin/main..HEAD` 为空，N1/N2 与根 `README.md` 均已随 `fcd3090` 推送，本待办关闭。
- [x] ~~根 `README.md` 仍按原约定留本地未推（见第 6 节）~~ → 同上，已推送。

---

## 8. 2026-08-27 新增：工具入课流水线落地（TOOL-emmx2md 首个样板）

> 状态：**已落地（本地待推送）** | 触发：用户提供 `emmx_to_md.py` + 生成它的原始 Prompt，要求入课并考虑后续同类内容的可延续性

### 落地的机制（可延续性设计）

以后再有「提示词 + Python 文件」入课，触发词「喵喵喵加肉-工具」自动走全链路：

```
tools/<tool-id>/ 三件套入库 → docs/toolbox.md 索引登记 → 模块 lecture.md 追加选学小节 → 喵喵喵培训自检
```

关键约定：

- 工具 ID 用语义 ID（`TOOL-xxx`，不用序号），目录名 = ID 后缀；三件套 = 脚本 + `prompt.md`（原始 Prompt 原文）+ `README.md`；
- 工具型小节**一律选学、默认 10 min、不计入模块总时长**（课程 18h 不变）；
- 公开 / 私有默认策略：纯通用工具公开入库；含敏感实现只写「思路 + 伪步骤」；
- 一致性护栏新增第 ⑦ 项：`tools/` ↔ `toolbox.md` ↔ 课件小节三者一致 + TOOL- 编号唯一。

### 本次变更清单

| # | 文件 | 变更 |
|---|------|------|
| 1 | `tools/emmx-to-md/`（新建） | 脚本从仓库根移入；新增 `README.md`、`prompt.md`（原始 Prompt 原文） |
| 2 | `tools/README.md`（新建） | 工具资产库维护者规范 |
| 3 | `docs/toolbox.md`（新建） | 「AI 提效工具箱」站点索引页，收录 TOOL-emmx2md |
| 4 | `mkdocs.yml` | nav 新增「AI 提效工具箱: toolbox.md」（位于 Prompt 模板之前） |
| 5 | `docs/modules/03-testcase-generation/lecture.md` | 追加第九节（AI 提效小工具 —— 思维导图 TXT 转 MD，10 min 选学），不动既有八节编号与小结 |
| 6 | `docs/modules/02-prompt-engineering/lecture.md` | 第一节「要素 5」末尾加 TOOL-emmx2md 交叉引用（五要素实战范例） |
| 7 | `docs/AI_CONTEXT.md` | 目录树补 `tools/` + `toolbox.md`；加肉约定补「喵喵喵加肉-工具」说明 |
| 8 | `.codebuddy/rules/training-content-add-flesh.mdc` | 新增工具型分支（全链路流程 + 选学不计时长 + 公开/私有策略） |
| 9 | `.codebuddy/rules/training-content-consistency.mdc` | 新增第 ⑦ 项检查（工具资产三者一致），触发条件扩至 `toolbox.md` / `tools/**` |

### 待办（按"推 `main` 前先过目"约定）

- [ ] 上述改动贴全量 diff 给用户过目后，commit + push `main`（一推即上线）。
- [ ] 仓库存在未跟踪杂项：`docs/6d3e301b6ae2ff65e618075290bc370c.jpg`、`site/`（本地构建产物）、`.vscode/`、`.DS_Store`，是否入库或加 `.gitignore` 由用户裁决（本次不处理）。
