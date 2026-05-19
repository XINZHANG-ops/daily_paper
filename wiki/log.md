## [2026-05-18] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 broken links
- 0 orphan pages found (every page has >=1 inbound link)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have >=1 paper appearances
- Added evidence_count to all 9 idea pages that had evidence but no frontmatter count

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages covering the same concept
- 0 duplicate content/paragraphs within pages
- 0 factually inconsistent dates between paper frontmatter and index.md
- All 66 entities have proper type field in frontmatter
- 0 topics have type field (correct - topics don't need types)
- 0 people in entities/ (all 66 are technical)
- All paper frontmatter topic/entity references resolve to existing pages
- All entity paper_count values match actual appearances table rows

**Pass 3 — Connection Quality:**
- 0 shallow "Related:", "See also:", or bare unannotated connections
- All Connections sections use annotated [[wikilinks]] with WHY explanations
- 0 paper pairs sharing 2+ entities without direct connections
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions

**Pass 4 — Index & Log:**
- Counts verified: Papers 42 | Topics 25 | Entities: 66 | Ideas: 9
- Rebuilt index.md with accurate counts and all pages listed
- This lint entry appended to wiki/log.md

## [2026-05-17] lint | daily health check (auto)

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk
- All [[wikilinks]] valid — 0 broken links
- 0 orphan pages (all pages have >=1 inbound link)
- Topic paper_counts match Key Papers table row counts
- Entity paper_counts match Appearances table row counts
- All 9 idea pages have >=1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages
- 0 factually inconsistent dates
- 0 stale frontmatter dates
- 0 people in entities/ (all 66 are technical)

**Pass 3 — Connection Quality:**
- Found 1 paper pair sharing 2+ entities without direct connection: 2604.18168 ↔ 2604.18486 (share meanflow, flow-matching)
- **FIXED**: Added annotated cross-connection between 2604.18168 (EMF/MeanFlow image generation) and 2604.18486 (OneVL/MeanFlow VLA planning) explaining both extend MeanFlow's one-step principle to different domains
- 0 shallow "Related:" or "See also:" connections
- All topic pages have ## Evolution and ## Patterns & Insights sections
- All entity pages have substantive technical descriptions

**Pass 4 — Session Insights:**
- Chat history reveals user asked about NPO (2604.20733) and DR-Venus (2604.19859) for 2026-04-23 — papers not yet in wiki (future papers beyond current processed list)
- User recalled "sampling is optimization" idea from 2026-02-25 notes — confirmed in wiki/ideas/sampling-is-optimization.md
- User reviewed Seedance 2.0, SpatialEvo, MEDS papers in detail — connections all properly annotated
- No new gaps identified requiring wiki updates

**Totals fixed:** 1 (added missing cross-connection between 2604.18168 and 2604.18486)
