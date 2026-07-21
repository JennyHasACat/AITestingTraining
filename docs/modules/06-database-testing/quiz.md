# M6 测验 — 数据库测试 + AI 辅助 SQL

> **题目数量**：7 题 | **建议时间**：8 分钟 | **通过标准**：5 题正确

---

## 选择题（单选，每题 1 分）

**Q1. 为什么 UI 测试通过后，仍然需要做数据库层面的验证？**

- A. 界面显示正确不能保证数据库中的数据存储正确
- B. 数据库验证比 UI 测试速度更快
- C. 测试工具无法测试 UI 层
- D. UI 层的测试不算真正的测试

<details markdown="1"><summary>查看答案</summary>

**答案：A**

解析：前端可能对数据做展示层的格式化或缓存处理，展示正确不代表底层存储正确。特别是金额、日期格式、状态值等，数据库值与显示值可能有映射转换，必须单独验证。

</details>

---

**Q2. 在 AI 生成的测试数据 INSERT SQL 中，以下哪项安全措施最重要？**

- A. 使用存储过程包装 INSERT
- B. 在测试数据中加入明显的标识前缀（如 TEST_），便于识别和清理
- C. 每次 INSERT 后立即 COMMIT
- D. 使用随机生成的 UUID 作为主键

<details markdown="1"><summary>查看答案</summary>

**答案：B**

解析：测试数据标识前缀（如 TEST_、AUTO_TEST_ 等）是最关键的安全措施，它让测试数据可以被精确识别和清理，避免意外删除真实数据。UUID 主键是好习惯但不是最重要的安全措施；存储过程和 COMMIT 是数据库操作规范。

</details>

---

**Q3. 以下哪条 AI 生成的 SQL 应该立即被拒绝执行？**

- A. `SELECT id, status FROM users WHERE email = 'test@test.com'`
- B. `DELETE FROM logs WHERE created_at < '2024-01-01'`
- C. `DELETE FROM employees`
- D. `UPDATE test_users SET status='ACTIVE' WHERE username LIKE 'TEST_%'`

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：`DELETE FROM employees` 没有 WHERE 条件，会删除整张表的所有数据，这是极度危险的写法。无论是生产还是测试环境都不应该执行。AI 有时会生成这类危险 SQL，必须人工审查。

</details>

---

**Q4. SOQL（Salesforce Object Query Language）与标准 SQL 的主要区别是？**

- A. SOQL 不支持 WHERE 条件过滤
- B. SOQL 不支持 SELECT *，必须明确列出字段名
- C. SOQL 只能查询不能过滤
- D. SOQL 使用 JOIN 关键字进行多表关联

<details markdown="1"><summary>查看答案</summary>

**答案：B**

解析：Salesforce SOQL 的主要特点：不支持 `SELECT *`（必须列出字段），多表关联通过关系字段导航实现（不用 JOIN），语法整体与 SQL 类似。这是团队在使用 AI 生成 Salesforce 查询时需要特别在 Prompt 中说明的。

</details>

---

## 判断题（T/F，每题 1 分）

**Q5. AI 生成的 SELECT 查询可以不经过人工审查直接运行在测试数据库上。**

<details markdown="1"><summary>查看答案</summary>

**答案：F（错误）**

解析：虽然 SELECT 是只读操作，但仍然需要确认：① 连接的是正确的环境（测试环境而非生产）；② WHERE 条件是否正确（避免返回错误数据集）；③ 是否会导致大量数据被读取（影响数据库性能）。全部读操作都应该人工确认环境。

</details>

---

**Q6. 测试的 Teardown SQL 应该在被测功能执行前运行。**

<details markdown="1"><summary>查看答案</summary>

**答案：F（错误）**

解析：正确的执行顺序是：Setup（准备数据）→ 执行被测功能 → Verify（验证结果）→ Teardown（清理数据）。Teardown 在最后运行，目的是清理本次测试产生的数据，避免影响后续测试。

</details>

---

## 简答题（1 题，4 分）

**Q7. 请写出用 AI 生成"测试数据验证 SQL"时，Prompt 中必须包含的 4 项信息，并说明每项的必要性。**

<details markdown="1"><summary>参考答案</summary>

（每项 1 分，共 4 分）

1. **数据库类型（MySQL/PostgreSQL/SOQL 等）**：不同数据库 SQL 方言有差异，如 MySQL 用 `LIMIT`，SQL Server 用 `TOP`，Salesforce 用 SOQL 不支持 `SELECT *`。

2. **表名和字段名（最好提供 CREATE TABLE 或字段列表）**：AI 无法猜测你的表结构，提供准确结构才能生成正确的列名和数据类型检查。

3. **提交的测试数据值**：AI 需要知道你期望哪些值被存入数据库，才能生成针对性的 WHERE 条件和断言。

4. **明确说明只生成 SELECT（不要写操作）**：安全约束，防止 AI 擅自生成 UPDATE/DELETE，增加误操作风险。

</details>

---

[← 返回课件](lecture.md) | [← Lab](lab-generic.md) | [→ 进入 M7](../07-automation-playwright/lecture.md)
