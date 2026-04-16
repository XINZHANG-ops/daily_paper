# daily_paper Wiki — Project Schema

This file defines the conventions for building and maintaining the wiki. Read alongside `llm-wiki.md` for the general pattern. When the two conflict, this file takes precedence.

## Context

This wiki tracks AI research papers fetched daily from HuggingFace, plus the reader's personal notes and insights. Each day up to 3 papers are selected, summarized by an LLM, and stored in `summaries.jsonl`. The wiki compiles those papers — along with personal reading notes — into a structured, richly interlinked knowledge base.

**Your job**: Read new papers and notes from `wiki/raw/`, integrate them into the wiki, and maintain rich annotated connections across all pages.

---

## Directory Structure

```
wiki/
  WIKI.md              # This file (project schema)
  index.md             # Catalog of all wiki pages (update on every ingest)
  log.md               # Append-only ingest log
  processed.json       # {"processed": ["arxiv_id1", ...]}
  pdf_cache/           # Raw PDF text per paper (gitignored, do not modify)
  raw/                 # Staged input for current ingest (gitignored, read-only)
  papers/              # One .md page per paper
  topics/              # Cross-cutting concept/theme pages
  entities/            # Named technical things: models, datasets, algorithms, benchmarks, frameworks
  ideas/               # Cross-cutting insights, patterns, and personal observations
```

**IMPORTANT DISTINCTIONS:**
- `entities/` are for TECHNICAL THINGS: models (GPT-4, Qwen3), datasets (MMLU, WebShop), algorithms (PPO, GRPO), benchmarks (Video-MME), frameworks, architectures. NEVER put people in entities/.
- `ideas/` are for INSIGHTS that emerge from reading multiple papers or from personal notes: "entropy metrics can be misleading", "sampling is fundamentally optimization", "RL training has multiple independent failure modes".
- `topics/` are for BROAD RESEARCH AREAS: reinforcement-learning, video-generation, computer-vision.

---

## Raw Input Format

Each subdirectory under `wiki/raw/` represents one paper to ingest:

```
wiki/raw/{date}_{arxiv_id}/
  summary.json         # Paper metadata and AI-generated summary
  pdf.txt              # Full extracted PDF text
  notes.md             # (optional) Personal reading notes for this date
```

Additionally, `wiki/raw/_all_notes/` contains personal reading notes from recent dates (not necessarily matching paper dates). These notes contain the reader's own insights, connections to their projects, and observations. Scan these for ideas and cross-references.

`summary.json` fields:
- `title` — paper title
- `published_at` — arXiv publication date (YYYY-MM-DD)
- `url` — arXiv PDF URL
- `content` — AI-generated English summary
- `content_zh` — AI-generated Chinese summary (if present)
- `date` — date added to our database (YYYY-MM-DD)
- `personal_notes` — (optional) reader's notes for this date

---

## Connection Rules — THE MOST IMPORTANT PART

Every `## Connections` section on every page must use **annotated [[wikilinks]]**. Every link MUST explain WHY and HOW things connect. This is what makes the wiki valuable.

### BAD — never generate these:

```markdown
## Connections
- Related: [[topics/reinforcement-learning]]
- See also: [[2604.03128]]
- [[entities/ppo]]
- 相关论文: [[2604.06268]]
```

### GOOD — always generate these:

```markdown
## Connections
- [[2604.03128]] — Both papers address RL training failure modes, but from opposite angles: RLSD fixes credit assignment (teacher-student information asymmetry) while this paper fixes signal quality (reward variance filtering). Together they suggest standard RL objectives have at least two independent structural vulnerabilities.
- [[entities/ppo]] — PPO is the primary RL algorithm in this paper's experiments; the template collapse vulnerability is algorithm-agnostic (also affects DAPO, GRPO) but manifests differently in PPO's clipped objective.
- [[ideas/entropy-is-misleading]] — This paper provides the strongest evidence that entropy-based monitoring can be fundamentally flawed: I(X;Z) can collapse to zero while H(Z|X) stays high.
- [[topics/reinforcement-learning]] — Extends the topic's understanding by showing that even within-input diversity (high entropy) can mask cross-input uniformity — a failure mode not discussed in any prior paper in this topic.
```

