# Prompt 模板资产包 — 自动化脚本生成类

> **分类**：Playwright / pytest 脚本生成 | **适用模块**：M7–M8

---

## AUTO-01 手动步骤转 Playwright POM 脚本

**场景**：将手动测试步骤转化为 Playwright Python 自动化脚本  
**推荐工具**：DeepSeek + GitHub Copilot  
**效果评级**：⭐⭐⭐⭐⭐  
**最后验证日期**：2026-07-20  
**已知局限**：定位器可能使用动态 class，需要人工替换为语义化定位器

```
你是一名 Playwright Python 自动化测试专家，使用 pytest 框架。
项目约定：
- Page Object Model（POM）
- 定位器优先：data-testid > role+name > aria-label > 稳定 id > CSS 类（最后选）
- 所有交互前必须加显式等待，禁止使用 asyncio.sleep()
- 使用 page.locator() / get_by_role() / get_by_label() API
- 断言使用 expect() API，不使用 assert is_visible()

手动测试步骤：
[粘贴有序的手动步骤，每步一行]

已知页面元素（提供你知道的）：
[aria-label="xxx" / data-testid="xxx" / role="button" name="xxx"]

请生成：
1. Page Object 类（包含定位器属性和操作方法）
2. pytest 异步测试函数（使用 async/await）
3. 每个定位器旁边加注释说明选择理由
```

---

## AUTO-02 定位器修复（动态 class 替换）

**场景**：修复 AI 生成或录制的脚本中的不稳定定位器  
**推荐工具**：DeepSeek  
**效果评级**：⭐⭐⭐⭐⭐  
**最后验证日期**：2026-07-20

```
以下 Playwright 代码使用了不稳定的定位器（动态 CSS 类/XPath），请修复。
[粘贴有问题的代码]
已知元素信息：
- [元素名称]：[aria-label/data-testid/role+name 等信息]
请：
1. 将所有不稳定定位器替换为语义化定位器
2. 解释每处修改的理由
3. 同时检查是否缺少显式等待，如有添加适当的 wait_for()
```

---

## AUTO-03 等待策略修复

**场景**：为缺少等待的脚本添加显式等待  
**推荐工具**：DeepSeek  
**效果评级**：⭐⭐⭐⭐  
**最后验证日期**：2026-07-20

```
请检查以下 Playwright 脚本，找出所有可能存在竞态条件的地方。
[粘贴脚本]
对每处缺少等待的位置，添加合适的等待策略：
- 等待元素可见：.wait_for(state="visible")
- 等待导航完成：wait_for_url() 或 wait_for_load_state()
- 等待网络请求：wait_for_response()
禁止使用 asyncio.sleep()，解释每处修改的理由。
```

---

## AUTO-04 pytest fixture 生成（API Setup/Teardown）

**场景**：生成通过 API 准备测试数据的 pytest fixture  
**推荐工具**：DeepSeek  
**效果评级**：⭐⭐⭐⭐⭐  
**最后验证日期**：2026-07-20

```
我需要一个 pytest async fixture（带 yield teardown），
通过 API 创建测试数据，测试结束后自动清理。
创建接口：[METHOD] [URL]，响应包含 {"id": "xxx"}
删除接口：[METHOD] [URL/{id}]
认证：[Bearer token from os.environ["API_TOKEN"]]
要求：
- 使用 httpx.AsyncClient（或 requests，按项目已有依赖）
- fixture scope = "function"（每用例独立数据）
- 创建数据使用 TEST_ 前缀标识
- Teardown 发生在 yield 之后
请生成 conftest.py 中的 fixture 代码。
```

---

## AUTO-05 conftest.py 浏览器 Fixture

**场景**：生成标准化的 Playwright pytest conftest 配置  
**推荐工具**：DeepSeek  
**效果评级**：⭐⭐⭐⭐  
**最后验证日期**：2026-07-20

```
你是一名 Playwright pytest 配置专家。
请生成一个 conftest.py，包含：
1. browser_context fixture（Chromium，视窗 1280×720）
2. --headed 命令行参数支持（默认 headless）
3. 每个 test 使用独立 context（不共享登录状态）
4. 测试失败时自动截图（保存路径：Screenshot/ 目录，文件名含测试名称和时间戳）
5. 基础 URL 从环境变量 BASE_URL 读取
```

---

## OP-AUTO01 OmniPeople POM 方法生成

**场景**：为 OmniPeople 系统生成符合现有代码风格的 POM 方法  
**推荐工具**：GitHub Copilot + DeepSeek  
**效果评级**：⭐⭐⭐⭐  
**最后验证日期**：2026-07-20

```
你是一名 Playwright Python 自动化测试专家。
以下是 OmniPeople 项目中现有的 Page Object 代码片段（用于理解风格）：
[粘贴 2-3 个现有方法]
我需要新增一个方法：[方法名]([参数])
业务说明：[描述这个方法需要操作什么 UI 元素，完成什么动作]
已知元素信息：[aria-label/data-testid/role+name]
请生成符合现有代码风格的方法，注释说明定位器选择理由。
```

---

*最后更新：2026-07-20*
