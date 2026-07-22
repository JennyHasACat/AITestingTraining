# Handoff — 培训内容一致性审查

> 创建时间：2026-07-21
> 状态：**审查已完成，问题已登记，尚未修复（用户暂停，待后续处理）**
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
| 修复代码/文档 | ❌ 未开始（用户暂停） |

---

## 3. 已登记的一致性问题（待修复）

### 高优先级

**H1 — README 模板数量虚标**
- 位置：`docs/prompt-templates/README.md` 第 3 行
- 现状：`> 共 6 个场景分类，60+ 条经验证的可复用 Prompt 模板`
- 实际：仅 6 个模板文件 + 1 个 Rovo Agent 文件，约 33 条模板，远不到 60+。
- 修复方向：改为真实数量（如"6 个分类，30+ 条"），或补全模板到 60+。

**H2 — 贡献门槛自相矛盾**
- 位置：
  - `docs/prompt-templates/README.md` 第 5 行写"2 人以上验证通过"，第 41 行又写"等待 1 位以上成员确认使用有效"
  - `docs/modules/09-prompt-assets/lecture.md` 第 120 行写"经过 2+ 人验证后，去掉 [需要验证] 标签"
- 现状：README 内部（2人 vs 1人）不一致，且 README 与 M9 lecture（2+人）也不一致。
- 修复方向：统一为单一口径（建议"2 人以上验证"与 M9 对齐）。

**H3 — M10 quiz 缺 Q6 编号**
- 位置：`docs/modules/10-full-loop-roi/quiz.md`
- 现状：页头写"题目数量：6 题"，但实际 Q5 之后直接跳到 Q7（综合题），无 Q6。
- 修复方向：补 Q6 或修正页头题数；同时把"6 题"口径统一。

### 中优先级

**M4 — M10 ROI 时间基线 lecture 与 lab 不一致**
- 位置：`docs/modules/10-full-loop-roi/lecture.md` vs `lab-omnipeople.md` / `lab-generic.md`
- 现状：lecture 写"需求 30min / 脚本 4h"，lab 写"需求 20min / 脚本 120min"，影响 ROI 计算基准。
- 修复方向：统一一组基准数字，lecture 与 lab 引用同一处。

**M5 — T-05 编号在两文件重复**
- 位置：`docs/prompt-templates/testcase-design.md` 第 87 行（`## T-05 CSV 导出`）与 `report-writing.md` 第 7 行（`## T-05 测试总结报告生成`）
- 修复方向：report-writing 中的 T-05 改为未占用的编号（如 T-06）。

**M6 — M1 命名不一致（smartClick vs smartWait）**
- 位置：`docs/modules/01-ai-foundations/lab-generic.md` 第 65 行用 `page.smartClick()`，quiz.md 第 119 行用 `page.smartWait()` 作为"不存在的方法"示例。
- 现状：两者均为虚构方法，但学员易困惑哪个是真/哪个是教学反例。
- 修复方向：在 lab 中明确 `smartClick` 为"假设方法/示意"，或统一术语。

### 低优先级

**L7 — Rovo Agent 未入 README 目录**
- 位置：`docs/prompt-templates/README.md` 模板索引表未收录 `rovo-test-case-generator-agent.md`
- 修复方向：在索引表补一行。

---

## 4. 结构性依赖（非 bug，需知会）

所有 OmniPeople 版 Lab 强依赖真实项目仓库路径（`fixtures/`、`page_objects/`、`Screenshot/`、`salesforceAPI.py`）。对**有 Bitbucket 权限的内部员工**无碍；若未来有外部学员，动手环节会卡住。当前维持"公开课件 + 私有代码"方案，无需改动。

---

## 5. 用户意图（已确认）

- 培训站已上线，暂不新增内容，优先把**已发布内容做准确、一致**。
- 用户今天较忙，暂停修复，先理解意图、给方案，后续再动手。
- 明确要求：**本次不要改任何代码/文档**，只产出 handoff 与方案。

---

## 6. 后续可选方案（待用户选定后执行）

- **方案 A — 一次性批量修复**：把 H1–L7 共 7 项在一个 commit 内全部修正，最快收口。
- **方案 B — 高优优先**：先修 H1/H2/H3（影响准确性最直观），中/低优先级留待下次内容更新顺手改。
- **方案 C — 随内容迭代顺带修**：不单独开 pass，每次改到对应模块/文件时顺手修正，避免一次性大改。
- **方案 D — 加一致性检查护栏**：在 `.codebuddy/rules/` 或 CI 中加一条检查（如 quiz 题号连续、模板编号唯一、README 数量声明与实际文件数一致），防止回归。

> 推荐：方案 B（先消高优）+ 方案 D（加护栏）组合。
