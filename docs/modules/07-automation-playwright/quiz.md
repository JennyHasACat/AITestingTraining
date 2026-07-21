# M7 测验 — AI 辅助 Playwright 自动化脚本生成

> **题目数量**：7 题 | **建议时间**：8 分钟 | **通过标准**：5 题正确

---

## 选择题（单选，每题 1 分）

**Q1. 以下哪种定位器策略最适合作为 Playwright 的首选？**

- A. `.locator('.btn.btn-primary.sc-xyz123')`（CSS 动态类名）
- B. `.locator('//div[@class="wrapper"]/button[1]')`（XPath 绝对路径）
- C. `.get_by_role("button", name="提交")`（语义化角色定位）
- D. `.locator('#button_3849201')`（动态生成的 ID）

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：语义化定位器（role + name）基于可访问性属性，不受 CSS 框架更新影响，在 UI 重构后仍然稳定。动态 CSS 类和自动生成的 ID 在每次构建或框架升级后可能失效。

</details>

---

**Q2. Playwright 中处理"点击按钮后等待结果页面出现"的正确方式是？**

- A. `await asyncio.sleep(3)`（固定等待 3 秒）
- B. `await page.wait_for_selector('.result')` 加上 `timeout=5000`
- C. `await page.locator('[data-testid="result"]').wait_for(state="visible")`
- D. 循环检查 `is_visible()` 直到返回 True

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：使用 `wait_for(state="visible")` 是 Playwright 推荐的显式等待方式，只等到元素出现就继续，不会无谓等待。`asyncio.sleep` 是固定等待，在慢速机器上可能不够，在快速机器上浪费时间。循环检查是反模式。

</details>

---

**Q3. 以下哪种断言方式在 Playwright 中最推荐？**

- A. `assert await page.locator('.result').is_visible()`
- B. `assert "成功" in await page.inner_text('.message')`
- C. `await expect(page.locator('[data-testid="success-msg"]')).to_contain_text("保存成功")`
- D. `result = await page.locator('.result').count(); assert result > 0`

<details markdown="1"><summary>查看答案</summary>

**答案：C**

解析：`expect()` API 是 Playwright 内置的断言库，它会自动等待条件满足（内置重试机制），失败时给出清晰的错误信息。其他方式缺少自动重试，在页面异步更新时容易出现误报。

</details>

---

**Q4. AI 生成的 Playwright 脚本中最常见的问题是什么？**

- A. 导入语句不完整
- B. 使用动态 CSS 类名作为选择器，缺少显式等待
- C. async/await 关键字遗漏
- D. 文件命名不规范

<details markdown="1"><summary>查看答案</summary>

**答案：B**

解析：根据 M7 课件的总结，AI 生成脚本时最频繁出现的两类问题是：① 使用动态 CSS 类（如 `.sc-abc123`）作为定位器，会在 UI 重构后失效；② 在点击/交互后没有显式等待下一步的条件满足，导致竞态条件。

</details>

---

## 判断题（T/F，每题 1 分）

**Q5. 在 AI 生成 Playwright 脚本的 Prompt 中，提供页面元素的 `aria-label` 和 `data-testid` 信息，能显著提升生成代码的质量。**

<details markdown="1"><summary>查看答案</summary>

**答案：T（正确）**

解析：提供具体的元素信息（aria-label、data-testid、role）让 AI 能直接生成稳健的语义化定位器，而不是猜测 CSS 类名或使用 XPath。这是提升 AI 脚本质量最有效的方式之一。

</details>

---

**Q6. GitHub Copilot 在自动化测试中的最佳使用方式是"把整个测试文件粘贴到对话框，让 Copilot 完成整个文件"。**

<details markdown="1"><summary>查看答案</summary>

**答案：F（错误）**

解析：Copilot 在 IDE 中的最佳使用方式是"注释驱动补全"——在代码注释中描述意图，Copilot 实时补全下一行或几行代码。这种方式让人保持控制权，每步都能审查，而不是一次性接受大量未经审查的代码。

</details>

---

## 简答题（1 题，4 分）

**Q7. 以下 AI 生成的代码片段存在至少 3 处问题，请逐一指出并给出修复建议：**

```python
async def test_submit_form(page):
    await page.goto("https://app.example.com")
    await page.locator('.form-input.first-name').fill("张三")
    await page.locator('button.submit-btn.active').click()
    assert await page.locator('.success-msg').is_visible()
```

<details markdown="1"><summary>参考答案</summary>

（每处 1 分，指出 3 处 = 3 分，修复建议补全 = 1 分）

**问题 1**：`.form-input.first-name` 使用了 CSS 类名定位器，可能是动态/不稳定的。
修复：改用 `page.get_by_role("textbox", name="名字")` 或 `page.locator('[aria-label="First Name"]')`

**问题 2**：`button.submit-btn.active` 使用了 CSS 类名，`active` 状态类在不同状态下可能消失。
修复：改用 `page.get_by_role("button", name="提交")` 或 `page.locator('[data-testid="submit-btn"]')`

**问题 3**：点击提交按钮后没有等待，直接检查成功消息，存在竞态条件。
修复：在 `click()` 后加 `await page.locator('[data-testid="success-msg"]').wait_for(state="visible")`

**问题 4**：`assert is_visible()` 断言太弱，只检查元素存在，不验证内容。
修复：改用 `await expect(page.locator('[data-testid="success-msg"]')).to_contain_text("提交成功")`

</details>

---

[← 返回课件](lecture.md) | [← Lab](lab-generic.md) | [→ 进入 M8](../08-api-testing/lecture.md)
