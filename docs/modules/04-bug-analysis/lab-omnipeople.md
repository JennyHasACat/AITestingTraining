# M4 实战 Lab — OmniPeople 定制版：Playwright 测试失败分析

> **预计时长**：35 分钟 | **工具**：DeepSeek（推荐，代码分析更准确）

---

## 背景

本 Lab 使用来自 OmniPeople 项目真实失败截图目录中的典型错误场景（已在 `Screenshot/` 目录中存有 FAIL 截图）。

---

## Lab 4-A：OmniPeople Playwright 报错分析（15 min）

以下是一个典型的 OmniPeople 自动化测试失败场景（基于真实模式）：

```
FAILED tests/omniPeople/managerService/newHire/test_newhire_fulltime.py
::test_create_fulltime_fulltime_china_01_bu_redNonPromoter_mcn_efo

playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
waiting for locator('select[name="contractType"]') to be visible

  at page_objects/omniPeople/managerService/newHire/newhire_fulltime_page.py:142

Error during test: element handle is gone
```

### 步骤

发送以下 Prompt 给 DeepSeek：

```
你是一名 Playwright Python 自动化测试专家，熟悉 Salesforce 类企业应用的测试。
以下是一个测试失败的详细信息：

测试名称：test_create_fulltime_fulltime_china_01_bu_redNonPromoter_mcn_efo
框架：Playwright (Python)，pytest
失败位置：newhire_fulltime_page.py:142，操作 select[name="contractType"] 时超时
报错：TimeoutError: Timeout 30000ms exceeded. Element "select[name='contractType']" not visible

业务背景：这是一个 HR 入职系统（基于 Salesforce），
"contractType" 是一个条件显示的下拉字段，
只有在前一个字段"employeeType"选择特定值后才会出现。

请分析：
1. 最可能的 3 个根因（按可能性排序）
2. 每个假设的快速验证方法
3. 对于"条件显示字段"的定位，推荐什么更稳健的 Playwright 策略？
4. 建议的修复代码方向（伪代码即可）
```

**记录 AI 分析结果，重点关注**：
- AI 是否识别出"条件显示字段"这个关键背景？
- AI 推荐的等待策略是什么？

---

## Lab 4-B：生成 OmniPeople 风格的 Bug 报告（10 min）

基于上面的测试失败，使用以下 Prompt 生成规范 Bug 报告：

```
你是一名测试工程师，以下是一个自动化测试失败的场景：
[粘贴 Lab 4-A 中的失败信息]

AI 分析认为根因是：[填写你认为最可能的根因]

环境：Chrome / Staging / Playwright Python 3.11
严重程度：P1

请生成一份规范 Bug 报告，包含：
- 标题（格式：[模块] [操作] [现象]）
- 严重程度 / 复现率 / 环境
- 前置条件
- 复现步骤（以手动测试步骤为主，因为自动化脚本可能有问题）
- 预期结果 / 实际结果
- 可能根因（来自 AI 分析）
```

---

## Lab 4-C：FAIL 截图辅助分析（10 min）

打开 `Screenshot/` 目录，找到任意一个 `FAIL_*.html` 文件，在浏览器中打开。

观察截图中的页面状态，然后向 AI 描述你看到的情况：

```
你是一名 OmniPeople 系统测试专家。
我打开了一个测试失败时自动保存的页面截图，
页面当前状态描述：[描述你看到的页面内容，如：
  - 表单部分填写
  - 某个字段显示为空/禁用
  - 出现了错误提示 xxx
  - 某个按钮不可点击]

测试的预期是完成 New Hire 入职流程提交。
请推测：这个页面状态可能说明在哪个步骤发生了问题？最可能的原因是什么？
```

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
