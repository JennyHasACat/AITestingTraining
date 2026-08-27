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
- 若你的目标不是迁出 Postman、而是留在 Postman 里批量造数（参数化 + 上下游传参 + Runner 迭代），见第六节 TOOL-postman-param —— 两条路线互补。

---

## 第六节：AI 提效小工具 —— Postman Collection 参数化生成（10 min，选学）

> 工具 ID：TOOL-postman-param ｜ 索引：[AI 提效工具箱](../../toolbox.md) ｜ 资产：仓库 `tools/postman-param/`

### 它解决什么问题

Postman 导出的 Collection 参数全部硬编码：姓名、手机号、时间段、`request_id` 全是定值。想用 Collection Runner 批量跑 250 轮造测试数据，结果是 250 条一模一样的重复数据；接口之间的 ID 传递（创建 → 更新 → 预约）还得手动复制。手动改几十上百个请求不现实 —— 让 AI 直接在原 JSON 里"反写"完成改造，产出一个导入即用的新 Collection。

### 核心思路 / 提示词骨架

```
1. 角色 + 目标：资深 Postman 脚本专家，对 collection JSON 做"反写"改造，
   支持 Collection Runner 批量迭代造数（如 250 次）
2. 数据流转：下游接口需要的 ID/字段，用 Tests 脚本 pm.environment.set 提取传递；
   跨接口一致性字段（如 parent_name）声明"必须与接口 A 完全一致"
3. 动态自增：手机号/姓名从起始值按迭代自增（Pre-request 计算 + 环境变量记数），
   明确位数格式（如 5 位补零）
4. 时间滑动：基准时间 + 步长（如每次 +15min），Pre-request 动态计算
5. 工程化锁死项：所有接口必须有 Tests（消除 "No tests found" 警告）；
   直接在原 JSON 内改写，不输出额外文件；除 Environment 初始变量外零手工配置
6. 反向交付物：要求 AI 输出【环境变量初始化清单】Markdown 表格，
   导入后照着配一遍即可运行
```

完整 Prompt 原文见仓库 `tools/postman-param/prompt.md`；该工具为**纯提示词型**（无脚本），Prompt 即全部资产。

### 使用示例

`tools/postman-param/sample/` 下有一对脱敏样例（线索创建 → 更新 → 预约 三接口链路）：

| 文件 | 状态 |
|------|------|
| `collection-before.json` | 改造前：姓名/手机号/时间段硬编码、`request_id` 固定、test 是占位脚本或无 |
| `collection-after.json` | 改造后：Pre-request 算自增与滑动时间、Tests 提取 `leadId` 传下游、`{{$guid}}` 动态 UUID、每请求都有正式断言 |

导入两个文件对比 diff，是最直观的"AI 到底改了什么"。

### 注意事项

- **防 JSON 结构破坏**：要求 AI 输出合法 Collection v2.1 schema，导入前先过 JSON lint（AI 偶尔会截断或产出非法 JSON）；
- **认清网关包装结构**：样例 Collection 所有请求的 URL 都是同一个网关，真实 endpoint 藏在 body 的 `url` / `http_method` 字段里 —— Prompt 里最好点明，否则 AI 可能改错层；
- **敏感信息先占位**：真实 Collection 含密钥与内部域名，发给 AI 前替换成 `{{app_secret}}` 这类占位符，导入后再通过环境变量配回；
- **与第五节的路线分工**：本节留在 Postman 生态（Runner 批量造数、轻量验证）；要纳入 CI 每日回归，用第五节「Collection → pytest」路线。两者互补，按需选用。

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
