import os, re, yaml
from collections import defaultdict

wiki_dir = '/Users/xinzhang/daily_paper/wiki'
issues = []
inbound = defaultdict(set)

all_pages = []
for cat in ['papers', 'topics', 'entities', 'ideas']:
    for f in os.listdir(os.path.join(wiki_dir, cat)):
        if f.endswith('.md'):
            path = os.path.join(wiki_dir, cat, f)
            all_pages.append((cat, f, path))

# First pass: collect all wikilinks
for cat, fname, path in all_pages:
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    rel = f'{cat}/{fname}'
    for m in re.finditer(r'\[\[([^\]]+)\]\]', content):
        target = m.group(1)
        if rel != 'WIKI.md':
            inbound[target].add(rel)

# Orphan check
with open(os.path.join(wiki_dir, 'index.md'), 'r') as fh:
    idx = fh.read()

for cat, fname, path in all_pages:
    slug = fname[:-3]
    has_inbound = False
    for target, sources in inbound.items():
        if target == slug or target == f'{cat}/{slug}':
            if sources:
                has_inbound = True
                break
    if not has_inbound:
        if f'{cat}/{slug}' in idx:
            has_inbound = True
    if not has_inbound and rel != 'WIKI.md':
        issues.append(f'ORPHAN: {cat}/{slug}')

# Check broken wikilinks in non-WIKI.md files
for cat, fname, path in all_pages:
    rel = f'{cat}/{fname}'
    if rel == 'WIKI.md':
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    for m in re.finditer(r'\[\[([^\]]+)\]\]', content):
        target = m.group(1)
        exists = False
        if target.startswith('entities/') or target.startswith('topics/') or target.startswith('ideas/'):
            exists = os.path.exists(os.path.join(wiki_dir, target + '.md'))
        elif re.match(r'^\d{4}\.\d+', target):
            exists = os.path.exists(os.path.join(wiki_dir, 'papers', target + '.md'))
        else:
            for c in ['entities', 'topics', 'ideas', 'papers']:
                if os.path.exists(os.path.join(wiki_dir, c, target + '.md')):
                    exists = True
                    break
        if not exists:
            issues.append(f'BROKEN: {target} in {rel}')

# Check topic paper_count vs Key Papers table
for cat, fname, path in all_pages:
    if cat != 'topics':
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if fm and 'paper_count' in fm:
                table_rows = re.findall(r'\|\s*\[\[\d+\.\d+\]\]', content)
                actual = len(table_rows)
                if actual != fm['paper_count']:
                    issues.append(f'TOPIC_MISMATCH: {fname} frontmatter={fm["paper_count"]} actual={actual}')
        except Exception:
            pass

# Check entity paper_count vs Appearances table
for cat, fname, path in all_pages:
    if cat != 'entities':
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if fm and 'paper_count' in fm:
                table_rows = re.findall(r'\|\s*\[\[\d+\.\d+\]\]', content)
                actual = len(table_rows)
                if actual != fm['paper_count']:
                    issues.append(f'ENTITY_MISMATCH: {fname} frontmatter={fm["paper_count"]} actual={actual}')
        except Exception:
            pass

# Check entity type is valid
valid_types = {'algorithm', 'model', 'benchmark', 'framework', 'protocol', 'concept', 'metric'}
for cat, fname, path in all_pages:
    if cat != 'entities':
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if fm and 'type' in fm:
                if fm['type'] not in valid_types:
                    issues.append(f'INVALID_TYPE: {fname} type={fm["type"]}')
        except Exception:
            pass

# Check ideas have evidence links
for cat, fname, path in all_pages:
    if cat != 'ideas':
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    evidence = re.findall(r'\[\[\d+\.\d+\]\]', content)
    if not evidence:
        issues.append(f'NO_EVIDENCE: {fname}')

# Check for shallow connections (just "Related:" or "See also:" without WHY)
for cat, fname, path in all_pages:
    if cat not in ('papers', 'topics', 'entities'):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^\s*[-*]\s*(Related|See also):?\s*$', stripped, re.IGNORECASE):
            issues.append(f'SHALLOW: {fname} line {i+1}: {stripped}')

# Check for duplicate pages (same concept, different name)
# Simple heuristic: check if title frontmatter is very similar
titles = {}
for cat, fname, path in all_pages:
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if fm and 'title' in fm:
                t = fm['title'].lower().strip()
                if t in titles:
                    issues.append(f'DUPLICATE_TITLE: {fname} vs {titles[t]} title="{fm["title"]}"')
                else:
                    titles[t] = fname
        except Exception:
            pass

for issue in sorted(set(issues)):
    print(issue)
if not issues:
    print('No issues found in comprehensive scan.')
