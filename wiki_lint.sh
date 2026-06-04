#!/usr/bin/env bash
# wiki_lint.sh — Launch ollama claude agent to lint/self-reflect the wiki.
#
# Checks broken links, removes wrong/duplicate info, improves connections.
# Scheduled to run daily at 11 PM via launchd.
#
# Usage:
#   ./wiki_lint.sh              # uses default model
#   ./wiki_lint.sh glm-5:cloud  # override model
#
set -Eeuo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$REPO/wiki"
_read_model() {
    python3 -c "
import json, os
c = json.load(open(os.path.expanduser('~/Desktop/model-config.json')))
print(c.get('projects', {}).get('$1') or c['default_model'])
" 2>/dev/null || echo "minimax-m3:cloud"
}
MODEL="${1:-$(_read_model daily-paper)}"
TODAY="$(date '+%Y-%m-%d')"
LINT_MARKER="$REPO/logs/lint_done_${TODAY}.json"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

if [[ ! -d "$WIKI_DIR" ]]; then
    log "wiki/ 目录不存在，无需 lint。"
    exit 0
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "ERROR: ollama not found in PATH" >&2
    exit 1
fi

log "开始 wiki lint，模型: $MODEL"

cd "$REPO"
git pull --ff-only || true

# ── 代码预扫描 ──────────────────────────────────────────────────────────────
PRESCAN_PY="/tmp/wiki_prescan_$$.py"
PROMPT_FILE="$(mktemp)"
trap 'rm -f "$PRESCAN_PY" "$PROMPT_FILE"' EXIT

cat > "$PRESCAN_PY" <<'PYTHON_EOF'
import re, sys
from pathlib import Path

wiki_dir = Path(sys.argv[1])
wikilink_re = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
all_pages, outgoing, incoming, thin_pages, categories = set(), {}, {}, [], []

