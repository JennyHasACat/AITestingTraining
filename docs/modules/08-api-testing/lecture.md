# M8 — API 测试 + 自动化进阶

> **时长**：2 小时 | **受众**：自动化 / API 工程师 | **前置要求**：M1–M3 + M7 建议

---

## 学习目标

完成本模块后，你能够：
1. 用 AI 从 API 文档或 Postman Collection 快速生成 pytest API 测试脚本
2. 设计覆盖正向、异常和边界的 API 测试场景
3. 用 AI 辅助编写 Pydantic 数据模型进行响应体验证
4. 将 API 测试与 Playwright E2E 测试集成（API Setup + UI 验证）

---

## 第一节：AI 辅助 API 测试的价值（15 min）

### 典型 API 测试痛点

- 手写 requests 代码重复度高
- 响应体断言写得不够完整（只验证状态码）
- 测试数据依赖难以管理
- 接口文档更新时，测试代码同步滞后

### AI 能解决的问题

| 痛点 | AI 方案 |
|------|---------|
| 重复 requests 代码 | 一次生成完整 pytest 测试函数 |
| 断言不完整 | 让 AI 生成 Pydantic 响应模型 + 字段级验证 |
| 测试场景不全 | 用 AI 枚举所有边界和异常场景 |
| 接口变更同步 | 粘贴新文档，让 AI 生成差异更新 |

---

## 第二节：API 测试脚本生成（35 min）

### 模板 API-01：从接口描述生成测试函数

```
你是一名 API 测试专家，使用 Python requests + pytest。
以下是一个 API 接口的描述：

接口名称：[接口名]
方法：[GET/POST/PUT/DELETE]
URL：[路径，如 /api/v1/employees]
认证方式：[Bearer Token / API Key / 无]
请求体（如果有）：[JSON 格式示例]
响应示例（成功）：[JSON 格式]
已知的错误场景：[如：缺少必填字段返回 400；未授权返回 401]

请生成 pytest 测试函数，覆盖：
1. 正常场景（成功响应）
2. 缺少必填字段（400 错误）
3. 未授权访问（401 错误）
4. 数据不存在（404 错误，如果适用）

要求：
- 使用 requests.Session 复用认证
- 断言包括：状态码 + 响应体关键字段 + 响应时间 < 2 秒
- 使用 pytest.mark.parametrize 合并相似测试
```

---

### 模板 API-02：Pydantic 响应体验证模型

```
以下是一个 API 的响应体 JSON 示例：
[粘贴响应 JSON]

请生成对应的 Pydantic v2 数据模型，要求：
- 所有字段使用正确的类型注解
- 可选字段使用 Optional
- 嵌套对象用独立的 Pydantic 类表示
- 对关键字段加上 Field(description="...")

然后生成一个使用这个模型验证 API 响应的 pytest 测试函数。
```

---

### 示例：员工创建 API

接口信息输入：
```
POST /api/v1/employees
Authorization: Bearer {token}
Request Body:
{
  "firstName": "张三",
  "lastName": "Zhang",
  "email": "zhangsan@company.com",
  "employeeType": "PART_TIME",
  "weeklyHours": 20
}
Response (201 Created):
{
  "id": "emp_001",
  "status": "PENDING_APPROVAL",
  "createdAt": "2024-01-15T08:30:00Z"
}
```

AI 生成的 Pydantic 模型（示例）：
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CreateEmployeeResponse(BaseModel):
    id: str = Field(description="员工 ID，格式：emp_xxx")
    status: str = Field(description="初始状态，应为 PENDING_APPROVAL")
    created_at: datetime = Field(alias="createdAt")
    
    model_config = {"populate_by_name": True}
```

---

## 第三节：API + UI 集成测试模式（20 min）

### 场景：API 准备数据，Playwright 验证 UI

```python
# conftest.py - 使用 API 快速创建测试数据
@pytest.fixture
async def created_employee(api_client):
    """通过 API 创建测试员工，测试结束后清理"""
    response = api_client.post("/api/v1/employees", json={
        "firstName": "TEST",
        "email": "test_auto@testdomain.com",
        "employeeType": "PART_TIME"
    })
    employee_id = response.json()["id"]
    yield employee_id
    # Teardown：API 删除
    api_client.delete(f"/api/v1/employees/{employee_id}")
```

**AI 生成 fixture 的 Prompt**：
```
我需要一个 pytest async fixture，通过 API 创建测试员工数据，
测试结束后自动通过 API 删除。
API 信息：POST /api/v1/employees，DELETE /api/v1/employees/{id}
认证：Bearer token 从环境变量 API_TOKEN 读取
请生成 fixture，使用 yield 模式区分 setup 和 teardown。
```

---

## 第四节：性能基线验证（10 min）

### 简单响应时间断言

```python
import time

def test_api_response_time():
    start = time.time()
    response = requests.get("/api/v1/employees")
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 2.0, f"响应时间 {elapsed:.2f}s 超过 2s 基线"
```

**AI Prompt**：
```
请为上面的 API 测试集合添加响应时间断言：
- 普通列表接口：< 2 秒
- 创建操作：< 3 秒
- 批量操作：< 10 秒
使用 pytest 的 @pytest.mark.slow 标记性能测试用例。
```

---

## 第五节：AI 提效小工具 —— API 自动化（10 min）

> 待补充：具体工具 / 链接 / 进阶用法（由维护者持续更新）

### 它解决什么问题

把"从接口文档生成单个测试函数"升级为**批量**：导入一个 Postman Collection / OpenAPI Spec，工具自动为每个接口生成 pytest 测试（正向 + 异常 + 边界），并配套 Pydantic 模型与 fixture。

### 核心思路（伪步骤）

```
1. 输入：OpenAPI Spec / Postman Collection / 接口文档
2. 工具：解析接口 → 套用 API-01 / API-02 生成测试函数与响应模型
3. 增强：自动加边界场景、参数化、认证 fixture
4. 输出：整套可运行 API 测试 + 覆盖率报告
```

提示词骨架（工具底层常封装的逻辑）：

```
你是 API 测试专家。基于以下 OpenAPI Spec 片段生成 pytest 测试：
[粘贴 Spec]
要求：
- 每个接口覆盖：正常 200 + 必填缺失 400 + 未授权 401
- 用 requests.Session 复用认证（Token 从环境变量读）
- 生成对应 Pydantic 响应模型做字段级断言
- 用 parametrize 合并相似场景
```

### 注意事项

- 自动生成的断言默认偏浅，关键业务字段需人工补强；
- Spec 更新后重新生成，注意保留团队自定义部分（避免覆盖）。

---

## 本模块小结

| 场景 | Prompt 模板 |
|------|------------|
| 从接口文档生成测试函数 | API-01（测试函数生成） |
| 响应体结构化验证 | API-02（Pydantic 模型） |
| API + UI 集成 | fixture yield 模式 |
| 性能基线验证 | 响应时间断言 |

---

[← 返回课程目录](../../README.md) | [→ 进入实战 Lab](lab-generic.md) | [→ 做测验](quiz.md)
