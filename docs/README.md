# AI 辅助软件测试 — 团队培训课程

> 适用对象：测试团队（手工 / 自动化 / API / CI/CD 混合）  
> 学习方式：自主学习（异步）  
> 总时长：约 18 小时 / 2 周完成  
> 工具要求：GitHub Copilot **或** Kimi / DeepSeek / 通义千问（任选其一即可开始）

---

## 🗺️ 学习路径总览

```
Week 1：认知建立 + 文档提效（全员必修）
  M1 → M2 → M3 → M4 → M5

Week 2：技术进阶 + 闭环整合
  M6（全员推荐）→ M7/M8（自动化工程师）→ M9 → M10（全员）
```

---

## 📚 课程目录

### Week 1 — 认知建立 + 文档提效（全员必修）

| 模块 | 标题 | 时长 | 课件 | 实战 Lab | 测验 |
|------|------|------|------|----------|------|
| M1 | AI 认知基础 + 工具环境搭建 | 1.5h | [lecture](modules/01-ai-foundations/lecture.md) | [通用版](modules/01-ai-foundations/lab-generic.md) · [OmniPeople版](modules/01-ai-foundations/lab-omnipeople.md) | [Quiz](modules/01-ai-foundations/quiz.md) |
| M2 | Prompt 工程精讲 | 2h | [lecture](modules/02-prompt-engineering/lecture.md) | [通用版](modules/02-prompt-engineering/lab-generic.md) · [OmniPeople版](modules/02-prompt-engineering/lab-omnipeople.md) | [Quiz](modules/02-prompt-engineering/quiz.md) |
| M3 | 测试用例 AI 批量生成 | 2h | [lecture](modules/03-testcase-generation/lecture.md) | [通用版](modules/03-testcase-generation/lab-generic.md) · [OmniPeople版](modules/03-testcase-generation/lab-omnipeople.md) | [Quiz](modules/03-testcase-generation/quiz.md) |
| M4 | Bug 分析与报告规范化 | 1.5h | [lecture](modules/04-bug-analysis/lecture.md) | [通用版](modules/04-bug-analysis/lab-generic.md) · [OmniPeople版](modules/04-bug-analysis/lab-omnipeople.md) | [Quiz](modules/04-bug-analysis/quiz.md) |
| M5 | 需求评审 + 测试计划提效 | 1.5h | [lecture](modules/05-requirements-planning/lecture.md) | [通用版](modules/05-requirements-planning/lab-generic.md) · [OmniPeople版](modules/05-requirements-planning/lab-omnipeople.md) | [Quiz](modules/05-requirements-planning/quiz.md) |

### Week 2 — 技术进阶 + 闭环整合

| 模块 | 标题 | 时长 | 受众 | 课件 | 实战 Lab | 测验 |
|------|------|------|------|------|----------|------|
| M6 | 数据库测试 + AI 辅助 SQL | 1.5h | 全员推荐 | [lecture](modules/06-database-testing/lecture.md) | [通用版](modules/06-database-testing/lab-generic.md) · [OmniPeople版](modules/06-database-testing/lab-omnipeople.md) | [Quiz](modules/06-database-testing/quiz.md) |
| M7 | 自动化脚本生成（Playwright） | 2h | 自动化工程师 | [lecture](modules/07-automation-playwright/lecture.md) | [通用版](modules/07-automation-playwright/lab-generic.md) · [OmniPeople版](modules/07-automation-playwright/lab-omnipeople.md) | [Quiz](modules/07-automation-playwright/quiz.md) |
| M8 | API 测试 + 自动化进阶 | 2h | 自动化/API | [lecture](modules/08-api-testing/lecture.md) | [通用版](modules/08-api-testing/lab-generic.md) · [OmniPeople版](modules/08-api-testing/lab-omnipeople.md) | [Quiz](modules/08-api-testing/quiz.md) |
| M9 | Prompt 资产体系建设 | 1.5h | 全员 | [lecture](modules/09-prompt-assets/lecture.md) | [通用版](modules/09-prompt-assets/lab-generic.md) · [OmniPeople版](modules/09-prompt-assets/lab-omnipeople.md) | [Quiz](modules/09-prompt-assets/quiz.md) |
| M10 | 完整 AI 闭环演练 + ROI 汇报设计 | 2h | 全员 + Manager | [lecture](modules/10-full-loop-roi/lecture.md) | [通用版](modules/10-full-loop-roi/lab-generic.md) · [OmniPeople版](modules/10-full-loop-roi/lab-omnipeople.md) | [Quiz](modules/10-full-loop-roi/quiz.md) |

---

## 🗂️ 额外资源

| 资源 | 说明 | 链接 |
|------|------|------|
| Prompt 模板资产包 | 6 大场景 30+ 条可直接复用的 Prompt | [prompt-templates/](prompt-templates/README.md) |
| 30 天落地行动计划 | 培训结束后的跟进节奏与 ROI 度量 | [roadmap/30-day-action-plan.md](roadmap/30-day-action-plan.md) |
| Rovo Agents 速查 | JIRA Rovo 的 AI agent 列表（含官方链接）+ 自建测试用例生成 agent 示例 | [Rovo_Agents.md](Rovo_Agents.md) |

---

## 🚀 快速开始（新学员看这里）

1. **确认工具可用**：打开 [Kimi](https://kimi.moonshot.cn/) 或 [DeepSeek](https://chat.deepseek.com/) 或 [通义千问](https://tongyi.aliyun.com/)，能正常对话即可。
2. **按顺序学习**：从 M1 开始，每天 1–2 小时，2 周完成。
3. **完成 Lab 再做 Quiz**：每模块的实战 Lab 是重点，Quiz 检验理解。
4. **提交问题 / 讨论**：使用 GitHub Issues（标签：`question` / `feedback` / `share-prompt`）。

---

## 📅 2 周学习计划表

| 日期 | 模块 | 预计用时 | 备注 |
|------|------|---------|------|
| Day 1 | M1 | 1.5h | 工具账号当天必须到位 |
| Day 2 | M2 | 2h | 核心！Prompt 技巧决定后续效果 |
| Day 3 | M3 | 2h | 直接用真实需求练习 |
| Day 4 | M4 | 1.5h | |
| Day 5 | M5 | 1.5h | Week 1 完成后做一次小组分享 |
| Day 6 | M6 | 1.5h | 全员建议完成 |
| Day 7 | M7 | 2h | 手工测试同学可选做，自动化工程师必修 |
| Day 8 | M8 | 2h | |
| Day 9 | M9 | 1.5h | 当天输出团队 Prompt 草稿 |
| Day 10 | M10 | 2h | 最终演练 + 产出效率数据 |

---

## 🏷️ Issues 使用规范

```
[question]    模块编号 + 问题描述   ← 学员提问
[feedback]    模块编号 + 改进建议   ← 内容反馈
[share-prompt] 场景描述 + Prompt 内容 ← 好 Prompt 共享
[bug]         描述问题              ← 内容错误报告
```

---

*课程内容持续更新。如有疑问请提 Issue 或联系培训负责人。*
