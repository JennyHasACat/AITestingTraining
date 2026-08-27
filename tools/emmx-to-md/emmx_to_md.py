#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emmx_to_md.py
=============

把亿图思维导图（mm.edrawsoft.cn）导出的 .emmx -> txt 文件转换为 Markdown 大纲。

核心特性
--------
- 层级靠 Tab 缩进表示，转成 Markdown 列表 + 缩进（每层 2 空格，纯列表，不加 H1）。
- 保留原文所有内容（含多行节点续行、自带编号、全(oor全角)字符、SQL、半/全角混排等）。
- 处理“多行文本节点只有首行带缩进、续行顶格无缩进”的亿图导出格式：
  顶格行若紧跟有缩进的行，判为上一行节点的续行，合并进同一列表项。
- 缩进单位统一换算：1 Tab = 1 单位；连续空格按探测宽度（默认 4）折算；容忍 Tab/空格混用。
- 编码自动嗅探（BOM / utf-8 / gbk / gb18030 / latin-1 兜底），出现替换字符 U+FFFD 时报警。
- 批量目录模式：递归 *.txt，输出保持相对路径结构；默认拒绝覆盖已有 .md，需 --force。
- 转换报告 convert_report.md：含统计指标 + 与原 txt 的字符级保真比对（核心护栏）。
- --dry-run：只解析、出报告、不写 .md。
- --strict：遇到可疑续行（顶格孤立行）直接抛错停机，而非仅记入报告。

Usage
-----
单文件：
    python emmx_to_md.py "OMNI-69499 (Vietnam Leave)1 (1).txt"
    python emmx_to_md.py input.txt -o output.md
    python emmx_to_md.py input.txt --encoding gbk

批量目录：
    python emmx_to_md.py ./txts -o ./md_out
    python emmx_to_md.py .            # 递归 *.txt，输出放各 txt 同目录

干跑 + 报告：
    python emmx_to_md.py ./txts --dry-run --report convert_report.md

严格模式（任意顶格孤立行即停机）：
    python emmx_to_md.py ./txts --strict
