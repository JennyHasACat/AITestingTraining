# M8 实战 Lab — OmniPeople 定制版：Salesforce API 测试

> **预计时长**：35 分钟 | **工具**：DeepSeek

---

## 背景

OmniPeople 基于 Salesforce，API 层使用 **Salesforce REST API**。
团队的 `salesforceAPI.py` 文件封装了基础连接逻辑。

---

## Lab 8-A：理解现有 API 工具（5 min）

打开项目根目录的 `salesforceAPI.py`，快速阅读：
- 这个文件提供了哪些方法？
- 认证方式是什么？
- 如何发起一个 SOQL 查询？

---

## Lab 8-B：用 AI 为 Salesforce API 生成测试（20 min）

发送以下 Prompt：

```
你是一名 Salesforce API 测试专家，熟悉 Salesforce REST API。
我需要对以下场景编写 API 测试：

场景：验证 New Hire Part-time 入职申请提交后，
Salesforce 中的 Employment__c 记录被正确创建。

API 信息：
- 使用 Salesforce REST API
- 查询接口：GET /services/data/v58.0/query?q=[SOQL]
- 认证：OAuth 2.0 Bearer Token（已封装在 salesforceAPI.py 中）

验证内容：
- Employment__c.Status__c = "Pending Approval"
- Employment__c.EmployeeType__c = "Part-time"
- Employment__c.ContractType__c = "NonPromoter"

请生成：
1. 查询 Employment__c 的 SOQL（查找最近 1 小时内创建的记录）
2. pytest 测试函数（验证响应体中的关键字段）
3. Pydantic 模型（验证响应结构）

注意：SOQL 中不支持 SELECT *，必须列出字段名。
```

---

## Lab 8-C：AI 辅助分析 API 测试覆盖缺口（10 min）

发送以下 Prompt：

```
我们当前的 OmniPeople 测试主要通过 Playwright UI 自动化验证。
对于以下功能，请分析哪些场景应该补充 API 层测试（而不是 UI 测试）：

1. New Hire 数据提交到 Salesforce 的一致性验证
2. 审批通过后，员工状态自动更新
3. 权限控制（非 Manager 角色能否创建 New Hire）
4. 批量操作性能（同时提交 10 个 New Hire 申请）

对每个场景，说明：
- 为什么这个场景适合 API 测试而非 UI 测试
- 推荐测试的 API 端点和验证内容
- 预期的响应时间基线是多少
```

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
