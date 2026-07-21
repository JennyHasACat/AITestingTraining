# Rovo Agents 速查 — 测试团队视角

> 适用场景：JIRA / Confluence 里用 Atlassian Rovo 的 AI agent 提效测试工作。
> 更新时间：2026-07-20

---

## 一、官方入口链接（已验证可用）

| 入口 | 用途 | 链接 |
|------|------|------|
| Rovo 产品总览 | 了解 Rovo 全家桶（Search / Chat / Studio / Agents） | https://www.atlassian.com/software/rovo |
| Rovo 帮助中心 | 官方支持文档入口、社区、系统状态 | https://support.atlassian.com/rovo/ |
| Rovo 博客（Inside Atlassian） | 官方发布的 agent / 案例文章 | https://www.atlassian.com/blog/rovo |
| 在你的实例里查看 agent | Rovo 应用 → `Agents` 标签页（Featured / Your agents） | `https://<你的域名>.atlassian.net/wiki/rovo/agents` |

> ⚠️ 每个 agent 没有独立的稳定公网深链，目录会随版本/订阅变化。以你实例里 Rovo → Agents 实际展示的列表为准。

---

## 二、Rovo 常见精选 Agent 及用途（测试相关重点标注）

| Agent | 用途 | 测试团队用法 |
|-------|------|-------------|
| **Edict**（Editorial Dictator） | 审阅润色文本：语法/清晰度/语气/风格 | ✅ 打磨 Confluence 测试方案、Jira 描述、缺陷报告 |
| **Deep Research** | 跨已连接应用做多步研究并出综合报告 | 调研某功能历史决策/现状，产出测试范围依据 |
| **Incident Manager** | 事件期间总结影响、起草状态通报、建议下一步 | 线上故障时的沟通与回归范围建议 |
| **Jira Issue Classifier / Triage** | 自动打标签、归类、建议优先级/组件 | ✅ 新需求/缺陷自动分流，减少手工 triage |
| **PR Reviewer / Summarizer** | 总结 PR 改动、高亮风险点 | ✅ 自动化脚本 PR 的评审初稿 |
| **Translator** | 跨语言翻译并保持语气 | 多语言团队互译用例/文档 |
| **Knowledge / Q&A agent** | 基于 Teamwork Graph 作答并附引用 | ✅ "最新测试规范是什么？"类问题 |
| **1:1 / Meeting agents** | 准备 1:1、总结会议、提取 action items | 复盘会/评审会纪要 |
| **Help Desk / JSM agent** | 分流应答 JSM 工单、拦截常见请求 | 服务台自助应答 |
| **Studio 自建 agent** | 用指令+工具+知识源搭专属 agent | ✅ 见下方「三、实际 Sample」 |

---

## 三、实际 Sample：自建「测试用例生成 Agent」（Rovo Studio）

下面是一份**可直接复制到 Rovo Studio → Create agent** 的定义，针对测试团队的「需求 → 用例」场景。

### 3.1 Agent 基本配置

| 字段 | 填写值 |
|------|--------|
| **Name** | 测试用例生成助手（Test Case Generator） |
| **Description** | 根据 Jira 需求/用户故事，生成可导入 Zephyr 的结构化功能测试用例（CSV），覆盖正常/异常/边界。 |
| **Goal** | 把需求文本快速转化为符合团队模板的测试用例初稿，标注置信度。 |
| **Visibility** | 团队可见（Team） |
| **Connected tools** | Jira（读取 issue）、Confluence（读取 PRD/规范）、Web（可选） |
| **Knowledge sources** | 团队用例模板页、测试规范 Confluence 空间 |

### 3.2 Instructions（系统提示词，直接粘贴）

```text
你是一名有 10 年经验的测试架构师。任务：基于用户提供的一条 Jira 需求 / 用户故事，
生成结构化功能测试用例，输出为可导入 Zephyr 的 CSV。

# 输出格式（CSV 列顺序，每行一个 Test Step）
Test Key | Title | Module | Description | Preconditions | Priority | Test Steps | Data for Steps | Expected Results | Jira Story ID | Test Type | Component | Release | Test Case Status | Creator | Folder

# 规则
1. 每个用例至少 3 步：Login → Navigate → 业务步骤；每条 Test Step 必须有对应 Expected Results。
2. 覆盖三类：正常路径（Positive）、异常路径（Negative / 校验拦截）、边界值（Boundary）。
3. 优先级映射：P0→1-Critical，P1→2-High，P2→3-Medium，P3→4-Low，无标注默认 High。
4. Data for Steps 仅填需求中明确给出的具体数据，禁止编造。
5. 每个用例末尾标注 [置信度: 高/中/低]，低置信度需在 Note 列说明原因。
6. 仅使用用户提供的模块名作为 Module；不要臆造字段。

# 输出后
- 先给 1 行摘要：本批用例数、覆盖维度、低置信度数量。
- 再输出 CSV 正文。
```

### 3.3 实际调用 Sample

**输入（粘贴到 agent 对话框）：**

```text
Jira Story OMNI-69714: Phone Number Parsing Logic Architecture
需求：修改 Opportunity 的 [Contact's Main Mobile] 为以下值，触发 SFC job 'cekatStageChangeNotify'，
检查 RequestBody 里的 [phone_number] 解析结果。
- 正例：Input 081213154611 → 6281213154611
- 负例/边界：Input (SG) 91234567 → 6291234567；Input (60) 11-1234 5678 → 601112345678
Module: Phone Number Parsing Logic Architecture
```

**Agent 预期输出（节选）：**

```csv
Test Key,Title,Module,Description,Preconditions,Priority,Test Steps,Data for Steps,Expected Results,Jira Story ID,Test Type,Component,Release,Test Case Status,Creator,Folder
TC_OMNI-69714_1,Verify Standard 08 prefix under positive scenarios,Phone Number Parsing Logic Architecture,,,2 - High,Login the Salesforce;Navigate to Phone Number Parsing Logic Architecture module;Change [Contact's Main Mobile] with the below value;Trigger SFC job 'cekatStageChangeNotify';Check [phone_number] in 'RequestBody',081213154611,"User can check the login function works well;User can check the function work as expected;User can check the function work as expected;User can check the function work as expected;The [phone_number] in 'RequestBody' displays as 6281213154611",OMNI-69714,Functional,,,Under Review,ext.jenny.ge,
TC_OMNI-69714_8,Verify Non-numeric in brackets under Negative Scenarios,Phone Number Parsing Logic Architecture,,,2 - High,Login the Salesforce;Navigate to Phone Number Parsing Logic Architecture module;Change [Contact's Main Mobile] with the below value;Trigger SFC job 'cekatStageChangeNotify';Check [phone_number] in 'RequestBody',(SG) 91234567,"User can check the login function works well;User can check the function work as expected;User can check the function work as expected;User can check the function work as expected;The [phone_number] in 'RequestBody' displays as 6291234567",OMNI-69714,Functional,,,Under Review,ext.jenny.ge,
```

> 摘要示例：`本批生成 12 条用例（正例 5 / 负例+边界 7），覆盖正常·异常·边界三维度，低置信度 0。`

### 3.4 落地建议
1. 先在 **Studio** 用上面 Instructions 建 agent，连通你们团队的 Confluence 用例模板空间作为 Knowledge。
2. 用 1 条真实 Jira Story 试跑，人工只 Review agent 标注的「低置信度」用例。
3. 跑通后把该 agent 加入 README「额外资源」或团队 Prompt 资产包，全员复用。

---

*链接与 agent 列表以各团队实际 Rovo 实例为准；本文档聚焦测试场景用法。*
