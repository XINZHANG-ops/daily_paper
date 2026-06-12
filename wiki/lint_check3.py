#!/usr/bin/env python3
import os, re

# Check topic paper_counts vs actual Key Papers tables
print("=== Topic paper_count vs actual ===")
topics_with_issues = []
for f in os.listdir('./topics'):
    if not f.endswith('.md'):
        continue
    fp = f'./topics/{f}'
    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    m = re.search(r'^paper_count:\s*(\d+)', content, re.MULTILINE)
    frontmatter_count = int(m.group(1)) if m else 0

    rows = re.findall(r'^\|\s*\[\[[0-9]+\.[0-9]+\]\][^\|]*\|[^\|]*\|[^\|]*\|', content, re.MULTILINE)
    actual_count = len(rows)

    if frontmatter_count != actual_count:
        topics_with_issues.append((f, frontmatter_count, actual_count))

print(f'Topics with paper_count mismatch: {len(topics_with_issues)}')
for t in topics_with_issues:
    print(f'  {t[0]}: frontmatter={t[1]}, actual={t[2]}')

# Check entity paper_counts vs actual Appearances table rows
print("\n=== Entity paper_count vs actual ===")
entities_with_issues = []
for f in os.listdir('./entities'):
    if not f.endswith('.md'):
        continue
    fp = f'./entities/{f}'
    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    m = re.search(r'^paper_count:\s*(\d+)', content, re.MULTILINE)
    frontmatter_count = int(m.group(1)) if m else 0

    rows = re.findall(r'^\|\s*\[\[[0-9]+\.[0-9]+\]\][^\|]*\|[^\|]*\|[^\|]*\|', content, re.MULTILINE)
    actual_count = len(rows)

    if frontmatter_count != actual_count:
        entities_with_issues.append((f, frontmatter_count, actual_count))

print(f'Entities with paper_count mismatch: {len(entities_with_issues)}')
for e in entities_with_issues:
    print(f'  {e[0]}: frontmatter={e[1]}, actual={e[2]}')

# Check ideas evidence counts
print("\n=== Ideas with missing evidence ===")
for f in os.listdir('./ideas'):
    if not f.endswith('.md'):
        continue
    fp = f'./ideas/{f}'
    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    evidence_links = re.findall(r'\[\[[0-9]+\.[0-9]+\]\]|\[Note\s+[0-9]{4}-[0-9]{2}-[0-9]{2}\]', content)
    if len(evidence_links) == 0:
        print(f'  {f}: no evidence links')

print("\n=== Done ===")