if wiki_dir.exists():
    for item in sorted(wiki_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and any(item.glob('*.md')):
            categories.append(item.name)

for cat in categories:
    for md in (wiki_dir / cat).glob('*.md'):
        pg = f"{cat}/{md.stem}"
        all_pages.add(pg)
        content = md.read_text(encoding='utf-8')
        body = content[content.find('---', 3) + 3:] if content.startswith('---') and '---' in content[3:] else content
        lines = [l for l in body.splitlines() if l.strip()]
        if len(lines) < 10:
            thin_pages.append((pg, len(lines)))
        for link in wikilink_re.findall(content):
            outgoing.setdefault(pg, []).append(link)
            incoming.setdefault(link, []).append(pg)

broken, orphans = [], []
for src, links in outgoing.items():
    for link in links:
        if link not in all_pages:
            slug = link.split('/')[-1]
            if not any(p.endswith(f'/{slug}') or p == slug for p in all_pages):
                broken.append((src, link))

for pg in all_pages:
    slug = pg.split('/')[-1]
    if pg not in incoming and slug not in incoming:
        orphans.append(pg)

total = len(broken) + len(orphans) + len(thin_pages)
if total == 0:
    print("CLEAR")
    sys.exit(0)

lines_out = [f"代码预扫描发现结构问题（共 {total} 个）— 先修复全部：\n"]
if broken:
    lines_out.append("断链（链接目标不存在）：")
    for src, link in broken:
        lines_out.append(f"  - `{src}` → 断链 [[{link}]]")
    lines_out.append("")
if orphans:
    lines_out.append("孤儿页（无其他页面链接到它们）：")
    for p in orphans:
        lines_out.append(f"  - `{p}`")
    lines_out.append("")
if thin_pages:
    lines_out.append("空页（去掉 frontmatter 后正文不足 10 行）：")
    for p, n in thin_pages:
        lines_out.append(f"  - `{p}` （{n} 行）")
    lines_out.append("")
print('\n'.join(lines_out))
PYTHON_EOF

PRESCAN_OUT="$(python3 "$PRESCAN_PY" "$WIKI_DIR")"

if [[ "$PRESCAN_OUT" == "CLEAR" ]]; then
    log "预扫描通过，无断链/孤儿页/空页，跳过 LLM。"
    LINT_OUTPUT="• 结构检查通过 — 无断链、孤儿页或空页。"
    python3 -c "
import json, sys
marker = {'date': '$TODAY', 'project': 'daily_paper', 'status': 'done', 'diff_stat': '', 'summary': sys.stdin.read().strip()}
with open('$LINT_MARKER', 'w') as f:
    json.dump(marker, f, ensure_ascii=False)
" <<< "$LINT_OUTPUT"
    exit 0
fi

# ── 构建 prompt ─────────────────────────────────────────────────────────────
printf '%s\n\n' "$PRESCAN_OUT" > "$PROMPT_FILE"

cat >> "$PROMPT_FILE" <<'STATIC_PART'
你正在对 daily_paper 研究 wiki 进行每日自检和健康检查。

=== 任务：WIKI LINT ===

对 wiki/ 目录进行全面检查。逐项执行以下所有检查。发现问题立刻修复，不要只报告问题。

## 第一步 — 修复上方列出的预扫描问题（代码精准检测，必须全部修复）
- 断链：修正链接目标，或删除链接
- 孤儿页：从相关页面添加有意义的 [[wikilink]] 指向它
- 空页：补充真实内容，或合并后删除

## 第二步 — 结构完整性
1. 读取 wiki/index.md。检查每个列出的页面是否存在，删除不存在的条目。
2. 扫描 wiki/papers/、wiki/topics/、wiki/entities/、wiki/ideas/ 查找未在 index.md 中的 .md 文件，添加它们。
3. 检查 topic 页面：paper_count 是否与 Key Papers 表格中的实际论文数一致？修正不匹配。
4. 检查 entity 页面：有没有 0 次论文引用的 entity？补充出现记录或删除。
5. 检查 idea 页面：有没有 0 个 evidence 链接的 idea？补充证据或删除。

## 第三步 — 错误与重复信息
1. 查找覆盖相同概念的重复页面（如同一模型的两个 entity 页面）。合并，保留内容更丰富的。
2. 检查页面内重复的段落或章节。
3. 检查页面之间不一致的事实信息（如论文日期不同）并修正。
4. 检查 frontmatter 的日期、slug、type 是否一致正确。

## 第四步 — 连接质量
1. 找出只写 "相关：" 或 "参见：" 而没有标注的链接，重写说明 WHY。
2. 找出共享 2+ 个 entity 但没有直接连接的论文，添加带标注的连接。
3. 检查 topic 页面是否缺少 ## Evolution 章节，补写时间线叙述。
4. 检查 topic 页面是否缺少 ## Patterns & Insights，从论文中综合洞察。
5. 检查浅薄的 entity 页面（只有名称没有描述），从论文内容中充实。

## 第五步 — 索引与日志
1. 重建 wiki/index.md，包含准确的数量和所有页面。
2. 向 wiki/log.md 追加一条 lint 条目，注明修复了什么。

最后输出 3-5 条中文要点摘要，每条以 • 开头，概括发现并修复了什么。每条不超过 100 字。
只输出要点，不输出其他内容。
STATIC_PART

# ── 调用 LLM ────────────────────────────────────────────────────────────────
LINT_OUTPUT="$(ollama launch claude \
    --model "$MODEL" \
    --yes \
    -- \
    -p "$(cat "$PROMPT_FILE")" \
    --permission-mode dontAsk 2>&1)"

EXIT_CODE=$?
echo "$LINT_OUTPUT" >> "$REPO/logs/lint.log"
log "Wiki lint 完成（退出码 $EXIT_CODE）。"

cd "$REPO"
git add -A

DIFF_STAT="$(git diff --cached --stat 2>/dev/null | tail -1)"
git commit -m "wiki: lint $TODAY" || true
git push || true

# Write lint completion marker with summary for xin-knowledge-bot
python3 -c "
import json, sys
summary = sys.stdin.read().strip()
if len(summary) > 2000:
    summary = summary[-2000:]
marker = {
    'date': '$TODAY',
    'project': 'daily_paper',
    'status': 'done',
    'diff_stat': '''$DIFF_STAT''',
    'summary': summary,
}
with open('$LINT_MARKER', 'w') as f:
    json.dump(marker, f, ensure_ascii=False)
" <<< "$LINT_OUTPUT"

exit $EXIT_CODE
