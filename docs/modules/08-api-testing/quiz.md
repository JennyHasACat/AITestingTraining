# M8 测验 — API 测试 + 自动化进阶

> **题目数量**：6 题 | **建议时间**：8 分钟 | **通过标准**：4 题正确

---

## 选择题（单选，每题 1 分）

**Q1. 以下哪种断言方式在 API 测试中最完整？**

- A. `assert response.status_code == 200`
- B. `assert response.json()["status"] == "success"`
- C. `assert response.status_code == 201 and CreateEmployeeResponse(**response.json())` 加响应时间检查
- D. `assert len(response.text) > 0`

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：完整的 API 断言应包含：① 状态码；② 响应体结构验证（Pydantic 模型）；③ 关键字段值；④ 响应时间。只检查状态码是不够的，因为服务器可能返回 200 但响应体数据错误。

</details>

---

**Q2. 使用 pytest fixture yield 模式进行 API 测试数据管理的主要优势是什么？**

- A. 让测试代码更简洁
- B. 确保测试数据在 setup 阶段创建，在 teardown 阶段自动清理，防止数据污染
- C. 提高 API 请求的执行速度
- D. 自动生成测试报告

<details markdown="1"><summary>查看答案</summary>

**答案：B**

解析：`yield` fixture 的核心价值是**测试隔离**——每个测试用例使用干净的独立数据，测试结束后自动清理，防止一个测试的数据影响另一个测试，确保测试的可重复性。

</details>

---

**Q3. 什么情况下应该优先使用 API 测试而非 UI 测试？**

- A. 需要验证页面布局和视觉效果
- B. 验证跨浏览器兼容性
- C. 验证后端数据持久化逻辑、性能基线、权限控制
- D. 测试用户交互流程的完整性

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：API 测试比 UI 测试速度快 10–100 倍，更适合：数据层验证（确认存储正确）、性能测试（响应时间）、权限控制（直接测试 API 权限规则）。UI 测试更适合用户流程验证和前端交互测试。

</details>

---

## 判断题（T/F，每题 1 分）

**Q4. 在 API 测试脚本中，应该直接在代码中硬编码测试账号的密码。**

<details markdown="1"><summary>查看答案</summary>

**答案：F（错误）**

解析：密码和 token 等敏感凭证必须通过环境变量（`os.environ["PASSWORD"]`）或 `.env` 文件读取，不能硬编码在代码中。硬编码凭证一旦提交到 Git 仓库，就构成安全漏洞。

</details>

---

**Q5. Pydantic 模型不仅能验证响应字段是否存在，还能验证字段的类型和取值范围。**

<details markdown="1"><summary>查看答案</summary>

**答案：T（正确）**

解析：Pydantic v2 支持复杂的类型验证：`int`/`str`/`datetime`/`Optional` 等类型检查，`Field(gt=0)` 等数值范围约束，`Enum` 枚举值约束，以及自定义 validator。这使得 API 响应的结构化验证比手写 `assert` 更系统完整。

</details>

---

## 简答题（1 题，5 分）

**Q6. 你需要测试一个"员工信息更新"的 API（PUT /api/employees/{id}），请列出至少 5 个需要覆盖的测试场景，并对每个场景说明期望的 HTTP 状态码。**

<details markdown="1"><summary>参考答案</summary>

（每个场景 1 分，共 5 分）

1. **正常更新成功**：提供有效 ID + 有效请求体 → 200 OK
2. **员工 ID 不存在**：提供不存在的 ID → 404 Not Found
3. **未授权访问**：请求头缺少 token 或 token 过期 → 401 Unauthorized
4. **权限不足**：使用非管理员 token 请求 → 403 Forbidden
5. **请求体字段验证**：必填字段为空/类型错误 → 400 Bad Request
6. **并发更新同一记录**：两个请求同时修改同一员工 → 其中一个应返回 409 Conflict 或适当处理
7. **只读字段尝试修改**：如 ID、创建时间等不可修改字段 → 400 Bad Request 或系统忽略该字段

（答出 5 个即满分）

</details>

---

[← 返回课件](lecture.md) | [← Lab](lab-generic.md) | [→ 进入 M9](../09-prompt-assets/lecture.md)
