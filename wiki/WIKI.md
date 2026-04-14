# daily_paper Wiki — Project Schema

This file defines the project-specific conventions for building and maintaining the wiki for the `daily_paper` repository. It is meant to be read alongside `llm-wiki.md`, which describes the general wiki pattern. When the two conflict, this file takes precedence.

## Context

This wiki tracks AI research papers fetched daily from HuggingFace. Each day, up to 3 papers are selected, summarized by an LLM, and stored in `summaries.jsonl`. This wiki compiles those papers into a structured, interlinked knowledge base.

**Your job**: Read new papers from `wiki/raw/`, integrate them into the wiki, and keep everything consistent and cross-referenced.

---

## Directory Structure

```
wiki/
  WIKI.md              # This file (project schema)
  index.md             # Catalog of all wiki pages (update on every ingest)
  log.md               # Append-only ingest log
  processed.json       # {"processed": ["arxiv_id1", "arxiv_id2", ...]}
  pdf_cache/           # Raw PDF text per paper (gitignored, do not modify)
  raw/                 # Staged input for current ingest (gitignored, read-only for you)
  papers/              # One .md page per paper
  topics/              # One .md page per topic/concept
```

---

## Raw Input Format

Each subdirectory under `wiki/raw/` represents one paper to ingest:

```
wiki/raw/{date}_{arxiv_id}/
  summary.json         # Paper metadata and AI-generated summary
  pdf.txt              # Full extracted PDF text
```

`summary.json` fields (not all papers have all fields):
- `title` — paper title
- `published_at` — arXiv publication date (YYYY-MM-DD)
- `url` — arXiv PDF URL (e.g. `http://arxiv.org/pdf/2503.01785`)
- `content` — AI-generated English summary (5-point structure)
- `content_zh` — AI-generated Chinese summary (if present)
- `date` — date added to our database (YYYY-MM-DD)
- `questions` — auto-generated quiz questions (if present)
- `flow_chart` — SVG string (ignore this field)

The arxiv ID can be extracted from the URL: `http://arxiv.org/pdf/{arxiv_id}`.

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
---

# Paper Title

**Published**: 2025-03-03 | **Added**: 2025-03-05 | **arXiv**: [2503.01785](http://arxiv.org/pdf/2503.01785)

## Summary

<!-- 2-3 paragraph synthesis combining the AI summary and key insights from the PDF -->

## Key Contributions

- Contribution 1
- Contribution 2
- Contribution 3

## Method

<!-- Core technical approach, architecture, or algorithm. Be concrete. -->

## Results

<!-- Key numbers, benchmarks, comparisons. What did they beat and by how much? -->

## Limitations & Future Work

<!-- What the paper acknowledges it doesn't solve. -->

## Related Papers

<!-- Links to other wiki papers this connects to. Use [[arxiv_id]] format. -->
- [[2501.12345]] — brief note on the connection

## Topics

<!-- Links to topic pages -->
- [[topics/topic_name]] — why this paper is relevant to this topic
```

---

## Topic Page Format

File: `wiki/topics/{topic_slug}.md`

Topic slugs use lowercase with underscores (e.g. `diffusion_models`, `rlhf`, `vision_language_models`).

```markdown
---
title: "Human-Readable Topic Name"
slug: topic_slug
paper_count: 12
last_updated: 2025-03-05
---

# Topic Name

## Overview

<!-- 2-4 paragraph synthesis of the state of this topic based on all papers seen so far.
     Update this section each time a new paper is added. Reflect the evolving picture. -->

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2503.01785]] Paper Title | 2025-03-03 | One-line contribution |

## Open Problems

<!-- Questions this body of work has not yet answered, based on limitations sections -->

## Connections

<!-- Links to related topic pages -->
- [[topics/related_topic]] — brief note on overlap
```

---

## index.md Format

```markdown
# Wiki Index

Last updated: YYYY-MM-DD | Papers: N | Topics: M

## Papers

| arXiv ID | Title | Date Added | Topics |
|----------|-------|------------|--------|
| [2503.01785](papers/2503.01785.md) | Paper Title | 2025-03-05 | topic1, topic2 |

## Topics

| Topic | Papers | Last Updated |
|-------|--------|-------------|
| [Diffusion Models](topics/diffusion_models.md) | 12 | 2025-03-05 |
```

---

## log.md Format

Append-only. Each ingest adds one entry:

```markdown
## [2025-03-05] ingest | 3 papers

- [[2503.01785]] Paper Title One
- [[2503.01786]] Paper Title Two
- [[2503.01787]] Paper Title Three

Topics updated: diffusion_models, rlhf
```

---

## processed.json Format

```json
{
  "processed": ["2503.01785", "2503.01786", "2503.01787"]
}
```

After successfully processing a paper, append its arxiv ID to this list.

---

## Ingest Workflow

For each paper directory in `wiki/raw/`:

1. **Read** `summary.json` and `pdf.txt`
2. **Extract** arxiv ID from the URL in `summary.json`
3. **Skip** if arxiv ID is already in `wiki/processed.json`
4. **Identify topics**: Read the paper and decide which topic pages it belongs to (2-4 topics). Create new topic pages if the topic doesn't exist yet.
5. **Write** `wiki/papers/{arxiv_id}.md` using the paper page format above
6. **Update** each relevant `wiki/topics/{topic}.md`:
   - Add the paper to the Key Papers table
   - Update the Overview synthesis to reflect the new paper
   - Update `paper_count` and `last_updated` in frontmatter
7. **Update** `wiki/index.md`: add the paper row, update counts
8. **Append** to `wiki/log.md`
9. **Update** `wiki/processed.json`: append the arxiv ID

Process all papers before updating the log (batch the log entry).

---

## Lint Checklist (run periodically)

- Topic pages with `paper_count` that doesn't match actual papers listed
- Papers in `index.md` without a corresponding `.md` file
- Topic slugs referenced in paper frontmatter that don't have a topic page
- Papers not linked from any topic page (orphans)
- Topics not linked from any paper (orphan topics)