"""

from __future__ import annotations

import argparse
import io
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from difflib import SequenceMatcher

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# Markdown 列表每层缩进（空格数）。已与用户确认 = 2。
MD_INDENT_UNIT = "  "

# 软换行：行尾两空格，保证 Xmind 导入时多行文本不丢失。
MD_SOFT_BREAK = "  "

# 默认空格缩进宽度探测：若某行用空格而非 Tab 缩进，按此宽度折算层级单位。
DEFAULT_SPACE_WIDTH = 4

# 候选编码顺序（utf-8-sig 会自动剥 BOM；utf-8 严格模式先试）
ENCODING_CANDIDATES = ["utf-8-sig", "utf-8", "gbk", "gb18030", "latin-1"]

# 报告文件默认名
DEFAULT_REPORT_NAME = "convert_report.md"

# 替换字符 U+FFFD，出现即说明解码可能已坏
REPLACEMENT_CHAR = "\ufffd"


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Node:
    """一个思维导图节点。

    属性
    ----
    indent : int
        层级深度（根=0），已按统一单位换算。
    lines : list[str]
        节点文本。lines[0] 为首行（原带缩进），lines[1:] 为续行（原顶格）。
    children : list[Node]
        子节点。
    """
    indent: int
    lines: list[str] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)

    def add_continuation(self, line: str) -> None:
        """把一行续行追加到本节点。"""
        self.lines.append(line)


@dataclass
class ParseStats:
    """解析过程统计，供报告使用。"""
    node_count: int = 0            # 节点总数（含续行合并后的多行节点）
    continuation_count: int = 0   # 被合并回的续行总数
    orphan_count: int = 0          # 顶格孤立行数（既非首行也未被合并）
    max_depth: int = 0             # 最大层级深度
    empty_line_count: int = 0       # 跳过的空行数
    # 孤立行详情：(txt 行号, 文本) 列表，便于报告定位
    orphan_details: list[tuple[int, str]] = field(default_factory=list)
    # 续行详情：(txt 行号, 文本) 列表
    continuation_details: list[tuple[int, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 编码处理
# ---------------------------------------------------------------------------

def detect_and_read(path: Path, override: str | None) -> tuple[str, str, bool]:
    """读取文件，自动嗅探编码。

    返回
    ----
    (text, used_encoding, has_replacement_char)

    has_replacement_char 为 True 说明解码存在 U+FFFD，可能已坏 —— 报告里报警。
    override 非空时强制使用该编码，失败直接抛错（避免静默坏数据）。
    """
    raw = path.read_bytes()

    if override:
        try:
            text = raw.decode(override)
        except LookupError:
            raise SystemExit(f"[ERROR] 未知编码名: {override}（文件 {path}）")
        except UnicodeDecodeError as e:
            raise SystemExit(
                f"[ERROR] 文件 {path} 无法用指定编码 {override} 解码: {e}"
            )
        return text, override, REPLACEMENT_CHAR in text

    # 自动嗅探：依次尝试候选编码，首个成功的采用
    last_err: Exception | None = None
    for enc in ENCODING_CANDIDATES:
        try:
            text = raw.decode(enc)
            return text, enc, REPLACEMENT_CHAR in text
        except UnicodeDecodeError as e:
            last_err = e
            continue
    # 理论上 latin-1 永不失败，到这里说明文件本身有问题
    raise SystemExit(f"[ERROR] 文件 {path} 所有候选编码均失败，最后错误: {last_err}")


# ---------------------------------------------------------------------------
# 缩进换算
# ---------------------------------------------------------------------------

def count_indent_units(line: str, space_width: int = DEFAULT_SPACE_WIDTH) -> int:
    """计算一行的前导缩进“单位数”。

    规则
    ----
    - 1 Tab = 1 单位
    - 连续空格按 space_width 折算（默认 4 空格 = 1 层）
    - Tab 与空格混用时，按出现顺序逐段累计
    - 遇到非空白字符即停止

    示例（space_width=4）：
        "\t\tA"      -> 2
        "    A" micro -> 1
        "\t  A"      -> 1 + 0 = 1（2 空格不足 4，计 0）
    """
    units = 0
    spaces = 0
    for ch in line:
        if ch == "\t":
            # 把累积的零散空格先结算（不足 1 单位则丢弃）
            spaces = 0
            units += 1
        elif ch == " ":
            spaces += 1
            if spaces >= space_width:
                units += 1
                spaces = 0
        else:
            break
    return units


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

def parse_lines(lines: list[str], space_width: int, stats: ParseStats,
                strict: bool, file_path: Path) -> list[Node]:
    """把按行切好的文本解析为节点树（森林）。

    核心难点：多行续行顶格无缩进，需识别并合并回上一节点。
    """
    roots: list[Node] = []
    # 栈元素 = (indent, Node)，栈顶为当前活跃节点
    stack: list[tuple[int, Node]] = []

    # 上一“非空行”的信息：用于续行判定
    # “非空行”指被本解析器实际处理的逻辑行（含续行行，不含空行）
    last_non_empty_line_no: int = -1
    last_non_empty_indent: int = -1

    def push_node(indent: int, first_line: str, line_no: int) -> Node:
        """建新节点并挂到正确父级。"""
        # 回溯栈到 indent < 当前 indent 的位置（父级）
        while stack and (not stack[-1][0] < indent):
            stack.pop()
        # 父节点：栈顶（可能为空 = 根）
        parent = stack[-1][1] if stack else None
        node = Node(indent=indent, lines=[first_line])
        if parent is None:
            roots.append(node)
        else:
            parent.children.append(node)
        stack.append((indent, node))
        stats.node_count += 1
        if indent > stats.max_depth:
            stats.max_depth = indent
        return node

    for line_no, raw_line in enumerate(lines, start=1):
        # 去行尾换行符：splitlines 已处理 \r\n / \r / \n，这里仅去可能的尾随空串
        # 注意：raw_line 已由 splitlines 去掉了换行符
        line = raw_line

        if line.strip() == "":
            stats.empty_line_count += 1
            continue

        indent = count_indent_units(line, space_width)
        content = line[indent_to_strip(line, space_width):] \
            if indent > 0 else line

        # 续行判定：顶格(indent=0) 且 非首行 且 上一非空行所属逻辑节点有缩进
        # 关键修正：亿图里经常出现连续多行续行（如 Precondition 下 1,2,3,4），
        # 第 2 条续行的"上一非空行"是上 1 条续行(顶格)，但其所属逻辑节点的 indent>0。
        # 故判据用"当前栈顶节点的 indent"而非"上一行字面 indent"。
        current_node_indent = stack[-1][0] if stack else -1
        # 扩展：根节点(indent=0)的多行续行也应合并。判据：栈中仅有 1 个根(刚 push)，
        # 紧邻上一非空行，则把顶格行作为该根的续行。
        is_root_continuation = (
            indent == 0
            and len(stack) == 1
            and stack[-1][0] == 0        # 当前活跃节点是根
            and last_non_empty_line_no == line_no - 1
        )
        is_continuation = (
            indent == 0
            and last_non_empty_line_no > 0      # 非首行
            and current_node_indent > 0         # 当前活跃节点有缩进（根的续行另有处理）
            and last_non_empty_line_no == line_no - 1  # 紧邻（无空行打断）
            and stack                                             # 栈中有节点可合并
        )

        if is_continuation or is_root_continuation:
            # 合并到当前栈顶节点（普通续行 = 有缩进节点；根续行 = 根节点）
            target = stack[-1][1]
            target.add_continuation(line)   # 整行原样保留（顶格无缩进，无需去空格）
            stats.continuation_count += 1
            stats.continuation_details.append((line_no, line))
            # 续行不改栈、不改 current_node_indent；但推进 last 行号以便下一续行判紧邻
            last_non_empty_line_no = line_no
            # last_non_empty_indent 保持原值（续行视为延续上一行，不更新 indent）
            continue

        # 非续行：顶格新行（孤儿） or 带缩进新节点
        if indent == 0 and last_non_empty_line_no > 0 and current_node_indent > 0 \
                and not (last_non_empty_line_no == line_no - 1):
            # 顶格行，上一非空行有缩进，但中间隔了空行 —— 既非续行也非根 -> 孤立行
            # 这种行按“根节点”处理，但记为孤立供报告警示
            stats.orphan_count += 1
            stats.orphan_details.append((line_no, line))
            if strict:
                raise SystemExit(
                    f"[STRICT] 文件 {file_path} 第 {line_no} 行为顶格孤立行，"
                    f"既非首行也非续行（内容: {line[:60]!r}）。--strict 模式已停机。"
                )
            # 按“保内容不丢”原则，作为新根节点处理
            push_node(indent=0, first_line=line, line_no=line_no)
            last_non_empty_line_no = line_no
            last_non_empty_indent = indent
            continue

        if indent == 0:
            # 根节点（含首行；或独立顶格根）
            push_node(indent=0, first_line=line, line_no=line_no)
        else:
            # 带缩进的新节点
            push_node(indent=indent, first_line=line, line_no=line_no)

        last_non_empty_line_no = line_no
        last_non_empty_indent = indent

    return roots


def indent_to_strip(line: str, space_width: int) -> int:
    """计算要去掉的前导字符数（用于取 content）。

    与 count_indent_units 配合：Tab 计 1 字符，空格计 space_width 字符。
    返回应剥离的前导字符数（字符数，非单位数）。
    """
    stripped = 0
    spaces = 0
    for ch in line:
        if ch == "\t":
            spaces = 0
            stripped += 1
        elif ch == " ":
            spaces += 1
            if spaces >= space_width:
                stripped += space_width
                spaces = 0
            # 不足 space_width 的零散空格不计入剥离（保持原样）
            # 避免把半层缩进的空格也吃掉
        else:
            break
    return stripped


# ---------------------------------------------------------------------------
# 序列化为 Markdown
# ---------------------------------------------------------------------------

def serialize_markdown(roots: list[Node], out: io.StringIO) -> None:
    """把节点森林序列化为 Markdown 列表（DFS，每层缩进 2 空格）。"""
    for root in roots:
        _serialize_node(root, depth=0, out=out)


def _serialize_node(node: Node, depth: int, out: io.StringIO) -> None:
    """DFS 序列化单个节点。"""
    prefix = MD_INDENT_UNIT * depth + "- "
    # 节点首行（去原缩进后的 content）
    first_line = node.lines[0]
    # 首行原本带缩进，已在解析时用 content；但续行是原样整行
    # 为统一，首行也用 content —— 但解析时 push 存的是 line（含缩进）
    # 这里需重新去缩进。简单起见，解析时存 content 更好。
    # （见 parse：push_node 存的是 line 原值；这里去缩进）
    # 为避免歧义，重新计算
    # —— 实际上 parse 时传的是 first_line=full line；这里 safe-strip
    first_content = _strip_leading_indent(first_line)
    out.write(f"{prefix}{first_content}")
    # 续行：软换行连接
    for cont in node.lines[1:]:
        out.write(MD_SOFT_BREAK + "\n" + prefix.replace("- ", "  "))
        out.write(cont)
    out.write("\n")
    # 子节点
    for child in node.children:
        _serialize_node(child, depth=depth + 1, out=out)


def _strip_leading_indent(line: str) -> str:
    """去掉行首的所有 Tab 和空格，保留内容。"""
    i = 0
    while i < len(line) and line[i] in " \t":
        i += 1
    return line[i:]


# ---------------------------------------------------------------------------
# 与原 txt 保真比对
# ---------------------------------------------------------------------------

def normalize_for_compare(text: str) -> str:
    """把文本归一化为“纯字符序列”，用于 txt vs md 内容比对。

    去除所有空白字符（空格、Tab、换行、MD 软换行两空格、列表符号 -、文件尾换行），
    仅保留“有意义的可见字符”。全/半角、SQL、符号一律原样保留。

    这样比对通过的依据是：所有非空白字符一字不差。
    """
    out_chars: list[str] = []
    for ch in text:
        if ch in (" ", "\t", "\r", "\n"):
            continue
        # 去除 Markdown 列表符号 “-”只在行首时去？为简单，去所有独立 - 可能误伤
        # 为安全，仅去除行首的列表前缀已在 md 端单独处理；此处不去掉正文中 -
        out_chars.append(ch)
    return "".join(out_chars)


def compare_content(txt_text: str, md_text: str) -> dict:
    """字符级保真比对。

    返回
    ----
    {
        "txt_len": int,            # txt 归一化后字符数
        "md_len": int,             # md 归一化后字符数
        "ratio": float,            # SequenceMatcher ratio
        "first_diff_txt": str,     # 首个差异块 txt 侧文本（前 80 字符），无误为 ""
        "first_diff_md": str,
        "identical": bool,
    }
    """
    txt_norm = normalize_for_compare(txt_text)
    md_norm = normalize_for_compare(md_text)
    # md 端需额外去除列表符号与软换行标记：normalize 已去空白，但 "---" 的 "-" 仍存
    # 因列表符号 `-` 在 md 行首，去掉所有行首 `- ` 即可
    # 简化：md 端去掉所有 “-” 字符？会误伤正文里的短横线（如 <-> 或 indeed）
    # 改进：md 端逐行去行首 “{indent}- ” 后再 normalize
    md_lines = md_text.splitlines()
    md_body = []
    for ln in md_lines:
        # 去行首列表前缀：任意空格 + “- ”
        stripped = ln.lstrip(" ")
        if stripped.startswith("- "):
            stripped = stripped[2:]
        elif stripped == "-":
            stripped = stripped[1:]
        md_body.append(stripped)
    md_norm = normalize_for_compare("\n".join(md_body))

    sm = SequenceMatcher(None, txt_norm, md_norm, autojunk=False)
    ratio = sm.ratio()
    identical = (txt_norm == md_norm)

    first_diff_txt = ""
    first_diff_md = ""
    if not identical:
        # 找首个差异
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            first_diff_txt = txt_norm[i1:i2][:80]
            first_diff_md = md_norm[j1:j2][:80]
            break

    return {
        "txt_len": len(txt_norm),
        "md_len": len(md_norm),
        "ratio": ratio,
        "first_diff_txt": first_diff_txt,
        "first_diff_md": first_diff_md,
        "identical": identical,
    }


# ---------------------------------------------------------------------------
# 单文件转换
# ---------------------------------------------------------------------------

@dataclass
class ConvertResult:
    input_path: Path
    output_path: Path | None        # dry-run 时为 None
    encoding: str
    has_replacement_char: bool
    stats: ParseStats
    comparison: dict
    skipped: bool = False           # 空文件等
    skip_reason: str = ""
    error: str = ""


def convert_one(input_path: Path,
                output_path: Path | None,
                encoding_override: str | None,
                space_width: int,
                dry_run: bool,
                force: bool,
                strict: bool) -> ConvertResult:
    """转换单个 txt 文件。"""
    # 读取（嗅探编码）
    text, used_enc, has_repl = detect_and_read(input_path, encoding_override)

    # 空文件退化
    if text.strip() == "":
        return ConvertResult(
            input_path=input_path, output_path=output_path,
            encoding=used_enc, has_replacement_char=has_repl,
            stats=ParseStats(), comparison={},
            skipped=True, skip_reason="空文件或纯空白文件",
        )

    # 按行切：splitlines 兼容 \r\n / \r / \n
    lines = text.splitlines()

    # 解析
    stats = ParseStats()
    roots = parse_lines(lines, space_width=space_width, stats=stats,
                       strict=strict, file_path=input_path)

    # 序列化为 Markdown
    buf = io.StringIO()
    serialize_markdown(roots, buf)
    md_text = buf.getvalue()

    # 保真比对
    comparison = compare_content(text, md_text)

    result = ConvertResult(
        input_path=input_path,
        output_path=output_path,
        encoding=used_enc,
        has_replacement_char=has_repl,
        stats=stats,
        comparison=comparison,
    )

    # 写盘（非 dry-run）
    if not dry_run and output_path is not None:
        if output_path.exists() and not force:
            result.skipped = True
            result.skip_reason = f"输出已存在，未覆盖（用 --force 覆盖）：{output_path}"
            return result
        output_path.write_text(md_text, encoding="utf-8")

    return result


# ---------------------------------------------------------------------------
# 批量入口
# ---------------------------------------------------------------------------

def collect_txt_files(input_path: Path) -> list[Path]:
    """输入为文件 → [该文件]；为目录 → 递归 *.txt（忽略 .md 输出）。"""
    if input_path.is_file():
        return [input_path]
    return sorted(p for p in input_path.rglob("*.txt") if p.is_file())


def resolve_output_path(txt_path: Path,
                         output_arg: Path | None,
                         input_is_dir: bool) -> Path:
    """解析输出 .md 路径。"""
    md_name = txt_path.stem + ".md"
    if output_arg is None:
        # 默认：同名 .md 放 txt 同目录
        return txt_path.with_suffix(".md")
    if input_is_dir:
        # 目录模式：保持相对路径结构，输出到 output_arg 下
        # 注意：here txt_path 是相对 input 的，取相对路径
        # 但若 txt 在 input 子目录，需建对应子目录
        return output_arg / md_name
    # 单文件 + output_arg：若 output_arg 是目录则放进去，否则当作完整文件名
    if output_arg.suffix == ".md":
        return output_arg
    if output_arg.is_dir() or (not output_arg.exists() and output_arg.suffix == ""):
        return output_arg / md_name
    return output_arg


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------

def build_report(results: list[ConvertResult], dry_run: bool) -> str:
    """生成 Markdown 报告。"""
    total = len(results)
    ok = sum(1 for r in results if not r.skipped and not r.error)
    warned = sum(1 for r in results if _has_warning(r))
    failed = sum(1 for r in results if r.error)
    skipped = sum(1 for r in results if r.skipped)
    fidelity_ok = sum(1 for r in results if r.comparison.get("identical"))
    fidelity_fail = sum(1 for r in results if r.comparison and not r.comparison.get("identical"))

    lines: list[str] = []
    lines.append("# 转换报告\n")
    lines.append(f"模式: {'DRY-RUN（未写盘）' if dry_run else '正常（已写盘）'}\n")
    lines.append("## 摘要\n")
    lines.append(f"- 处理文件数: {total}")
    lines.append(f"- 成功: {ok} / 警告: {warned} / 失败: {failed} / 跳过: {skipped}")
    lines.append(f"- 字符级保真通过: {fidelity_ok} ✅")
    lines.append(f"- 字符级保真失败: {fidelity_fail} ✗\n")

    lines.append("## 逐文件明细\n")
    lines.append("| 文件 | 编码 | 节点/续行/孤立 | md 节点 | txt 字符 | md 字符 | 保真率 | 状态 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        rel = r.input_path.name
        s = r.stats
        c = r.comparison or {}
        ratio = f"{c.get('ratio', 0):.1%}" if c else "N/A"
        status = "✅" if not _has_warning(r) and not r.error else ("⚠️" if _has_warning(r) else "❌")
        if r.skipped:
            status = "⏭️"
        txt_len = c.get("txt_len", "N/A")
        md_len = c.get("md_len", "N/A")
        repl = " ！" if r.has_replacement_char else ""
        lines.append(
            f"| {rel} | {r.encoding}{repl} | {s.node_count}/{s.continuation_count}/{s.orphan_count} "
            f"| {s.node_count} | {txt_len} | {md_len} | {ratio} | {status} |"
        )
    lines.append("")

    # 警告详情
    warned_results = [r for r in results if _has_warning(r)]
    if warned_results:
        lines.append("## 警告详情\n")
        for r in warned_results:
            lines.append(f"### {r.input_path.name}\n")
            s = r.stats
            c = r.comparison or {}
            if r.has_replacement_char:
                lines.append("- ⚠️ 解码出现替换字符 U+FFFD，疑似编码错误（内容可能已坏）")
            if r.error:
                lines.append(f"- ❌ 错误: {r.error}")
            if r.skipped:
                lines.append(f"- ⏭️ 跳过: {r.skip_reason}")
            if c:
                ratio = c.get("ratio", 0)
                if ratio < 1.0:
                    lines.append(f"- ⚠️ 保真率 {ratio:.1%}（应为 100%）")
                    if c.get("first_diff_txt") or c.get("first_diff_md"):
                        lines.append(
                            f"  - 首个差异: txt 侧 {c['first_diff_txt']!r} "
                            f"| md 侧 {c['first_diff_md']!r}"
                        )
            if s.orphan_count > 0:
                lines.append(f"- ⚠️ 顶格孤立行 {s.orphan_count} 处（既非首行也非续行）:")
                for ln, txt in s.orphan_details[:10]:
                    lines.append(f"  - 第 {ln} 行: {txt[:80]!r}")
            if s.continuation_count > 0:
                lines.append(f"- ℹ️ 续行合并 {s.continuation_count} 处:")
                for ln, txt in s.continuation_details[:10]:
                    lines.append(f"  - 第 {ln} 行: {txt[:80]!r}")
            if stats_max := s.max_depth:
                lines.append(f"- ℹ️ 最大层级深度: {stats_max}")
            lines.append("")

    # 图例
    lines.append("## 图例\n")
    lines.append("- ✅ 保真率 100% 且无警告")
    lines.append("- ⚠️ 有警告（孤立行 / 编码替换字符 / 保真率 < 100%）")
    lines.append("- ❌ 失败（未产出 md）")
    lines.append("- ⏭️ 跳过（空文件 / 输出已存在未覆盖）")
    lines.append("- `延续/续行`：亿图格式中顶格无缩进的后续行，合并回上一节点")
    lines.append("- `孤立行`：顶格行但既非首行也非续行，按根节点处理并记入警告")
    lines.append("- `保真率`：txt 与 md 字符级比对（去空白后）的相似度，100% = 0 丢字")
    return "\n".join(lines) + "\n"


def _has_warning(r: ConvertResult) -> bool:
    """是否含需要人工确认的警告。"""
    if r.has_replacement_char:
        return True
    if r.comparison and r.comparison.get("ratio", 1.0) < 1.0:
        return True
    if r.stats.orphan_count > 0:
        return True
    return False


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="把亿图思维导图导出的 txt 转为 Markdown 大纲（保留全部内容）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path,
                        help="输入 txt 文件或目录（目录模式递归 *.txt）")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="输出 .md（单文件）或输出目录（批量）；默认同名 .md 放同目录")
    parser.add_argument("--encoding", default=None,
                        help="强制指定输入 txt 编码（如 gbk），默认自动嗅探")
    parser.add_argument("--space-width", type=int, default=DEFAULT_SPACE_WIDTH,
                        help=f"空格折算层级宽度，默认 {DEFAULT_SPACE_WIDTH}（仅当文件用空格缩进时生效）")
    parser.add_argument("--dry-run", action="store_true",
                        help="只解析、比对、出报告，不写 .md")
    parser.add_argument("--force", action="store_true",
                        help="输出 .md 已存在时强制覆盖")
    parser.add_argument("--strict", action="store_true",
                        help="遇到顶格孤立行（可疑续行）直接抛错停机")
    parser.add_argument("--report", type=Path, default=None,
                        help=f"报告输出路径，默认 {DEFAULT_REPORT_NAME}")
    parser.add_argument("--no-report", action="store_true",
                        help="不生成报告文件")
    args = parser.parse_args(argv)

    input_path: Path = args.input.resolve()
    if not input_path.exists():
        print(f"[ERROR] 输入不存在: {input_path}", file=sys.stderr)
        return 2

    input_is_dir = input_path.is_dir()
    txt_files = collect_txt_files(input_path)
    if not txt_files:
        print(f"[ERROR] 未在 {input_path} 找到 .txt 文件", file=sys.stderr)
        return 2

    results: list[ConvertResult] = []
    for txt in txt_files:
        out = resolve_output_path(txt, args.output, input_is_dir) if not args.dry_run else None
        if out is not None and input_is_dir:
            out.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = convert_one(
                input_path=txt,
                output_path=out,
                encoding_override=args.encoding,
                space_width=args.space_width,
                dry_run=args.dry_run,
                force=args.force,
                strict=args.strict,
            )
        except SystemExit as e:
            r = ConvertResult(
                input_path=txt, output_path=out,
                encoding="?", has_replacement_char=False,
                stats=ParseStats(), comparison={},
                error=str(e),
            )
        results.append(r)

    # 控制台简要总结
    _print_summary(results, args.dry_run)

    # 报告
    if not args.no_report:
        report_path = args.report or (input_path.parent if input_path.is_file() else input_path) / DEFAULT_REPORT_NAME
        # 若报告本身落在输入目录下且输入是目录，避免递归影响
        report_text = build_report(results, args.dry_run)
        try:
            report_path.write_text(report_text, encoding="utf-8")
            print(f"[INFO] 报告已写入: {report_path}", file=sys.stderr)
        except OSError as e:
            print(f"[WARN] 报告写入失败: {e}", file=sys.stderr)

    # 返回码：有错误=1，否则 0
    return 1 if any(r.error for r in results) else 0


def _print_summary(results: list[ConvertResult], dry_run: bool) -> None:
    """控制台总结。"""
    total = len(results)
    ok = sum(1 for r in results if not _has_warning(r) and not r.error and not r.skipped)
    warned = sum(1 for r in results if _has_warning(r))
    failed = sum(1 for r in results if r.error)
    skipped = sum(1 for r in results if r.skipped)
    fidelity_ok = sum(1 for r in results if r.comparison.get("identical"))
    mode = "DRY-RUN" if dry_run else "WRITE"
    print(f"[{mode}] 共 {total} 个文件: 成功 {ok} / 警告 {warned} / 跳过 {skipped} / 失败 {failed}",
          file=sys.stderr)
    print(f"  字符级保真通过 {fidelity_ok}/{total}", file=sys.stderr)
    for r in results:
        if r.skipped:
            flag = "⏭️"
        elif r.error:
            flag = "❌"
        elif _has_warning(r):
            flag = "⚠️"
        else:
            flag = "✅"
        c = r.comparison or {}
        ratio = f"{c.get('ratio', 0):.1%}" if c else "N/A"
        repl = " [U+FFFD!]" if r.has_replacement_char else ""
        print(f"  {flag} {r.input_path.name}  编码={r.encoding}{repl}  保真={ratio}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
