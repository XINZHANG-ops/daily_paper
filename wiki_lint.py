import os, re, json, glob
from pathlib import Path
from collections import defaultdict
from itertools import combinations

wiki_dir = Path('/Users/xinzhang/daily_paper/wiki')

md_files = []
for subdir in ['papers', 'topics', 'entities', 'ideas']:
    md_files.extend(wiki_dir.glob(f'{subdir}/*.md'))

pages = {}
for f in md_files:
    rel = f.relative_to(wiki_dir)
    pages[str(rel)] = f.read_text('utf-8')

index_md = wiki_dir.joinpath('index.md').read_text('utf-8')

index_papers = re.findall(r'\[([\d.]+)\]\(papers/[\d.]+\.md\)', index_md)
index_topics = re.findall(r'\[([^\]]+)\]\(topics/[^)]+\.md\)', index_md)
index_entities = re.findall(r'\[([^\]]+)\]\(entities/[^)]+\.md\)', index_md)
index_ideas = re.findall(r'\[([^\]]+)\]\(ideas/[^)]+\.md\)', index_md)

print(f"Papers in index.md: {len(index_papers)}")
print(f"Topics in index.md: {len(index_topics)}")
print(f"Entities in index.md: {len(index_entities)}")
print(f"Ideas in index.md: {len(index_ideas)}")

papers_on_disk = sorted([f.name.replace('.md','') for f in wiki_dir.glob('papers/*.md')])
topics_on_disk = sorted([f.stem for f in wiki_dir.glob('topics/*.md')])
entities_on_disk = sorted([f.stem for f in wiki_dir.glob('entities/*.md')])
ideas_on_disk = sorted([f.stem for f in wiki_dir.glob('ideas/*.md')])

print(f"Papers on disk: {len(papers_on_disk)}")
print(f"Topics on disk: {len(topics_on_disk)}")
print(f"Entities on disk: {len(entities_on_disk)}")
print(f"Ideas on disk: {len(ideas_on_disk)}")

missing_from_index = {
    'papers': [p for p in papers_on_disk if p not in index_papers],
    'topics': [t for t in topics_on_disk if t not in index_topics],
    'entities': [e for e in entities_on_disk if e not in index_entities],
    'ideas': [i for i in ideas_on_disk if i not in index_ideas],
}

missing_from_disk = {
    'papers': [p for p in index_papers if p not in papers_on_disk],
    'topics': [t for t in index_topics if t not in topics_on_disk],
    'entities': [e for e in index_entities if e not in entities_on_disk],
    'ideas': [i for i in index_ideas if i not in ideas_on_disk],
}

for k,v in missing_from_index.items():
    if v:
        print(f"On disk but not in index ({k}): {v}")
for k,v in missing_from_disk.items():
    if v:
        print(f"In index but not on disk ({k}): {v}")

wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
all_wikilinks = defaultdict(set)
for rel_path, content in pages.items():
    for link in wikilink_pattern.findall(content):
        all_wikilinks[link].add(rel_path)

targets = set()
for rel_path in pages:
    stem = Path(rel_path).stem
    targets.add(stem)
    targets.add(rel_path.replace('.md', ''))

broken = []
for link, sources in all_wikilinks.items():
    link_clean = link.strip().lower().replace(' ', '-')
    found = False
    for t in targets:
        if t.lower().replace(' ', '-') == link_clean or Path(t).stem.lower() == link_clean:
            found = True
            break
    if not found:
        broken.append((link, sources))

print(f"\nBroken wikilinks: {len(broken)}")
for link, sources in broken:
    print(f"  [[{link}]] from {sources}")

inbound = defaultdict(set)
for rel_path, content in pages.items():
    source_stem = Path(rel_path).stem
    for link in wikilink_pattern.findall(content):
        inbound[link.lower().strip().replace(' ', '-')].add(source_stem)

orphans = []
for rel_path in pages:
    stem = Path(rel_path).stem
    stem_clean = stem.lower().replace(' ', '-')
    ib = set()
    for k, v in inbound.items():
        if k == stem_clean and stem in v:
            ib.update(v)
    ib.discard(stem)
    if len(ib) == 0:
        orphans.append(stem)

print(f"\nOrphan pages: {len(orphans)}")
for o in orphans:
    print(f"  {o}")

print("\n--- Topic paper counts ---")
topic_paper_pattern = re.compile(r'\| \[([\d.]+)\]\(papers/[\d.]+\.md\) \|')
for topic in topics_on_disk:
    content = pages.get(f'topics/{topic}.md', '')
    paper_ids = topic_paper_pattern.findall(content)
    idx_match = re.search(rf'\| \[{re.escape(topic)}\]\(topics/{re.escape(topic)}\.md\) \| (\d+) \|', index_md)
    idx_count = int(idx_match.group(1)) if idx_match else 0
    if len(paper_ids) \!= idx_count:
        print(f"  Topic {topic}: table has {len(paper_ids)}, index says {idx_count}")

print("\n--- Entity appearances ---")
entity_mention_pattern = re.compile(r'\*\*Appearances:\*\*\s*(.*?)(?:\n\n|\n##|\Z)', re.DOTALL)
for entity in entities_on_disk:
    content = pages.get(f'entities/{entity}.md', '')
    appearances = entity_mention_pattern.search(content)
    if appearances:
        apps = re.findall(r'\[([\d.]+)\]', appearances.group(1))
        if len(apps) == 0:
            print(f"  Entity {entity}: zero appearances")
    else:
        apps = re.findall(r'papers/(\d+\.\d+)', content)
        if len(apps) == 0:
            print(f"  Entity {entity}: zero appearances (no Appearances section)")

print("\n--- Idea evidence ---")
for idea in ideas_on_disk:
    content = pages.get(f'ideas/{idea}.md', '')
    evidence = re.findall(r'\[([\d.]+)\]', content)
    if len(evidence) == 0:
        print(f"  Idea {idea}: zero evidence links")

print("\n--- Potential duplicate names ---")
for a, b in combinations(entities_on_disk, 2):
    a_norm = a.replace('-', '').replace('_', '')
    b_norm = b.replace('-', '').replace('_', '')
    if a_norm == b_norm and a \!= b:
        print(f"  Possible duplicate entities: {a} and {b}")

print("\nDone with automated checks.")
