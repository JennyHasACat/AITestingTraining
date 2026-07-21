# M6 实战 Lab — 通用版：AI 辅助数据库测试

> **预计时长**：35 分钟 | **工具**：DeepSeek（SQL 推理最准确）

---

## Lab 6-A：数据验证 SQL 生成（15 min）

### 场景

你刚完成了一个用户注册功能的 UI 测试，
表单提交了以下数据：
- 用户名：`TEST_user_001`
- 邮箱：`test001@testmail.com`
- 角色：`VIEWER`
- 状态：注册后默认 `PENDING`

相关表结构：
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  role ENUM('ADMIN', 'EDITOR', 'VIEWER') DEFAULT 'VIEWER',
  status ENUM('ACTIVE', 'PENDING', 'DISABLED') DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 步骤

使用 **模板 DB-01** 生成验证 SQL，要求验证：
1. 记录已插入
2. email 字段值正确
3. role 默认值为 VIEWER
4. status 默认值为 PENDING
5. created_at 在最近 1 分钟内

**你的 Prompt**：
```
[在此填写]
```

**AI 生成的 SQL**：
```sql
-- [粘贴 AI 输出]
```

**人工 Review 检查**：
- [ ] SELECT 语句语法正确
- [ ] 没有 WHERE 条件遗漏
- [ ] 可以在测试数据库安全运行

---

## Lab 6-B：测试数据 Setup + Teardown（15 min）

### 场景

你需要测试一个"账号锁定后自动解锁"的功能，
要求在数据库中存在一个锁定状态 = `LOCKED`，且锁定时间早于 30 分钟前的用户。

使用 **模板 DB-02** 生成：

```
你是一名测试数据工程师，数据库类型：MySQL。
我需要为以下测试场景准备数据：
场景：账号在 30 分钟前被锁定，现在应该自动解锁。
表结构：
users 表：id, email, status, locked_at (TIMESTAMP, 账号锁定时间)

请生成：
1. INSERT 语句（模拟 30 分钟前锁定的账号）
2. 验证 SELECT（确认数据已创建且 locked_at 正确）
3. Teardown DELETE（清理这条测试数据）

安全要求：INSERT 的 email 必须包含 "TEST_" 前缀
```

**AI 生成的 SQL（3条）**：
```sql
-- Setup INSERT:

-- Verify SELECT:

-- Teardown DELETE:
```

**执行顺序确认**：
1. 运行 INSERT（Setup）
2. 运行被测功能
3. 运行 SELECT（验证功能结果）
4. 运行 DELETE（Teardown）

---

## Lab 6-C：识别不安全的 SQL（5 min）

以下 3 条 AI 生成的 SQL，哪些存在风险？

```sql
-- SQL 1:
DELETE FROM sessions WHERE user_id = 100;

-- SQL 2:
DELETE FROM test_data;

-- SQL 3:
SELECT * FROM orders WHERE status = 'PENDING' AND created_at > '2024-01-01';
```

| SQL | 是否安全？ | 问题说明 |
|-----|---------|---------|
| SQL 1 | | |
| SQL 2 | | |
| SQL 3 | | |

<details>
<summary>参考答案</summary>

- **SQL 1**：⚠️ 有风险 — 如果 user_id=100 是生产数据，会删除真实用户会话。应增加时间范围或环境标识条件。
- **SQL 2**：❌ 危险 — 无 WHERE 条件，删除整张表所有数据。这种 SQL 永远不应该执行，AI 不应该生成这种写法。
- **SQL 3**：✅ 安全 — 只读查询，有 WHERE 条件。

</details>

---

[← 返回课件](lecture.md) | [→ OmniPeople 定制版](lab-omnipeople.md) | [→ 做测验](quiz.md)
