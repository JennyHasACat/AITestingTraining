# M6 — 数据库测试 + AI 辅助 SQL

> **时长**：1.5 小时 | **受众**：全员推荐（自动化工程师必修）| **前置要求**：M1 + M2

---

## 学习目标

完成本模块后，你能够：
1. 用 AI 快速编写用于验证测试结果的 SQL 查询
2. 使用 AI 设计测试数据的 Setup 和 Teardown SQL
3. 借助 AI 分析数据库层面的 Bug（数据不一致/脏数据）
4. 安全地在测试中使用 AI 辅助 SQL（避免误操作生产数据）

---

## 第一节：数据库在测试中的角色（15 min）

### 什么时候需要直接查数据库？

| 场景 | 为什么需要 DB 验证 |
|------|-----------------|
| UI/API 提交后验证数据持久化 | 界面显示正确不代表存储正确 |
| 测试数据准备 | 快速生成特定状态的测试数据 |
| 数据清理（Teardown） | 防止测试污染其他用例 |
| Bug 根因分析 | 确认是前端显示问题还是数据库问题 |
| 回归验证 | 核心字段的数据一致性检查 |

### 安全原则（重要！）

> ⚠️ **严禁在生产数据库执行写操作（INSERT/UPDATE/DELETE）**  
> ⚠️ 所有 AI 生成的 SQL，运行前必须 **人工审查**  
> ⚠️ 测试环境 SQL 和生产 SQL 要严格区分  
> ✅ 只读查询（SELECT）相对安全，但仍需确认连接的是正确环境

---

## 第二节：测试验证 SQL 生成（25 min）

### 模板 DB-01：UI 提交后的数据验证 SQL

```
你是一名数据库测试专家，熟悉 MySQL/PostgreSQL。
我刚完成了一个 [功能] 的 UI 测试，
表单提交的数据应该存储在 [表名] 表中。

表结构（如果知道，提供 CREATE TABLE 语句或字段列表）：
[表结构信息]

提交的测试数据：
[提交的字段值]

请生成 SQL 查询，验证：
1. 记录是否成功插入
2. 关键字段值是否与提交值一致
3. 系统自动填充的字段（如创建时间、状态默认值）是否正确

注意：只生成 SELECT 查询，不要生成写操作。
```

---

### 模板 DB-02：测试数据准备 SQL

```
你是一名测试数据工程师。
我需要为以下测试场景准备测试数据：
场景描述：[描述你的测试场景，如"一个已过期的积分记录"]
相关表：[表名 + 关键字段]

请生成：
1. INSERT 语句（创建测试所需的初始数据）
2. 验证数据已正确插入的 SELECT 查询
3. 测试完成后的 DELETE/UPDATE 清理语句（Teardown）

注意：
- 生成的 INSERT 使用明显的测试标识（如用户名包含"TEST_"前缀）
- 提供运行顺序：先 INSERT，执行测试，最后 Teardown
```

---

### 模板 DB-03：数据不一致 Bug 分析

```
你是一名数据库调试专家。
我发现前端显示的数据与预期不符，需要在数据库层面排查。
现象描述：[描述前端和数据库之间的不一致]
相关表（猜测）：[表名]

请帮我生成排查 SQL：
1. 查询最新插入/更新的记录（确认数据存储状态）
2. 跨表关联查询（如果涉及外键关联）
3. 检查是否有触发器或约束可能改变了数据
```

---

## 第三节：常见测试场景 SQL 模式（20 min）

### 3.1 验证记录存在且状态正确

```sql
-- 通用模式：验证插入后的状态
SELECT id, status, created_at, updated_at
FROM employees
WHERE email = 'test@company.com'
  AND status = 'PENDING_APPROVAL'
ORDER BY created_at DESC
LIMIT 1;
```

**AI 追问技巧**：
```
上面的查询，如果我需要同时验证关联表（如 employee_contracts）中的记录也已创建，
请生成 JOIN 版本。
```

---

### 3.2 清理测试数据（Teardown）

```sql
-- 安全的测试数据清理（只删除带 TEST 标识的数据）
DELETE FROM employees
WHERE email LIKE 'TEST_%@testdomain.com'
  AND created_at > NOW() - INTERVAL 1 HOUR;
```

**AI 生成注意点**：
- 始终加上 `WHERE` 条件，绝不允许裸 `DELETE FROM table`
- 加时间范围限制，防止误删历史测试数据
- 运行前先用 `SELECT` 确认要删除的数据范围

---

### 3.3 边界数据查询

```sql
-- 查找特定边界状态的记录（如即将过期的积分）
SELECT user_id, points, expire_date, DATEDIFF(expire_date, NOW()) AS days_remaining
FROM user_points
WHERE expire_date BETWEEN NOW() AND NOW() + INTERVAL 7 DAY
  AND points > 0
ORDER BY expire_date ASC;
```

---

## 第四节：AI SQL 辅助的局限性（10 min）

| 局限性 | 说明 | 应对方式 |
|--------|------|---------|
| AI 不知道你的实际表结构 | 生成的 SQL 列名/表名可能错误 | 提供真实的 CREATE TABLE 语句 |
| AI 可能使用错误的 SQL 方言 | MySQL 和 PostgreSQL 某些语法不同 | 在 Prompt 中明确数据库类型 |
| AI 无法验证 SQL 正确性 | 生成的 SQL 必须本地运行验证 | 先在测试环境运行，再用于自动化 |
| AI 可能生成不安全的 DELETE | 没有 WHERE 条件的批量删除 | 人工审查所有写操作 SQL |

---

## 本模块小结

| 场景 | Prompt 模板 |
|------|------------|
| 验证 UI 提交数据 | DB-01（数据验证 SQL） |
| 准备测试数据 | DB-02（测试数据 Setup/Teardown） |
| 排查数据不一致 | DB-03（数据一致性排查） |
| 安全规则 | 永远 SELECT 先行，写操作必须人工审查 |

---

[← 返回课程目录](../../README.md) | [→ 进入实战 Lab](lab-generic.md) | [→ 做测验](quiz.md)
