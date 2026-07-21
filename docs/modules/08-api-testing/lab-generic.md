# M8 实战 Lab — 通用版：AI 生成 API 测试脚本

> **预计时长**：45 分钟 | **工具**：DeepSeek

---

## Lab 8-A：生成完整 API 测试集（25 min）

使用以下接口信息，生成完整 pytest 测试文件：

```
接口：用户登录
POST /api/v1/auth/login
认证：无（这就是获取 token 的接口）

请求体：
{
  "email": "string",
  "password": "string"
}

成功响应 (200)：
{
  "token": "eyJhbGci...",
  "expiresIn": 3600,
  "user": {
    "id": "usr_001",
    "email": "user@company.com",
    "role": "ADMIN"
  }
}

已知错误场景：
- 密码错误 → 401，{"error": "INVALID_CREDENTIALS"}
- 邮箱格式错误 → 400，{"error": "INVALID_EMAIL_FORMAT"}
- 缺少 password 字段 → 400，{"error": "MISSING_REQUIRED_FIELD"}
- 账号不存在 → 404，{"error": "USER_NOT_FOUND"}
- 账号被锁定 → 403，{"error": "ACCOUNT_LOCKED"}
```

### 你的 Prompt（使用 API-01 模板）：

```
[在此填写]
```

### AI 生成的测试文件：

```python
# [粘贴 AI 输出]
```

### Review 检查：

- [ ] 覆盖了成功场景和 5 个错误场景
- [ ] 状态码断言完整
- [ ] 响应体关键字段有验证（token 存在、user.role 正确等）
- [ ] 响应时间断言 < 2 秒
- [ ] 测试数据没有硬编码真实密码（使用环境变量或占位符）

---

## Lab 8-B：生成 Pydantic 响应验证模型（15 min）

针对上面接口的成功响应，使用 **模板 API-02** 生成 Pydantic 模型：

```
{
  "token": "eyJhbGci...",
  "expiresIn": 3600,
  "user": {
    "id": "usr_001",
    "email": "user@company.com",
    "role": "ADMIN"
  }
}
```

**AI 生成的 Pydantic 模型**：
```python
# [粘贴 AI 输出]
```

**验证问题**：
1. `expiresIn` 应该是正整数（> 0），Pydantic 模型如何约束这个条件？
2. `user.role` 只能是 `ADMIN`/`EDITOR`/`VIEWER`，如何用 Enum 表示？

发送追问 Prompt，让 AI 补充这两个约束。

---

## Lab 8-C：API + UI 集成 fixture（5 min）

发送以下 Prompt，生成 OmniPeople 风格的 API Setup fixture：

```
我需要一个 pytest fixture（async，带 yield teardown），
通过调用 API 创建测试员工数据，测试结束后自动删除。

API：
- 创建：POST /api/employees，响应包含 {"id": "emp_xxx"}
- 删除：DELETE /api/employees/{id}
- 认证：从 os.environ["API_TOKEN"] 读取

要求：
- 使用 httpx.AsyncClient（异步版 requests）
- fixture scope = "function"（每个测试用例独立数据）
- 创建的员工 email 包含 "TEST_" 前缀
```

---

[← 返回课件](lecture.md) | [→ OmniPeople 定制版](lab-omnipeople.md) | [→ 做测验](quiz.md)
