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

## Lab 4-B：生成可创建 Jira 的 Bug 报告（10 min）

基于上面的测试失败，使用 **模板 B-06** 生成可映射到 Jira 的规范 Bug 报告。先填写以下练习配置；不要使用真实生产项目，也不要在没有明确授权时创建 Issue：

```
Jira 配置：
- Project Key：TRAINING
- Issue Type：Bug
- Parent / Epic：留空
- Sprint：留空
- Estimate / Story Points：Story Points，3
- Priority：Medium
- Labels：functional-defect
- Assignee：不指定
- Summary 格式：[Environment] - <Module> - <Page/Feature> - <Issue>

原始 Bug 描述：
[粘贴 Lab 4-A 中的失败信息]

补充上下文：
- AI 分析认为最可能的根因：[填写你的判断]
- 测试环境：Chrome / Staging / Playwright Python 3.11
- 需求依据：[填写条件显示字段的预期规则；未知时标记待补充]
```

检查输出是否满足：
- [ ] Project Key、Issue Type、Priority、Labels 等值来自配置，而不是 Prompt 的固定项目值
- [ ] Summary 使用指定格式，环境或页面未知时为 `NA`
- [ ] Description 包含 Test url、Test environment、Steps、Expect Result、Actual Result
- [ ] 不确定的业务规则被标记为 `NA` 或“待补充”，没有被 AI 编造
- [ ] 默认只输出字段；若没有已授权 Jira Sandbox 工具，则保留人工创建所需的完整内容

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
