# TOOL-postman-param — Postman Collection 参数化生成

> 形态 B（纯提示词型）：无脚本，核心资产是 `prompt.md` 的原始 Prompt。
> 所属模块：M8 第六节「AI 提效小工具 —— Postman Collection 参数化生成」。

## 它解决什么问题

Postman 导出的 Collection 参数全部硬编码：姓名、手机号、时间段、`request_id` 都是定值。想用 Collection Runner 批量迭代造测试数据，产出的却是一堆重复数据；接口之间的 ID 传递（创建 → 更新 → 预约）还得手动复制。手动改造几十上百个请求不现实 —— 让 AI 直接在原 JSON 内"反写"完成改造，产出导入即用的新 Collection。

## 用法

1. 从 Postman 导出 Collection（v2.1 JSON）；
2. **先发前脱敏**：把真实密钥 / 内部域名替换为 `{{app_secret}}` 这类占位符；
3. 把 JSON 源码 + `prompt.md` 的 Prompt（填好 `[占位符]`）一起发给 AI；
4. AI 返回改造后的 JSON（已注入 Pre-request / Tests 脚本、Body 已变量化）；
5. 用 JSON lint 校验返回值合法（符合 Collection v2.1 schema），导入 Postman；
6. 按 AI 输出的【环境变量初始化清单】配好 Environment 初始变量；
7. Collection Runner 设置迭代次数，开跑。

## sample/ 样例

| 文件 | 说明 |
|------|------|
| `collection-before.json` | 改造前：3 请求链路（创建 Lead → 更新 Lead → 预约），参数硬编码、test 为占位脚本或无 |
| `collection-after.json` | 改造后：自增手机号/姓名、Tests 提取 `leadId` 传下游、时间滑动、`{{$guid}}` 动态 UUID、每请求有正式断言 |

样例已脱敏（虚构域名 / 会员 ID / 密钥占位符），可导入 Postman 对比结构，但网关地址是虚构的，不能真实调通 —— 用于对照学习"AI 到底改了什么"。

## 环境变量初始化清单（after 样例）

| 变量名 | 初始值 | 用途说明 |
|--------|--------|----------|
| `apigateway_url` | `https://your-apigw.example.com` | 3 个请求统一的网关地址 |
| `app_secret` | （填入真实密钥） | 请求头 `x-odin-appsecret` |
| `base_mobile` | `13800000000` | Add Lead 手机号自增起始值 |
| `base_name` | `AutoTest-00000` | Add Lead 姓名自增起始值（前缀 + 5 位序号） |
| `base_start_time` | `2026-09-01T09:00:00.000Z` | Book Appointment 时间滑动基准 |
| `slot_step_minutes` | `15` | 每次迭代时间后推步长（分钟） |
| `seq` | `0` | 迭代计数器，脚本自动 +1，配好后不用手改 |

## 边界与注意事项

- **防 JSON 结构破坏**：要求 AI 输出合法 Collection v2.1 schema，导入前必过 JSON lint（AI 偶尔会截断或产出非法 JSON）；
- **认清网关包装结构**：样例 Collection 所有请求的 URL 都是同一个网关，真实 endpoint 藏在 body 的 `url` / `http_method` 字段里 —— Prompt 里最好点明这层结构，否则 AI 可能改错地方；
- **敏感信息先占位**：真实 Collection 含密钥与内部域名，发给 AI 前必须替换为占位符，导入后通过环境变量配回；
- **断言深度**：AI 生成的 Tests 偏浅（状态码 + 个别字段），关键业务断言人工补强；
- **路线分工**：本工具留在 Postman 生态（Runner 批量造数 / 轻量验证）；要纳入 CI 回归，走 M8 第五节「Collection → pytest」路线，两者互补。
