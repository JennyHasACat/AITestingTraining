# M10 实战 Lab — OmniPeople 定制版：闭环演练 + ROI 汇报

> **预计时长**：50 分钟

---

## Capstone：OmniPeople New Hire 完整 AI 辅助闭环

使用 OmniPeople New Hire Part-Time BU NonPromoter 场景，
走完完整的 AI 辅助测试闭环，**同时记录时间**。

---

### Phase 1 — 需求分析

使用 M5-OmniPeople Lab 中的需求描述，
运行需求歧义分析 Prompt，记录：
- 发现问题数：___
- 其中你之前未注意到的新问题：___

---

### Phase 2 — 用例生成

基于 M3-OmniPeople Lab 的维度，生成 Part-Time NonPromoter 的完整用例集，
然后与 `fixtures/omniPeople/managerService/newHire/` 中的现有 YAML 对比：
- AI 生成总数：___
- 与现有 YAML 重叠：___
- AI 新增（现有未覆盖）：___

---

### Phase 3 — 脚本评估

打开 `tests/omniPeople/managerService/newHire/` 中的测试文件，
选择 1 个测试函数，用以下 Prompt 让 AI 进行代码评审：

```
你是一名 Playwright Python 代码审查专家。
以下是我们项目中的一个测试函数：
[粘贴测试函数]

请从以下角度进行代码评审：
1. 定位器稳健性（是否有动态 class/id？）
2. 等待策略（是否有竞态条件风险？）
3. 断言完整性（是否只验证了表面，而非核心业务逻辑？）
4. 代码可维护性（是否符合 POM 规范？是否有重复代码？）
5. 给出 1–2 个具体的改进建议（带代码示例）
```

---

### Phase 4 — ROI 数据收集

填写以下表格（基于你今天的实际操作时间）：

| 任务 | AI 辅助用时 | 估算传统用时 | 节省比例 |
|------|-----------|------------|---------|
| 需求分析（~15个功能点） | | 45 min | |
| 用例生成（Part-time NP 场景）| | 90 min | |
| 代码评审（1个测试函数） | | 20 min | |
| **合计** | | **155 min** | |

---

### Manager 专项：ROI 汇报草稿

使用 **模板 ROI-01**，将上面的数据填入，生成管理层汇报摘要草稿。

生成后检查：
- [ ] 结论先行（第一句就说明了"节省了多少时间"）
- [ ] 数字是真实测量数据，不是夸大的估算
- [ ] 下一步建议具体可执行（不是"继续推进 AI 落地"这类空话）
- [ ] 包含了工具成本（即使目前是免费的，也要说明）

---

[← 返回课件](lecture.md) | [← 通用版 Lab](lab-generic.md) | [→ 做测验](quiz.md)
