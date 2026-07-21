# M4 实战 Lab — 通用版：AI 辅助 Bug 分析与报告

> **预计时长**：35–40 分钟 | **工具**：Kimi / DeepSeek

---

## Lab 4-A：日志分析实战（15 min）

以下是一段 Playwright 测试的报错日志，请用 AI 进行分析：

```
FAILED tests/test_checkout.py::test_complete_order_flow
playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
=========================== logs ===========================
waiting for locator('button[data-testid="submit-order"]') to be visible
  locator resolved to <button data-testid="submit-order" class="btn btn-primary disabled">Submit Order</button>
  element is not visible
============================================================
    at tests/test_checkout.py:87 in test_complete_order_flow

  85 |     await page.fill('#total-amount', '150.00')
  86 |     await page.check('#terms-checkbox')
> 87 |     await page.locator('button[data-testid="submit-order"]').click()
  88 |
```

### 步骤

使用 M4 课件中的 **模板 B-02（UI 失败分析）** 分析上面的日志，发给 AI。

**你的分析 Prompt**：
```
[在此填写你的 Prompt]
```

**AI 的分析结果**：
```
[粘贴 AI 输出]
```

**你的判断**：
- AI 提出的哪个根因假设最可能是正确的？为什么？
- 如果你来修复这个测试，第一步会做什么？

<details>
<summary>参考分析方向</summary>

这个日志的关键线索：
- 错误类型：TimeoutError，元素存在但 `not visible`
- 元素有 `disabled` class：`class="btn btn-primary disabled"`
- 操作顺序：fill total-amount → check terms → click submit

**最可能根因**：按钮处于 disabled 状态，可能是因为：
1. `total-amount` 填写值不符合某个验证规则（如金额需要 > 0 且 <= 某个限额）
2. `terms-checkbox` 勾选动作未被系统检测到（异步状态更新未完成）
3. 按钮启用条件还依赖其他字段（如收货地址、支付方式）未填写

**建议验证方向**：检查按钮的 disabled 状态由什么条件控制（查前端代码或需求），确认所有触发条件都满足后再点击。

</details>

---

## Lab 4-B：从口头描述生成规范 Bug 报告（15 min）

以下是一个测试工程师的口头 Bug 描述（不规范）：

```
在测试新用户注册的时候发现，如果用户名里面有中文，注册是成功的，
但是后来登录的时候系统找不到这个账号，报错说用户不存在。
感觉是后端存数据的时候中文编码处理有问题。在 Chrome 上试的，
我们的 staging 环境。P1 吧感觉。
```

### 步骤

使用 **模板 B-04（Bug 报告生成）** 将上面的描述转化为规范报告。

**你的 Prompt**：
```
[在此填写你的 Prompt]
```

**AI 的 Bug 报告**：
```
[粘贴 AI 输出]
```

**你的 Review**：
- AI 生成的报告是否完整（包含所有必需字段）？
- 复现步骤是否足够具体？开发人员能独立复现吗？
- 有什么需要你补充的信息（如具体的用户名示例）？

---

## Lab 4-C：Bug 严重程度判断练习（10 min）

以下 4 个 Bug，请先自己判断严重程度，再用 AI 验证并对比：

| Bug 描述 | 我的判断 | AI 的建议 | 是否一致？ |
|---------|---------|---------|---------|
| 用户结账时选择信用卡支付后，页面白屏无法继续 | | | |
| 商品列表页的价格显示为 ¥100.0 而不是 ¥100.00（少一位小数） | | | |
| "忘记密码"功能在 Safari 浏览器上无法发送重置邮件 | | | |
| 管理后台的导出 Excel 功能，中文字段显示乱码 | | | |

---

[← 返回课件](lecture.md) | [→ OmniPeople 定制版](lab-omnipeople.md) | [→ 做测验](quiz.md)