### Connection annotation checklist:
1. Does the annotation explain a SPECIFIC relationship, not just "related"?
2. Does it say something a reader couldn't guess from the page titles alone?
3. Would removing this annotation lose important context?

If any answer is no, rewrite the annotation.

---

## Paper Page Format

File: `wiki/papers/{arxiv_id}.md`

```markdown
---
title: "Full Paper Title"
arxiv_id: 2503.01785
published_at: 2025-03-03
date_added: 2025-03-05
url: http://arxiv.org/pdf/2503.01785
topics: [topic_slug_1, topic_slug_2]
entities: [entity_slug_1, entity_slug_2]
---

# Paper Title

**Published**: 2025-03-03 | **Added**: 2025-03-05 | **arXiv**: [2503.01785](http://arxiv.org/pdf/2503.01785)

## Summary
<!-- 2-3 paragraph synthesis combining the AI summary and key insights from the PDF -->

## Key Contributions
- Contribution 1
- Contribution 2

## Method
<!-- Core technical approach. Be concrete. -->

## Results
<!-- Key numbers, benchmarks, comparisons. -->

## Limitations & Future Work

## Personal Notes
<!-- Content from the reader's notes if available for this paper's date.
     Include their own insights, connections to their projects, questions.
     If no notes available, omit this section entirely. -->

## Connections
<!-- ANNOTATED [[wikilinks]] to other papers, topics, entities, ideas.
     Every link must explain WHY. See Connection Rules above. -->
```

---

## Topic Page Format

File: `wiki/topics/{topic_slug}.md`

Topic slugs: lowercase with hyphens (e.g. `reinforcement-learning`, `video-generation`).

```markdown
---
title: "Human-Readable Topic Name"
slug: topic_slug
paper_count: N
last_updated: YYYY-MM-DD
---

# Topic Name

## Overview
<!-- 2-4 paragraph synthesis of the state of this topic based on ALL papers seen so far.
     Update this section each time a new paper is added. -->

## Evolution
<!-- Chronological NARRATIVE of how this topic has developed across papers we've seen.
     NOT a list of papers. A story showing progression of ideas.

     Example:
     In early April, RLSD revealed that self-distillation in RLVR has an irreducible
     mutual information gap caused by teacher-student information asymmetry...
     Three days later, RAGEN-2 showed a complementary failure mode — template collapse —
     where reasoning appears diverse within inputs but becomes input-agnostic across inputs...
     Together these papers suggest the field is converging on understanding WHY RL training
     fails silently, not just detecting failure after the fact. -->

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2503.01785]] Paper Title | 2025-03-03 | One-line contribution to this topic |

## Patterns & Insights
<!-- Synthesized observations that emerge from looking across all papers in this topic.
     What themes recur? What contradictions exist? What's the trajectory? -->

## Open Problems
<!-- Questions this body of work has not yet answered -->

## Connections
<!-- ANNOTATED [[wikilinks]] to related topics, entities, ideas -->
```

---

## Entity Page Format

File: `wiki/entities/{entity_slug}.md`

Entity slugs: lowercase with hyphens. Entities are TECHNICAL THINGS only: models, datasets, algorithms, benchmarks, frameworks, architectures. NEVER people.

```markdown
---
title: "Entity Name"
slug: entity_slug
type: model|dataset|algorithm|benchmark|framework|architecture
paper_count: N
last_updated: YYYY-MM-DD
---

# Entity Name

## What It Is
<!-- 1-2 paragraph description synthesized from all papers that mention it -->

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06268]] | core method | Used as baseline RL algorithm for template collapse experiments |

## Connections
<!-- ANNOTATED [[wikilinks]] explaining WHY/HOW this relates to other entities, topics, ideas -->
```

---

## Idea Page Format

File: `wiki/ideas/{idea_slug}.md`

Ideas are cross-cutting insights, patterns, and personal observations — especially drawn from reading notes.

