# M7 实战 Lab — 通用版：AI 生成 Playwright 脚本

> **预计时长**：50 分钟 | **工具**：DeepSeek + GitHub Copilot（如已配置）

---

## Lab 7-A：手动步骤转 Playwright 脚本（25 min）

### 手动测试步骤（使用以下场景）

```
功能：用户修改个人信息
系统：Web 应用，React 前端

步骤：
1. 已登录状态，进入 /profile/edit 页面
2. 清空"显示名称"字段，输入"新名字"
3. 在"个人简介"字段输入"这是我的简介"
4. 点击"保存更改"按钮
5. 验证页面出现"保存成功"提示
6. 验证页面顶部的用户名显示已更新为"新名字"

页面元素信息（已知）：
- 显示名称输入框：aria-label="Display Name"
- 个人简介文本域：data-testid="bio-textarea"  
- 保存按钮：role="button"，name="保存更改"
- 成功提示：data-testid="success-toast"
- 顶部用户名：data-testid="header-username"
```

### 步骤

使用 **模板 AUTO-01** 生成 POM + 测试函数，**强调**：
- 使用语义化定位器（上面已提供）
- 所有操作前加显式等待
- 断言使用 `expect()` 而非 `assert is_visible()`

**AI 生成的代码**：
```python
# [粘贴 AI 生成的 Page Object]
```

```python
# [粘贴 AI 生成的 test 函数]
```

### 代码 Review 检查

- [ ] 没有使用动态 CSS class 作为定位器
- [ ] 所有 click/fill 操作前有合适的等待
- [ ] 断言使用 `expect()` API
- [ ] 有 `async/await` 关键字
- [ ] 测试函数有 `@pytest.mark.asyncio` 或框架兼容的标记

---

## Lab 7-B：修复 AI 生成的问题代码（20 min）

以下是 AI 生成但存在问题的代码，请用修复 Prompt 让 AI 改进：

```python
# 问题代码（有 3 处需要修复）
class ProfilePage:
    def __init__(self, page):
        self.page = page
        # 问题1：使用了动态 class
        self.name_input = page.locator('.input-field.sc-abc123 input')
        # 问题2：使用了脆弱的 xpath
        self.save_button = page.locator('//div[@class="footer"]/button[2]')
        
    async def save_profile(self, name, bio):
        await self.name_input.click()
        await self.name_input.fill(name)
        # 问题3：没有等待，直接点击
        await self.save_button.click()
        # 问题4：断言太弱
        assert await self.page.locator('.toast').is_visible()
```

**发送给 AI 的修复 Prompt**：
```
以下 Playwright Python 代码存在 3 类问题：
1. 使用了动态 CSS class 和不稳定的 XPath 作为定位器
2. 缺少显式等待
3. 断言使用了 is_visible() 而非 expect()

已知元素信息：
- 名称输入框：aria-label="Display Name"
- 保存按钮：role="button"，name="保存更改"
- 成功提示：data-testid="success-toast"，文字内容为"保存成功"

请修复上面的代码，解释每处修改的理由。
```

---

## Lab 7-C：快速生成 pytest fixture（5 min）

发送以下 Prompt，生成团队可复用的 fixture：

```
你是一名 Playwright pytest 专家。
请生成一个 conftest.py 中的 browser_context fixture，要求：
- 浏览器类型：Chromium
- headed/headless 可通过命令行参数控制（--headed）
- 视窗大小：1280x720
- 每个 test 使用独立的 context（不共享登录状态）
- 支持失败时自动截图（保存到 Screenshots/ 目录）
```

---

[← 返回课件](lecture.md) | [→ OmniPeople 定制版](lab-omnipeople.md) | [→ 做测验](quiz.md)
