# TOOL-emmx2md — 思维导图 TXT 转 MD（XMind 导入）

## 解决什么问题

亿图思维导图（mm.edrawsoft.cn）导出的 TXT 用 Tab 缩进表示层级，XMind 只认 Markdown 大纲，两者格式不互通。手动转换 100+ 节点的导图既慢又容易丢内容。本脚本自动完成转换，并做**字符级保真比对**，确保零丢字。

## 用法

```bash
python emmx_to_md.py "xxx.txt"            # 单文件
python emmx_to_md.py ./txts -o ./md_out   # 批量目录
python emmx_to_md.py ./txts --dry-run     # 只解析校验、出报告，不写盘
```

更多参数：

| 参数 | 作用 |
|------|------|
| `--force` | 输出 md 已存在时强制覆盖（默认不覆盖，防冲掉手改产物） |
| `--strict` | 遇到顶格孤立行（可疑续行）直接报错停机 |
| `--encoding` | 强制指定编码（默认自动嗅探 utf-8-sig → utf-8 → gbk → gb18030 → latin-1） |
| `--report` | 指定转换报告路径（默认 `convert_report.md`） |
| `--space-width` | 空格折算层级宽度（默认 4，仅当文件用空格而非 Tab 缩进时生效） |

## 边界 / 注意

- **保真比对是核心护栏**：报告保真率必须 100%；出现 ⚠️（顶格孤立行 / 编码替换字符 U+FFFD）需人工核对；
- 编码混乱的 TXT（GBK/UTF-8 混存）建议先 `--dry-run` 探一遍再正式转；
- 零第三方依赖，仅 Python 标准库即可运行。

## 溯源

- 生成本脚本的原始 Prompt：同目录 `prompt.md`
- 课件小节：`docs/modules/03-testcase-generation/lecture.md` 第九节
- 站点索引：`docs/toolbox.md`