```markdown
---
title: "Idea Title"
slug: idea_slug
source: paper|note|synthesis
last_updated: YYYY-MM-DD
---

# Idea Title

## The Insight
<!-- What is the core observation? 1-2 paragraphs. -->

## Evidence
<!-- Which papers or notes support this? With annotated links -->
- [[2604.06268]] — Template collapse shows that entropy metrics can be fundamentally misleading
- [Note 2026-02-25] — Personal observation about sampling-as-optimization connects to the same theme

## Implications
<!-- What does this mean for the field or for the reader's work? -->

## Connections
<!-- ANNOTATED [[wikilinks]] to related ideas, topics, entities, papers -->
```

---

## index.md Format

```markdown
# Wiki Index

Last updated: YYYY-MM-DD | Papers: N | Topics: M | Entities: E | Ideas: I

## Papers

| arXiv ID | Title | Date Added | Topics |
|----------|-------|------------|--------|
| [2503.01785](papers/2503.01785.md) | Paper Title | 2025-03-05 | topic1, topic2 |

## Topics

| Topic | Papers | Last Updated |
|-------|--------|-------------|
| [Topic Name](topics/topic_slug.md) | 12 | 2025-03-05 |

## Entities

| Entity | Type | Papers | Last Updated |
|--------|------|--------|-------------|
| [Entity Name](entities/entity_slug.md) | algorithm | 3 | 2025-03-05 |

## Ideas

| Idea | Source | Last Updated |
|------|--------|-------------|
| [Idea Title](ideas/idea_slug.md) | synthesis | 2025-03-05 |
```

---

## log.md Format

Append-only. Each ingest adds one entry:

```markdown
## [2025-03-05] ingest | 3 papers

- [[2503.01785]] Paper Title One
- [[2503.01786]] Paper Title Two

Topics updated: reinforcement-learning, agent-systems
Entities created: ppo, grpo
Ideas created: entropy-is-misleading
Notes integrated: 2 dates
```

---

## processed.json Format

```json
{
  "processed": ["2503.01785", "2503.01786"]
}
```

After successfully processing a paper, append its arxiv ID to this list.

---

## Ingest Workflow

For each paper directory in `wiki/raw/` (skip `_all_notes`):

1. **Read** `summary.json`, `pdf.txt`, and `notes.md` (if present)
2. **Extract** arxiv ID from the URL in `summary.json`
3. **Skip** if arxiv ID is already in `wiki/processed.json`
4. **Identify topics** (2-4): broad research areas this paper belongs to
5. **Identify entities** (2-6): specific models, datasets, algorithms, benchmarks, frameworks mentioned
6. **Identify ideas** (0-3): cross-cutting insights, especially from personal notes
7. **Write** `wiki/papers/{arxiv_id}.md` with annotated `## Connections`
8. **Create/update** each `wiki/topics/{slug}.md`:
   - Add paper to Key Papers table
   - Update Overview synthesis
   - Update Evolution narrative
   - Update Patterns & Insights
   - Update `paper_count` and `last_updated`
9. **Create/update** each `wiki/entities/{slug}.md`:
   - Add paper to Appearances table
   - Update description
   - Update connections
10. **Create/update** each `wiki/ideas/{slug}.md` (if relevant ideas found)
11. **Update** `wiki/index.md`: add rows, update counts
12. **Update** `wiki/processed.json`: append the arxiv ID

After processing ALL papers:
13. **Read** notes from `wiki/raw/_all_notes/` (if directory exists)
14. **Scan** notes for insights that connect to existing wiki content
15. **Create/update** idea pages based on note insights
16. **Update** paper pages with `## Personal Notes` where date matches
17. **Append** to `wiki/log.md` with summary of what was created/updated

---

## Lint Checklist

### Structural
- Topic pages with `paper_count` that doesn't match actual papers listed
- Papers in `index.md` without a corresponding `.md` file
- Topic/entity slugs referenced in frontmatter without a corresponding page
- Papers not linked from any topic page (orphans)
- Topics not linked from any paper (orphan topics)
- Entities with no paper appearances
- Ideas with no evidence links

### Connection Quality
- Connections that just say "Related:", "See also:", or link without annotation → rewrite with WHY
- Papers that share 2+ entities but have no direct connection to each other → add connection
- Topic pages missing `## Evolution` section → write chronological narrative
- Topic pages missing `## Patterns & Insights` → synthesize from papers
- People appearing in `entities/` → these belong in ideas or remove entirely
- Shallow entity pages with only a name and no description → flesh out from paper content
