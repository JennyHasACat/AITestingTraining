# M7 实战 Lab — OmniPeople 定制版：New Hire 脚本生成

> **预计时长**：45 分钟 | **工具**：DeepSeek + GitHub Copilot

---

## 背景

本 Lab 直接使用 OmniPeople 项目中真实的 Page Object 和 YAML 结构，
让你体验 AI 如何辅助扩展现有自动化脚本。

---

## Lab 7-A：读懂现有 POM 结构（5 min）

打开项目中的：
```
page_objects/omniPeople/managerService/newHire/
```

找到 Full-time 或 Part-time 相关的 Page Object 文件，
快速阅读并理解：
- 类的结构（`__init__` 中有哪些定位器？）
- 方法的命名规范（操作动词 + 对象名）
- 定位器风格（是否使用 `get_by_role` / `data-testid`？）

---

## Lab 7-B：用 AI 仿造一个新的 Page Object 方法（20 min）

### 场景

当前 Part-time 的 Page Object 已有 `select_employee_type()` 方法。
你需要新增一个方法：`fill_weekly_hours(hours: str)`。

发送以下 Prompt：

```
你是一名 Playwright Python 自动化测试专家。
以下是我们项目中现有的 OmniPeople New Hire Page Object 片段（已有方法示例）：

[从文件中复制 2-3 个现有方法到这里]

我需要在这个类中新增一个方法：fill_weekly_hours(hours: str)，
用于填写兼职员工的"预计每周工时"字段。

已知信息：
- 该字段在选择 Part-time 后才显示
- 字段类型：数字输入框
- 需要等待字段可见后再填写

请：
1. 生成符合现有代码风格的 fill_weekly_hours 方法
2. 解释选择该定位器策略的理由
3. 指出这个方法在使用前需要满足什么前置条件
```

---

## Lab 7-C：用 AI 分析现有用例覆盖缺口（20 min）

打开 `fixtures/omniPeople/managerService/newHire/` 中的 Part-time YAML 文件。

发送以下 Prompt（提供 YAML 中的 case 列表）：

```
你是一名测试架构师。
以下是我们当前 OmniPeople New Hire Part-time 模块的自动化用例列表：
[粘贴 YAML 中所有 case 的 scenario 名称或简要描述]

这些用例覆盖了以下业务维度：
- 全职/兼职创建
- 部分合同类型
- 部分字段验证

请分析：
1. 基于常见 HR 系统测试经验，上面哪些重要场景可能还没有覆盖？
2. 优先推荐 3 个应该添加的用例（按风险由高到低），并说明理由
3. 对于每个推荐用例，给出 YAML 格式的 case 骨架
```

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
