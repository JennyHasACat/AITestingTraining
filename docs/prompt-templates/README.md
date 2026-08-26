# Prompt 模板资产包 — 目录

> 共 **7 个场景分类**，30+ 条经验证的可复用 Prompt 模板  
> 维护方式：GitHub Issues + PR 流程  
> 贡献标准：2 人以上验证通过，效果评级 ≥ 4 星方可入库

---

## 分类导航

| 文件 | 场景 | 模板数 | 对应模块 |
|------|------|--------|---------|
| [testcase-design.md](testcase-design.md) | 测试用例设计 | T-01 ~ T-06 + OP-T01 | M3 |
| [bug-report.md](bug-report.md) | Bug 分析与报告 | B-01 ~ B-06 + OP-B01 | M4 |
| [script-generation.md](script-generation.md) | 自动化脚本生成 | AUTO-01 ~ AUTO-05 + OP-AUTO01 | M7–M8 |
| [sql-query.md](sql-query.md) | 数据库 SQL / SOQL | DB-01 ~ DB-05 | M6 |
| [requirements-analysis.md](requirements-analysis.md) | 需求分析与测试计划 | R-01 ~ R-07 | M5 |
| [report-writing.md](report-writing.md) | 测试报告与文档 | D-05, D-01 ~ D-04 | M5 + M10 |
| [rovo-test-case-generator-agent.md](rovo-test-case-generator-agent.md) | Rovo Agent（测试用例生成） | Agent 级 | 可独立使用 |

---

## 命名规范

| 前缀 | 含义 |
|------|------|
| `T-` | 通用测试类 |
| `B-` | Bug 分析报告类 |
| `R-` | 需求分析类 |
| `DB-` | 数据库 SQL 类 |
| `AUTO-` | 自动化脚本类 |
| `D-` | 文档报告类 |
| `OP-` | OmniPeople 项目专属 |

---

## 贡献流程

1. 使用一个 Prompt 至少 3 次，效果稳定
2. 按标准格式整理（参考各文件中的示例）
3. 在 GitHub Issues 提交，标签：`[prompt-new]`
4. 等待 2 位以上成员确认使用有效
5. 提 PR 添加到对应分类文件

---

## 标准模板格式

```markdown
## [编号] [模板名称]

**场景**：一句话
**推荐工具**：xxx
**效果评级**：⭐⭐⭐⭐
**最后验证日期**：YYYY-MM-DD
**已知局限**：（如有）

[完整 Prompt 正文，占位符用 [大括号]]

使用说明：[如何填写占位符]
```
