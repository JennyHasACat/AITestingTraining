# M6 实战 Lab — OmniPeople 定制版：Salesforce 数据验证 SQL

> **预计时长**：30 分钟 | **工具**：DeepSeek

---

## 重要说明

OmniPeople 基于 Salesforce 平台，底层使用 **Salesforce Object** 存储数据，
标准查询语言为 **SOQL**（Salesforce Object Query Language），而非标准 SQL。  
SOQL 与 SQL 语法类似但有区别：不支持 `*`，必须列出字段名；不支持 `JOIN`（用关系字段导航代替）。

---

## Lab 6-A：生成 SOQL 验证查询（15 min）

### 场景

测试完成 New Hire Part-Time 入职申请提交后，
需要验证 Salesforce 中的 `Contact`（员工记录）和 `Employment__c`（入职申请记录）
是否已正确创建。

发送以下 Prompt 给 DeepSeek：

```
你是一名 Salesforce 测试专家，熟悉 SOQL。
我完成了一个新员工入职申请的提交测试，需要在 Salesforce 中验证数据。

相关 Object：
1. Contact（员工基本信息）：字段包括 FirstName, LastName, Email, Department
2. Employment__c（入职申请）：字段包括 EmployeeType__c, ContractType__c, 
   StartDate__c, WeeklyHours__c, Status__c, Employee__c（关联 Contact 的外键）

测试提交的数据：
- 员工名：Test User
- 邮箱：testuser_pt@test.com
- 员工类型：Part-time
- 合同类型：NonPromoter
- 开始日期：今天

请生成 SOQL 查询，验证：
1. Contact 记录已创建，Email 字段正确
2. Employment__c 记录已创建，EmployeeType__c = 'Part-time'，Status__c = 'Pending Approval'
3. Employment__c 的 Employee__c 正确关联到对应的 Contact

注意：SOQL 不支持 SELECT *，必须列出需要的字段名。
```

---

## Lab 6-B：用 AI 分析 Salesforce 数据不一致（15 min）

### 场景

测试发现：New Hire 申请提交成功后，UI 显示状态为 "Submitted"，
但通过 Salesforce Developer Console 查询，Status__c 字段值为 "Draft"。

发送以下 Prompt：

```
你是一名 Salesforce SDET。
我发现了一个数据不一致的问题：
- UI 显示：状态 = "Submitted"
- 数据库实际值：Status__c = "Draft"

相关 Object：Employment__c
可能的原因：
1. 前端显示了错误的状态映射（UI 显示值 ≠ 数据库值）
2. 触发器（Trigger）或流（Flow）在保存后改变了状态
3. 提交操作未真正触发状态更新

请：
1. 生成 SOQL 查询，查看该记录的完整历史状态变化
   （提示：可以查询 Employment__c 的 LastModifiedDate 和相关 History Object）
2. 列出 3 个可能根因及验证方法
3. 如果是 Salesforce Trigger 导致的，如何快速验证？
```

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
