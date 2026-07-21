# M9 实战 Lab — OmniPeople 定制版：建设 OmniPeople 测试 Prompt 库

> **预计时长**：35 分钟

---

## 目标

今天我们从 0 开始建设 OmniPeople 测试团队的专属 Prompt 库，
选取 2–3 个在过去 M1–M8 学习中最有效的 OmniPeople 相关 Prompt，
整理成标准格式并贡献到 `prompt-templates/` 目录。

---

## Lab 9-A：候选 Prompt 盘点（10 min）

回顾过去各模块中使用过的 OmniPeople 专属 Prompt，
列出你认为值得保留的 3 条（从以下维度挑选）：

| 来源模块 | Prompt 描述 | 你的评分（⭐1-5）| 是否贡献 |
|---------|-----------|--------------|---------|
| M1-OmniPeople Lab | New Hire 场景头脑风暴 | | |
| M3-OmniPeople Lab | Part-Time 用例维度提取 | | |
| M4-OmniPeople Lab | Playwright 失败分析 | | |
| M5-OmniPeople Lab | New Hire 需求评审 | | |
| M6-OmniPeople Lab | SOQL 验证查询生成 | | |
| M7-OmniPeople Lab | POM 方法生成 | | |

---

## Lab 9-B：整理最高分 Prompt 为标准格式（20 min）

选取评分最高的 1–2 条，按 M9 课件的标准格式整理。

**示例：New Hire 需求评审 Prompt（已整理）**：

```markdown
## OP-R01 OmniPeople New Hire 需求歧义分析

**场景**：评审 New Hire 功能需求时，从可测性角度找出问题
**推荐工具**：Kimi（长文档处理好）
**效果评级**：⭐⭐⭐⭐⭐
**贡献者**：培训示例
**最后验证日期**：2026-07-20
**已知局限**：对 Salesforce 特有的字段条件显示逻辑理解有限，需要补充业务背景

---

### Prompt 正文

你是一名资深测试架构师，熟悉 HR 信息系统（基于 Salesforce）。
以下是 OmniPeople 系统的新员工入职（New Hire）功能需求描述：
[粘贴需求文档片段]

请从可测性角度分析，找出：
1. 模糊或矛盾的表述（至少3处）
2. 缺失的约束条件（如字段范围、必填规则）
3. 条件显示字段的触发规则是否完整定义
4. 审批流异常场景（退回/超时/并发审批）是否有说明
5. 建议补充的验收标准（Given-When-Then格式）

输出格式：表格，列：问题编号 | 问题类型 | 原文引用 | 问题描述 | 建议补充内容

---

### 使用说明
1. 将[粘贴需求文档片段]替换为当前迭代的需求文本
2. 如果需求涉及特定合同类型，在"背景"中补充说明
3. 适合在 Sprint 开始时的需求评审会议前使用

### 典型输出示例
[你在 Lab 5-A 中得到的最佳输出截图或文本]

### 已知效果不佳的场景
- 对 Salesforce 流（Flow）和触发器（Trigger）的内部逻辑理解不准确
- 超过 3000 字的需求文档可能导致分析质量下降（建议分段处理）
```

---

## Lab 9-C：贡献到仓库（5 min）

将整理好的 Prompt 添加到：
```
prompt-templates/testcase-design.md   ← 用例设计相关
prompt-templates/requirements-analysis.md  ← 需求评审相关
```

格式参考见上方示例，直接在文件末尾追加新模板即可。

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
