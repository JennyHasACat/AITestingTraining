# M7 — AI 辅助 Playwright 自动化脚本生成

> **时长**：2 小时 | **受众**：自动化工程师必修，手工测试建议了解 | **前置要求**：M1–M3

---

## 学习目标

完成本模块后，你能够：
1. 将手动测试步骤转化为可运行的 Playwright Python 脚本初稿
2. 使用 AI 生成符合 Page Object Model（POM）规范的定位器代码
3. 识别并修复 AI 生成脚本中的常见问题（动态选择器、缺少等待）
4. 使用 GitHub Copilot 在 IDE 内实时辅助脚本编写

---

## 第一节：为什么自动化脚本要用 AI 辅助？（15 min）

### 传统方式的痛点

```
手动测试步骤 → 脑力转化为代码 → 选择器调试 → 等待策略 → 断言编写
耗时：半天 ~ 1天（对于复杂场景）
```

### AI 辅助后的流程

```
手动步骤 + 页面元素信息 → AI 生成初稿 → 运行验证 → 修复定位器/等待 → 完成
耗时：30分钟 ~ 2小时
```

### AI 擅长 vs 需要人工处理

| AI 擅长 | 需要人工处理 |
|---------|------------|
| 脚本结构和框架代码 | 稳健的 UI 定位器（AI 容易用动态 class） |
| Page Object 类的骨架 | 等待策略（何时等待，等待什么） |
| 基础断言框架 | 业务相关的断言（预期值确认） |
| pytest fixture 模板 | 跨步骤的数据依赖处理 |

---

## 第二节：手动步骤转 Playwright 脚本（30 min）

### 模板 AUTO-01：手动步骤转脚本

```
你是一名 Playwright Python 自动化测试专家，使用 pytest 框架。
项目约定：
- 使用 Page Object Model（POM）
- 定位器优先使用语义化选择器（role、aria-label、data-testid）
- 所有交互前必须加显式等待（不使用 sleep）
- 使用 page.locator() 而非 page.find_element()

以下是一段手动测试步骤：
[粘贴手动步骤]

相关页面元素（提供你知道的）：
[提供 aria-label、data-testid、role 等信息，如果有的话]

请生成：
1. Page Object 类（包含定位器和操作方法）
2. pytest 测试函数（使用 async/await）
3. 每个定位器旁边加注释说明选择该定位器的理由
```

---

### 实际示例

手动步骤输入：
```
测试：用户登录功能
1. 打开 https://app.example.com/login
2. 在邮箱字段输入 test@company.com
3. 在密码字段输入 TestPass123!
4. 点击"登录"按钮
5. 验证页面跳转到 /dashboard，且顶部显示用户姓名
```

AI 生成的 POM 框架（示例）：
```python
# page_objects/login_page.py
from playwright.async_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # 语义化定位器 - 优先 role + name
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="登录")
    
    async def login(self, email: str, password: str):
        await self.page.goto("https://app.example.com/login")
        await self.email_input.fill(email)
        await self.password_input.fill(password)
        await self.login_button.click()
        # 等待导航完成
        await self.page.wait_for_url("**/dashboard")
```

---

## 第三节：常见 AI 脚本问题修复（30 min）

### 问题 1：动态 class 选择器（最常见！）

❌ AI 经常生成：
```python
self.submit_button = page.locator('.btn.btn-primary.sc-3dk8 button')
```

✅ 应该改为：
```python
# 方案 1: data-testid（最稳健）
self.submit_button = page.locator('[data-testid="submit-btn"]')
# 方案 2: role + name（语义化）
self.submit_button = page.get_by_role("button", name="提交")
# 方案 3: aria-label
self.submit_button = page.locator('[aria-label="提交申请"]')
```

**修复 Prompt**：
```
你生成的定位器 .btn.btn-primary.sc-3dk8 使用了动态 CSS 类，不够稳健。
请检查页面元素，推荐优先使用：
1. data-testid 属性
2. role + accessible name
3. aria-label 属性
4. 稳定的 id 属性
5. 最后才考虑 CSS 类（只用稳定的语义化类名）

请更新上面的定位器，并说明为什么选择这个替代方案。
```

---

### 问题 2：缺少等待

❌ AI 经常生成：
```python
await page.click('#submit')
await page.locator('.result').is_visible()
```

✅ 应该改为：
```python
await page.locator('[data-testid="submit-btn"]').click()
# 等待响应后出现的元素
await page.locator('[data-testid="success-message"]').wait_for(state="visible")
```

**修复 Prompt**：
```
请检查上面的脚本，找出所有可能存在竞态条件的地方（点击后直接操作下一步，没有等待过渡）。
对每处加入合适的显式等待：
- 等待元素可见：wait_for(state="visible")
- 等待导航完成：wait_for_url()
- 等待网络请求：wait_for_response() 或 wait_for_load_state()
不要使用 asyncio.sleep()
```

---

### 问题 3：断言太弱

❌ AI 经常生成：
```python
assert await page.locator('.result').is_visible()  # 只验证存在
```

✅ 应该改为：
```python
# 验证具体内容
await expect(page.locator('[data-testid="user-greeting"]')).to_contain_text("欢迎，张三")
# 验证 URL
await expect(page).to_have_url(re.compile(".*/dashboard"))
# 验证元素属性
await expect(page.locator('[data-testid="status-badge"]')).to_have_attribute("data-status", "approved")
```

---

## 第四节：GitHub Copilot IDE 内辅助（15 min）

### 使用方式

在 VS Code 中，Copilot 的最高效用法是**在注释中写意图，让 Copilot 补全代码**：

```python
class NewHirePage:
    def __init__(self, page: Page):
        # 点击新员工类型下拉框
        # Copilot 会在这里补全定位器代码
        
    async def select_employee_type(self, emp_type: str):
        # 选择员工类型，支持 'full-time' 和 'part-time'
        # Copilot 会补全 await self.xxx.select_option(emp_type)
```

### Copilot 快捷键

| 操作 | 快捷键 |
|------|--------|
| 接受建议 | `Tab` |
| 查看多个建议 | `Alt + ]` / `Alt + [` |
| 拒绝建议 | `Esc` |
| 触发建议 | `Ctrl + Enter`（打开 Copilot 面板） |

---

## 本模块小结

| 问题 | 解决方案 |
|------|---------|
| 手动步骤→脚本 | 模板 AUTO-01 + 提供页面元素信息 |
| 动态选择器 | 改用 data-testid / role / aria-label |
| 缺少等待 | 显式等待修复 Prompt |
| 断言太弱 | expect() 断言升级 |
| IDE 内补全 | GitHub Copilot 注释驱动 |

---

[← 返回课程目录](../../README.md) | [→ 进入实战 Lab](lab-generic.md) | [→ 做测验](quiz.md)
