#!/usr/bin/env python3
"""Deep quality checks on wiki/ directory."""
import re
from pathlib import Path
from collections import defaultdict

WIKI_ROOT = Path("/Users/xinzhang/daily_paper/wiki")


def parse_frontmatter(content: str):
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1].strip()
    body = parts[2].strip()
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                # Parse list like [foo, bar]
                items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
                fm[key] = items
            else:
                fm[key] = val.strip('"').strip("'")
    return fm, body


def extract_section(body: str, section_name: str):
    """Extract content of a markdown section by name (case-insensitive)."""
    pattern = re.compile(rf"^##\s+{re.escape(section_name)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return None
    start = match.end()
    # Find next ## heading
    next_heading = re.search(r"^##\s+", body[start:], re.MULTILINE)
    if next_heading:
        end = start + next_heading.start()
        return body[start:end].strip()
    return body[start:].strip()


def has_meaningful_content(section_body: str, min_chars: int = 50):
    """Check if section has at least min_chars of meaningful text after removing markdown."""
    if not section_body:
        return False
    # Remove wikilinks
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", section_body)
    # Remove markdown links
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove bold/italic
    text = re.sub(r"[*_]+", "", text)
    # Remove headings
    text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return len(text) >= min_chars


def find_shallow_connections(body: str):
    """Find bare wikilinks with no explanatory text on the same line."""
    issues = []
    for line in body.splitlines():
        # Find wikilinks in this line
        wikilinks = re.findall(r"\[\[([^\]]+)\]\]", line)
        if not wikilinks:
            continue
        # Check if line has explanatory text beyond the wikilink and list markers/whitespace
        # Remove the wikilink itself
        line_without_links = re.sub(r"\[\[([^\]]+)\]\]", "", line)
        # Remove markdown syntax characters
        cleaned = re.sub(r"[*_#\-\+\|]", "", line_without_links)
        # If there's meaningful text left (not just whitespace/punctuation), it's not shallow
        meaningful = re.sub(r"\s+|\.|,|;|:|!|\?", "", cleaned)
        if not meaningful:
            for link in wikilinks:
                issues.append((line.strip(), link))
    return issues


def find_section_range(body: str, section_name: str):
    """Return (start, end) indices of a section."""
    pattern = re.compile(rf"^##\s+{re.escape(section_name)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return None
    start = match.end()
    next_heading = re.search(r"^##\s+", body[start:], re.MULTILINE)
    if next_heading:
        end = start + next_heading.start()
        return (start, end)
    return (start, len(body))


def main():
    results = {
        "missing_evolution": [],
        "missing_patterns": [],
        "shallow_entities": [],
        "shallow_connections": [],
        "missing_paper_connections": [],
    }

    # Gather files
    topic_files = sorted((WIKI_ROOT / "topics").glob("*.md"))
    entity_files = sorted((WIKI_ROOT / "entities").glob("*.md"))
    paper_files = sorted((WIKI_ROOT / "papers").glob("*.md"))
    idea_files = sorted((WIKI_ROOT / "ideas").glob("*.md"))

    all_pages = {
        "topic": topic_files,
        "entity": entity_files,
        "paper": paper_files,
        "idea": idea_files,
    }

    # 1. Missing Evolution in topic pages
    for f in topic_files:
        content = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        section = extract_section(body, "Evolution")
        if section is None:
            results["missing_evolution"].append(str(f.relative_to(WIKI_ROOT)))

    # 2. Missing Patterns & Insights in topic pages
    for f in topic_files:
        content = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        section = extract_section(body, "Patterns & Insights")
        if section is None:
            results["missing_patterns"].append(str(f.relative_to(WIKI_ROOT)))

    # 3. Shallow entity pages (What It Is < 50 meaningful chars)
    for f in entity_files:
        content = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        section = extract_section(body, "What It Is")
        if section is None:
            results["shallow_entities"].append((str(f.relative_to(WIKI_ROOT)), "MISSING 'What It Is' section"))
        elif not has_meaningful_content(section, min_chars=50):
            meaningful_text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", section)
            meaningful_text = re.sub(r"\s+", " ", meaningful_text).strip()
            results["shallow_entities"].append((str(f.relative_to(WIKI_ROOT)), f"shallow ({len(meaningful_text)} meaningful chars): {meaningful_text[:80]}..."))

    # 4. Shallow connections in all pages
    for category, files in all_pages.items():
        for f in files:
            content = f.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(content)
            # Check Connections section specifically
            range_conn = find_section_range(body, "Connections")
            if range_conn is None:
                continue
            conn_body = body[range_conn[0]:range_conn[1]]
            shallow = find_shallow_connections(conn_body)
            for line_content, link in shallow:
                results["shallow_connections"].append(
                    (str(f.relative_to(WIKI_ROOT)), line_content, link)
                )

    # 5. Papers sharing 2+ entities but no direct link
    paper_entities = {}
    paper_bodies = {}
    for f in paper_files:
        content = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        paper_entities[f.name] = set(fm.get("entities", []))
        paper_bodies[f.name] = body

    paper_names = list(paper_entities.keys())
    for i in range(len(paper_names)):
        for j in range(i + 1, len(paper_names)):
            p1, p2 = paper_names[i], paper_names[j]
            shared = paper_entities[p1] & paper_entities[p2]
            if len(shared) >= 2:
                # Check if either links to the other
                link1 = f"[[{p1.replace('.md', '')}]]"
                link2 = f"[[{p2.replace('.md', '')}]]"
                body1 = paper_bodies[p1]
                body2 = paper_bodies[p2]
                has_link = link1 in body2 or link2 in body1
                if not has_link:
                    results["missing_paper_connections"].append(
                        (p1, p2, sorted(shared))
                    )

    # Print results
    print("=" * 80)
    print("WIKI DEEP QUALITY CHECK RESULTS")
    print("=" * 80)

    print(f"\n1. MISSING EVOLUTION SECTION ({len(results['missing_evolution'])} topic pages)")
    print("-" * 40)
    for item in results["missing_evolution"]:
        print(f"  - {item}")

    print(f"\n2. MISSING PATTERNS & INSIGHTS SECTION ({len(results['missing_patterns'])} topic pages)")
    print("-" * 40)
    for item in results["missing_patterns"]:
        print(f"  - {item}")

    print(f"\n3. SHALLOW ENTITY PAGES ({len(results['shallow_entities'])} entities)")
    print("-" * 40)
    for item in results["shallow_entities"]:
        print(f"  - {item[0]}: {item[1]}")

    print(f"\n4. SHALLOW CONNECTIONS ({len(results['shallow_connections'])} instances)")
    print("-" * 40)
    for item in results["shallow_connections"]:
        print(f"  - {item[0]}")
        print(f"    Line: '{item[1]}' -> shallow link to [[{item[2]}]]")

    print(f"\n5. MISSING PAPER-TO-PAPER CONNECTIONS ({len(results['missing_paper_connections'])} pairs)")
    print("-" * 40)
    for p1, p2, shared in results["missing_paper_connections"]:
        print(f"  MISSING_CONNECTION: {p1} and {p2} share entities {shared} but have no direct link")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  Missing Evolution sections:         {len(results['missing_evolution'])}")
    print(f"  Missing Patterns & Insights:        {len(results['missing_patterns'])}")
    print(f"  Shallow entity pages:                 {len(results['shallow_entities'])}")
    print(f"  Shallow connections:                  {len(results['shallow_connections'])}")
    print(f"  Missing paper connections:            {len(results['missing_paper_connections'])}")
    total_issues = (
        len(results["missing_evolution"])
        + len(results["missing_patterns"])
        + len(results["shallow_entities"])
        + len(results["shallow_connections"])
        + len(results["missing_paper_connections"])
    )
    print(f"  TOTAL ISSUES:                         {total_issues}")
    print("=" * 80)


if __name__ == "__main__":
    main()
