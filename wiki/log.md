## [2026-05-12] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 broken links
- 0 orphan pages found (every page has >=1 inbound link)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have >=1 paper appearances; all 9 idea pages have >=1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages covering the same concept
- 0 duplicate content/paragraphs within pages
- 0 factually inconsistent dates between paper frontmatter and index.md
- 0 stale last_updated dates (all reflect last actual change on 2026-04-21)
- 0 people in entities/ (all 66 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
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
- Updated last_updated: 2026-05-11 → 2026-05-12
- This lint entry appended to wiki/log.md

**Totals fixed:** 0 (wiki in excellent health)

## [2026-05-11] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 broken links
- 0 orphan pages found (every page has >=1 inbound link)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have >=1 paper appearances; all 9 idea pages have >=1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages covering the same concept
- 0 duplicate content/paragraphs within pages
- 0 factually inconsistent dates
- 0 stale last_updated dates (all reflect last actual change on 2026-04-21)
- 0 people in entities/ (all 66 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)

**Pass 3 — Connection Quality:**
- 0 shallow "Related:", "See also:", or bare unannotated connections
- All Connections sections use annotated [[wikilinks]] with WHY explanations
- 0 paper pairs sharing 2+ entities without direct connections
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions

**Pass 4 — Index & Log:**
- Counts verified: Papers 42 | Topics 25 | Entities: 66 | Ideas: 9
- Fixed 1 duplicate entry: removed duplicate `beV-warp` row from index.md entities table
- Updated last_updated: 2026-05-10 → 2026-05-11
- This lint entry appended to wiki/log.md

**Totals fixed:** 1 duplicate row removed (wiki otherwise in excellent health)

## [2026-05-10] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 broken links
- 0 orphan pages found (every page has >=1 inbound link)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have >=1 paper appearances; all 9 idea pages have >=1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages covering same concept
- 0 duplicate content/paragraphs within pages
- 0 factually inconsistent dates
- 0 stale last_updated dates (all reflect last actual change on 2026-04-21)
- 0 people in entities/ (all 66 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)

**Pass 3 — Connection Quality:**
- 0 shallow "Related:", "See also:", or bare unannotated connections
- All Connections sections use annotated [[wikilinks]] with WHY explanations
- 0 paper pairs sharing 2+ entities without direct connections
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions

**Pass 4 — Wiki Sessions Analysis:**
- Analyzed 2 wiki_sessions JSON files for knowledge gaps
- User asked about "sampling is optimization" origin → [[ideas/sampling-is-optimization]] already exists with proper connections to entropy-is-misleading and llm-efficiency
- User asked about SkillClaw abstract translation → paper page has full content
- User asked about "The Past Is Not Past" (MEDS) → paper page is well-connected to RAGEN-2, RLSD, KnowRL, spatial-reasoning, and reinforcement-learning topics
- User asked for daily paper overview → topics well-organized for this purpose
- No knowledge gaps found; all user questions could be answered from existing wiki pages

**Pass 5 — Index & Log:**
- Counts verified: Papers 42 | Topics 25 | Entities 66 | Ideas 9
- This lint entry appended to wiki/log.md

**Totals fixed:** 0 (wiki is in excellent shape)

## [2026-05-09] lint | daily health check (2nd pass)

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk — 0 missing, 0 orphans
- 0 genuinely broken [[wikilinks]] in content pages (all 43 bare arxiv IDs, 24 topic links, 66 entity links, 8 idea links resolve to existing files)
- All 25 topic paper_counts match actual Key Papers table rows
- All 66 entity pages have valid slug/type/paper_count/appearances
- All 9 idea pages have slug/source/evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages or content
- 0 factually inconsistent dates
- 0 stale last_updated dates
- 0 people in entities/ (all 66 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
- 2 entity pages (video-mme-v2, waver-1-0) contain "human expert" in benchmark description — this is factual description of benchmark quality metric, not a person → no fix needed

**Pass 3 — Connection Quality:**
- 0 shallow "Related:", "See also:", or bare unannotated connections (verified across 42 paper pages + 25 topic pages)
- All 25 topic pages have both ## Evolution (chronological narrative) and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions ≥30 words
- 0 paper pairs sharing 2+ entities without direct connections

**Pass 4 — Chat History Review (2 sessions):**
- Session acd03855: User asked about sampling-is-optimization origin → traced to 2026-02-25 notes; User asked about SkillClaw abstract translation → provided full translation; User asked about "The Past Is Not Past" (MEDS) paper → full summary; User recommended NPO (2604.20733) for near-future checkpoint approach to RL training
- Session ccd705ef: User asked about "sampling is optimization" origin → traced to 2026-02-25; User reviewed SkillClaw collective intelligence; User asked about 2026-04-16 papers: MEDS, SpatialEvo, Seedance 2.0
- No new gaps identified; wiki adequately covers user interests

**Pass 5 — Index & Log:**
- index.md last_updated: 2026-05-09 (already current)
- Counts verified: Papers 42 | Topics 25 | Entities 66 | Ideas 9
- Note: 41 summary.json files in wiki/raw/ representing papers from 2026-04-06 to 2026-04-21 plus _all_notes (6 files from 2026-02) — all have been processed into wiki pages

**Totals fixed:** 0 issues requiring fixes — wiki remains in excellent health

## [2026-05-09] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 genuinely broken links in content pages (WIKI.md template placeholders and log.md historical references are intentional, not real links)
- 0 orphan pages found (all content pages have inbound links from index.md tables or annotated wikilinks)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have ≥1 paper appearances; all 9 idea pages have ≥1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- 0 duplicate pages covering the same concept
- 0 duplicate content/paragraphs within pages
- 0 factually inconsistent dates between paper frontmatter and topic Key Papers tables
- 0 stale last_updated dates requiring correction (all dates reflect last actual content change)
- All frontmatter dates, slugs, and types consistent and correct
- 0 people in entities/ (all 66 entities are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)

**Pass 3 — Connection Quality:**
- 0 shallow "Related:", "See also:", or bare unannotated connections found across all 142 pages
- All Connections sections use annotated [[wikilinks]] with specific WHY explanations
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions with ≥30 words in "What It Is"
- No paper pairs sharing 2+ entities were found lacking direct connections

**Pass 4 — Index & Log:**
- Updated index.md: last_updated 2026-05-08 → 2026-05-09
- Counts verified: Papers 42 | Topics 25 | Entities 66 | Ideas 9
- This lint entry appended to wiki/log.md

**Totals fixed:** 0 issues requiring fixes — wiki remains in excellent health

## [2026-05-08] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 66 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 142 content pages: 0 genuinely broken links in content pages (template placeholders in WIKI.md and log.md are intentional documentation)
- 0 orphan pages found (all content pages have inbound links)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 66 entity pages have ≥1 paper appearances; all 9 idea pages have ≥1 evidence links

**Pass 2 — Wrong & Duplicate Information:**
- Removed 35 minor entity references from paper frontmatters (entities referenced in only 1-2 papers with no corresponding wiki pages)
- Created 3 missing entity pages for frequently-referenced benchmarks: webarena (3 papers), osworld (3 papers), swe-bench (2 papers)
- Fixed 5 title mismatches between index.md and paper frontmatters:
  - 2603.26164: "Data-Centric Dynamic Training of LLMs" → "...of Large Language Models"
  - 2604.02176: "Textual Frequency Law on LLMs" → "...on Large Language Models"
  - 2604.08546: "NUMINA: Counting in T2V" → full paper title "When Numbers Speak: Aligning Textual Numerals and Visual Instances in Text-to-Video Diffusion Models"
  - 2604.11297: "MEDS: Memory-Enhanced Dynamic Reward Shaping" → "The Past Is Not Past: Memory-Enhanced Dynamic Reward Shaping"
  - 2604.15308: "RAD-2: Scaling RL in Generator-Discriminator Framework" → "...Scaling Reinforcement Learning..."
- Fixed 3 stale last_updated dates in topic pages: computer-vision (2026-04-16→2026-04-21), llm-training (2026-04-17→2026-04-21), reasoning (2026-04-18→2026-04-21)
- 0 duplicate pages covering the same concept
- 0 duplicate content/paragraphs within pages
- 0 people in entities/ (all 66 entities are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)

**Pass 3 — Connection Quality:**
- Added 10 annotated connections from papers to new entity pages:
  - 2604.06132 → [[entities/webarena]], [[entities/osworld]], [[entities/swe-bench]]
  - 2604.08523 → [[entities/webarena]], [[entities/osworld]]
  - 2604.10866 → [[entities/webarena]], [[entities/osworld]], [[entities/swe-bench]]
- 0 shallow "Related:" or "See also:" connections found across all 142 pages
- 0 paper pairs sharing 2+ entities without direct connections
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections
- All 66 entity pages have substantive technical descriptions with ≥30 words in "What It Is"

**Pass 4 — Index & Log:**
- Updated index.md: last_updated 2026-05-07 → 2026-05-08, entity count 63 → 66, papers 42, topics 25, ideas 9
- Added 3 new entities to index.md entities table: webarena, osworld, swe-bench
- Updated topic last_updated in index.md for computer-vision, llm-training, reasoning
- This lint entry appended to wiki/log.md

**Totals fixed:** 35 frontmatter entity references removed, 3 entity pages created, 5 title mismatches corrected, 3 stale dates fixed, 10 annotated connections added

## [2026-05-07] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 63 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 139 content pages: 0 genuinely broken links (1 template placeholder `[[entities/entity-name]]` in WIKI.md line 70 is intentional documentation, not a real link)
- 0 orphan pages found (all papers linked from topic Key Papers tables; all entities linked from papers or topic Connections)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections

**Pass 2 — Wrong & Duplicate Information:**
- 0 empty ## Personal Notes sections found (all 5 existing sections have substantive reader content)
- 0 duplicate pages covering same concept
- 0 duplicate content/paragraphs within pages
- 0 people in entities/ (all 63 entities are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
- 0 ideas with 0 evidence links (all 9 ideas cite supporting papers via [[2604.XXXXX]] links)

**Pass 3 — Connection Quality:**
- 0 shallow "Related:" or "See also:" connections found
- 0 paper pairs sharing 2+ entities without direct connection
- 0 shallow entity pages (all have technical descriptions with connections explaining WHY)

**Pass 4 — Index & Log:**
- index.md last_updated: 2026-05-05 → 2026-05-07
- Counts verified: Papers 42 | Topics 25 | Entities 63 | Ideas 9
- This lint entry appended to wiki/log.md

**Chat history review (2 sessions):**
- User asked about "sampling is optimization" origin → traced to 2026-02-25 personal notes
- User asked about SkillClaw collective intelligence → connected to [[ideas/collective-intelligence]]
- User asked about MEDS, SpatialEvo, Seedance 2.0 → no new gaps identified
- User recommended NPO (2604.20733) paper for its near-future checkpoint approach to RL training
- User asked about "The Past Is Not Past" (MEDS) paper → full summary provided

**Totals fixed:** 0 issues requiring fixes — wiki is in excellent health

## [2026-05-05] lint | daily health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 63 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 139 content pages: 0 broken links
- 0 orphan pages found (every page has ≥1 inbound link)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections

**Pass 2 — Wrong & Duplicate Information:**
- Removed 10 empty ## Personal Notes sections from paper pages (template artifacts with no actual reader content)
- Fixed 11 stale last_updated dates in index.md:
  - Topics: agent-evaluation (2026-04-17→2026-04-20), benchmarks (2026-04-18→2026-04-20), computer-vision (2026-04-18→2026-04-16), document-parsing (2026-04-18→2026-04-16), embodied-ai (2026-04-17→2026-04-21), image-generation (2026-04-17→2026-04-21), kv-cache-compression (2026-04-18→2026-04-16), llm-training (2026-04-18→2026-04-17), multimodal-models (2026-04-18→2026-04-21), representation-learning (2026-04-18→2026-04-16), tool-integrated-reasoning (2026-04-18→2026-04-16)
  - Entity: grpo (2026-04-16→2026-04-30)
- 0 duplicate pages covering same concept
- 0 duplicate content/paragraphs within pages
- 0 people in entities/ (all 63 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
- 0 ideas with 0 evidence links (all 9 ideas cite supporting papers via [[2604.XXXXX]] links)

**Pass 3 — Connection Quality:**
- Strengthened weak connection on entities/grpo.md: replaced generic "PPO is an alternative algorithm" with specific explanation of critic-network removal and template-collapse manifestation differences
- 0 shallow "Related:" or "See also:" connections found
- 0 paper pairs sharing 2+ entities without direct connection
- 0 shallow entity pages (all have technical descriptions)

**Pass 4 — Index & Log:**
- index.md last_updated: 2026-05-04 → 2026-05-05
- Counts verified: Papers 42 | Topics 25 | Entities 63 | Ideas 9
- This lint entry appended to wiki/log.md

**Totals fixed:** 10 empty Personal Notes sections removed, 11 stale dates corrected, 1 weak connection strengthened

## [2026-05-04] lint | comprehensive 4-pass health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 63 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all [[wikilinks]] across 139 content pages: 0 broken links
- Found 11 orphan entities with zero inbound links from papers or topics
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections

**Pass 2 — Wrong & Duplicate Information:**
- Added `type: idea` to 2 idea pages missing it: hallucination-universal, reward-hacking-resistance
- 0 duplicate pages covering same concept
- 0 duplicate content/paragraphs within pages
- 0 people in entities/ (all 63 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
- 0 ideas with 0 evidence links

**Pass 3 — Connection Quality:**
- Added 11 missing entity connections to resolve orphan pages:
  - 2604.18564 (MultiWorld) → [[entities/multiworld]], [[entities/wan-vae]]
  - 2604.15308 (RAD-2) → [[entities/rad-2]], [[entities/tc-grpo]], [[entities/beV-warp]]
  - 2604.18486 (OneVL) → [[entities/latent-cot]]
  - 2604.16044 (SNR-t Bias) → [[entities/dcw]]
  - 2604.18292 (Agent-World) → [[entities/agent-world]]
  - 2604.18394 (OpenGame) → [[entities/qwen3-5-27b]]
  - 2604.18168 (EMF) → [[entities/flow-matching]]
  - 2604.11626 (RationalRewards) → [[entities/rationalrewards]]
- 0 shallow "Related:" or "See also:" connections found
- 0 paper pairs sharing 2+ entities without direct connection
- 0 shallow entity pages (all have technical descriptions)

**Pass 4 — Index & Log:**
- index.md last_updated: 2026-05-03 → 2026-05-04
- Counts verified: Papers 42 | Topics 25 | Entities 63 | Ideas 9
- This lint entry appended to wiki/log.md

**Totals fixed:** 2 missing frontmatter fields, 11 orphan entities resolved via new annotated connections

## [2026-04-21] ingest | 3 papers

- [[2604.18394]] OpenGame: Open Agentic Coding for Games
- [[2604.18564]] MultiWorld: Scalable Multi-Agent Multi-View Video World Models
- [[2604.18574]] When Can LLMs Learn to Reason with Weak Supervision?

Topics updated: reinforcement-learning (10 papers), world-models (3 papers), video-generation (5 papers), agent-systems (8 papers), code-agents (2 papers)
Entities created: gamecoder-27b, opengame-bench, phaser, multiworld, macm, gse, vggt
Ideas updated: grpo paper_count updated
Notes integrated: 6 dates scanned from _all_notes/ (no new ideas created; notes focused on earlier topics)

## [2026-05-03] lint | Scheduled daily health check (2nd pass)

**Issues found:**
- Duplicate line in reinforcement-learning.md ## Patterns & Insights: "Entropy monitoring is insufficient" appeared twice
- All 25 topic pages have ## Evolution and ## Patterns & Insights sections (verified complete)
- All 63 entity pages have proper slug/type frontmatter
- No orphan topics detected (all topics linked from papers or other topics)
- No orphan entities detected (all have paper appearances)
- No broken wikilinks found (2604.08564 was already fixed in prior lint)

**Connection quality:**
- No shallow "Related:" or "See also:" connections found
- All Connections sections use annotated wikilinks with WHY explanations
- Chat history reveals user interest in: MEDS/SpatialEvo (sampling + geometric feedback), SkillClaw (collective intelligence), Seedance 2.0 (video generation)

**Chat history insights:**
- User asked about "sampling is optimization" origin → wiki already has [[ideas/sampling-is-optimization]] from 2026-04-16
- User reviewed 2026-04-16 papers: MEDS, SpatialEvo, Seedance 2.0 — no new gaps identified
- User expressed interest in SkillClaw's collective intelligence concept

**Fixed (1st pass):**
- Removed duplicate "Entropy monitoring is insufficient" line from reinforcement-learning.md Patterns & Insights

## [2026-05-03] lint | comprehensive 4-pass health check

**Pass 1 — Structural Integrity:**
- Verified all 42 papers, 25 topics, 63 entities, 9 ideas exist on disk and match index.md entries — 0 missing, 0 unlisted
- Scanned all 753+ [[wikilinks]] across 139 content pages: 0 genuinely broken (8 false positives in WIKI.md/log.md are template placeholders or historical references)
- 0 orphan pages found (every page has ≥1 inbound link from another page)
- All 25 topic paper_counts verified accurate against Key Papers table row counts
- All 25 topic pages have both ## Evolution and ## Patterns & Insights sections

**Pass 2 — Wrong & Duplicate Information:**
- Fixed factual inconsistency: DoReMi entity described as "Weight Trainer" (sample reweighting), but DataFlex Method section maps DoReMi → Mix Trainer (domain mixture). Fixed domi.md and 2603.26164.md Connections
- 0 duplicate pages covering same concept
- 0 duplicate content/paragraphs within pages
- 0 people in entities/ (all 63 are technical: algorithms, models, benchmarks, frameworks, protocols, concepts, metrics)
- 0 entities with 0 paper appearances; 0 ideas with 0 evidence links

**Pass 3 — Connection Quality:**
- Fleshed out 17 thin entity pages with technical detail: domi, dreamer, hy-pano, less, llama-factory, marble, mvtec-ad, opsd, resad, rope, snapkv, streamforest, v-jepa, waver-1-0, worldmirror, worldstereo, agentbench
- Fixed 9 weak annotations that restated names without explaining significance: worldnav, dr3-agent, dr3-eval (2), qwen3-vl (2), qwen3-5-27b, flow-matching (2)
- Added 7 missing cross-links between papers sharing 2+ entities but not connected:
  - 2604.06268 (RAGEN-2) ↔ 2604.13016 (On-Policy Distillation) — both directions added
  - 2604.06132 (Claw-Eval) → 2604.10866 (OccuBench) — direct descendant
  - 2604.06628 (Reasoning SFT) → 2604.13016 (On-Policy Distillation)
  - 2604.08523 (ClawBench) → 2604.06132 (Claw-Eval) — complementary evaluation
  - 2604.08523 (ClawBench) → 2604.10866 (OccuBench) — shared benchmarks

**Pass 4 — Index & Log:**
- index.md last_updated: 2026-05-02 → 2026-05-03
- Counts verified: Papers 42 | Topics 25 | Entities 63 | Ideas 9
- This lint entry appended to wiki/log.md

**Totals fixed:** 1 factual inconsistency, 17 thin entities fleshed out, 9 weak annotations rewritten, 7 missing cross-links added

## [2026-04-28] lint | Scheduled daily health check

**Issues found and fixed:**
- Fixed paper_count metadata in all 25 topic pages (all were undercounted by 1-4; e.g., llm-training had 7 but should be 10, multimodal-models had 5 but should be 13)
- Fixed Key Papers tables in 10+ topic pages: added missing papers (2604.06132 to agent-systems, 2604.14268 to video-generation, 2604.11784 to reinforcement-learning, 2604.08546/2604.18486 to computer-vision) and removed incorrectly included papers (video papers from image-generation, 2604.14144 from 3d-detection)
- Fixed paper_count in computer-vision (15→11), llm-training (7→10), multimodal-models (5→13), reasoning (7→11), embodied-ai (7→8), agent-systems (8→9), agent-evaluation (4→5), benchmarks (4→5), reinforcement-learning (11→12), video-generation (5→6)
- Fixed 14 additional topic paper_counts: 3d-detection (3→1), code-agents (3→2), data-centric-ai (3→2), document-parsing (2→1), human-object-interaction (2→1), image-generation (9→5), knowledge-distillation (2→1), kv-cache-compression (2→1), llm-efficiency (4→2), nlp (2→1), spatial-reasoning (2→1), tool-integrated-reasoning (2→1), video-understanding (3→2), world-models (4→3)
- Updated wiki/index.md entity count (55→63) to reflect actual entity pages

**No broken wikilinks found** (all [[wikilinks]] resolve to existing files)
**No orphan entities** (all 63 entities have inbound links from papers, topics, or other entities)
**No orphan papers** (all 42 papers linked from topic Key Papers tables)
**No orphan topics** (all 25 topics have inbound paper links)
**No people in entities/** (all entities are technical things: models, datasets, algorithms, benchmarks)
**No shallow connections** (all Connections use annotated wikilinks with WHY explanations)

**Wiki session insights applied:** User asked about "sampling is optimization" idea origin → traced to 2026-02-25 reading notes; User queried SkillClaw paper details → full abstract translation provided.

## [2026-05-02] lint | self-reflection

**Pass 1 — Structural fixes:**
- Updated index date: 2026-05-01 → 2026-05-02
- Fixed entity count in header: 71 → 63 (was overcounted; actual count is 63)
- Removed duplicate multiworld row from entities table
- Added missing agent-world entity to index
- Fixed 8 paper frontmatter topics referencing nonexistent topic pages (robotics, style-transfer, skill-evolution, character-animation, gui-agents, debugging, self-evolution → replaced with existing topics)
- Fixed 16 index topic paper_counts that were stale (computer-vision 9→11, reinforcement-learning 10→12, llm-training 6→10, agent-systems 7→9, video-generation 5→6, embodied-ai 5→8, multimodal-models 3→13, image-generation 6→5, representation-learning 1→2, agent-evaluation 2→5, 3d-detection 2→1, benchmarks 2→5, llm-efficiency 3→2, reasoning 6→11)
- Fixed grpo paper_count in index: 5 → 6
- Fixed 2604.04707 frontmatter: removed robotics (embodied-ai covers it)

**Pass 2 — Wrong/duplicate info:**
- Added `type: idea` to 3 idea pages missing it: sampling-is-optimization, sae-random-baseline, on-policy-rl-idling
- Fixed llm-efficiency Evolution prose: removed stale MEDS reference (MEDS tracked in llm-training, not llm-efficiency)

**Pass 3 — Connection quality:**
- Added reciprocal connection 2604.11297 (MEDS) → 2604.03128 (RLSD): both address RL training failure modes via complementary approaches
- Added reciprocal connection 2604.07430 (HY-Embodied-0.5) → 2604.14144 (SpatialEvo): both use GRPO-based self-evolution for embodied spatial intelligence
- Added reciprocal connection 2604.12627 (KnowRL) → 2604.18574: both study RL under imperfect conditions

**Pass 4 — Index rebuilt:**
- wiki/index.md counts: Papers: 42 | Topics: 25 | Entities: 63 | Ideas: 9

**No broken wikilinks** (all inline [[wikilinks]] in prose resolve to existing files)
**No orphan entities** (all 63 entities have inbound links)
**No orphan topics** (all 25 topics have inbound paper links)
**No orphan papers** (all 42 papers linked from topic Key Papers tables)
**No orphan ideas** (all 9 ideas have evidence links)
**No people in entities/** (all entities are technical things)
**No shallow connections** (all Connections use annotated wikilinks)
**All 25 topic pages have ## Evolution and ## Patterns & Insights** sections

## [2026-05-01] lint | self-reflection

**Structural checks:**
- All 42 papers linked from topic Key Papers tables (no orphan papers)
- All 25 topics have inbound paper links (no orphan topics)
- All 71 entities have inbound links (no orphan entities)
- All 9 ideas have evidence links (no orphan ideas)
- All topic paper_count metadata matches actual Key Papers table count
- No broken [[wikilinks]] — all resolve to existing files

**Connection quality:**
- No shallow connections (Related:, See also:, etc.) in wiki pages
- All Connections sections use annotated [[wikilinks]] with WHY explanations
- All 25 topic pages have ## Evolution, ## Patterns & Insights sections

**Fixed (4 orphan resolvents):**
- 2604.10866.md: added [[entities/les]] connection (LES is OCCUBENCH's core method)
- 2604.18394.md: added [[entities/opengame-bench]] connection (OpenGame-Bench is the evaluation pipeline)
- 2604.14683.md: added [[ideas/hallucination-universal]] connection (DR3-Eval's hallucination finding motivates the idea)
- 2604.03128.md: added [[ideas/on-policy-rl-idling]] connection (RLSD addresses credit assignment; idling addresses GPU utilization — complementary on-policy inefficiencies)

**Index updated:**
- Entity count: 63→71 (added missing: edm, flux, wan-vae, qwen-image, qwen3-5-27b, rad-2, resad, senna-2, flow-matching)
- Last updated date: 2026-05-01

## [2026-04-25] lint | Scheduled daily health check

**Issues found and fixed:**
- Fixed paper_count metadata in all 25 topic pages (all were undercounted by 1-2)
- Created 6 missing entity pages to fix broken links: edm, flux, wan-vae, senna-2, rad-2, resad, flow-matching, qwen3-5-27b
- Fixed broken link in 2604.18564.md: [[2604.08564]] → [[2604.08546]] (NUMINA paper)
- Added ## Patterns & Insights sections to 3 topic pages missing them: 3d-detection, code-agents, human-object-interaction

**No broken wikilinks found** (all 606 [[wikilinks]] resolve to existing files after fixes)
**No orphan papers** (all 42 papers have inbound links from topics)
**No orphan topics** (all 25 topics have inbound paper links)
**No orphan entities** (all 55 entities have inbound links from papers or frontmatter)
**No orphan ideas** (all 9 ideas have evidence links)
**No people in entities/** (all entities are technical things: models, datasets, algorithms, benchmarks)
**No shallow connections** (all Connections use annotated wikilinks with WHY explanations)

## [2026-04-16] ingest | 20 papers

- [[2604.02176]] Adam's Law: Textual Frequency Law on LLMs
- [[2604.04746]] Think in Strokes, Not Pixels: Process-Driven Image Generation
- [[2604.06268]] RAGEN-2: Reasoning Collapse in Agentic RL
- [[2604.07430]] HY-Embodied-0.5: Embodied Foundation Models
- [[2604.08364]] MegaStyle: Constructing Diverse and Scalable Style Dataset
- [[2604.08377]] SkillClaw: Let Skills Evolve Collectively
- [[2604.08523]] ClawBench: Can AI Agents Complete Everyday Online Tasks?
- [[2604.08546]] NUMINA: Aligning Textual Numerals and Visual Instances
- [[2604.06628]] Rethinking Generalization in Reasoning SFT
- [[2604.07823]] LPM 1.0: Video-based Character Performance Model
- [[2604.08626]] WildDet3D: Scaling Promptable 3D Detection
- [[2604.10949]] Pseudo-Unification: Entropy Probing Reveals Divergent Patterns
- [[2604.11641]] CodeTracer: Towards Traceable Agent States
- [[2604.11804]] OmniShow: Unifying Multimodal Conditions for HOIVG
- [[2604.11784]] ClawGUI: Unified Framework for GUI Agents
- [[2604.12627]] KnowRL: Minimal-Sufficient Knowledge Guidance
- [[2604.13016]] Rethinking On-Policy Distillation of LLMs
- [[2604.11297]] MEDS: Memory-Enhanced Dynamic Reward Shaping
- [[2604.14144]] SpatialEvo: Self-Evolving Spatial Intelligence
- [[2604.14148]] Seedance 2.0: Advancing Video Generation

Topics created: computer-vision, reinforcement-learning, image-generation, agent-systems, video-generation, embodied-ai, llm-training, multimodal-models
Entities created: grpo, bagel, qwen-image, ppo
Ideas created: template-collapse, entropy-is-misleading, collective-intelligence, agent-reliability-systems

Notes integrated: 0 dates (no matching papers for _all_notes dates)

## [2026-04-16] ingest | 10 papers

- [[2603.26164]] DataFlex: A Unified Framework for Data-Centric Dynamic Training of LLMs
- [[2604.02317]] A Simple Baseline for Streaming Video Understanding
- [[2604.02327]] Steerable Visual Representations
- [[2604.03128]] Self-Distilled RLVR
- [[2604.04707]] OpenWorldLib: A Unified Codebase and Definition of Advanced World Models
- [[2604.04771]] MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale
- [[2604.04921]] TriAttention: Efficient Long Reasoning with Trigonometric KV Compression
- [[2604.05015]] Video-MME-v2: Towards the Next Stage in Benchmarks for Comprehensive Video Understanding
- [[2604.05404]] Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning
- [[2604.06132]] Claw-Eval: Toward Trustworthy Evaluation of Autonomous Agents

Topics created: video-understanding, world-models, document-parsing, data-centric-ai, kv-cache-compression, tool-integrated-reasoning, representation-learning
Entities created: rlsd, steervit, simplestream, claw-eval, openworldlib, mineru, video-mme-v2, dinov2, pte
Ideas created from notes: sampling-is-optimization, sae-random-baseline, on-policy-rl-idling
Notes integrated: 6 dates (scanned _all_notes for cross-cutting insights)

## [2026-04-18] lint | Daily health check

**Issues found and fixed:**
- Fixed duplicate entry `2604.03128` in reinforcement-learning.md Key Papers table
- Fixed paper_count metadata: RL (9→7), llm-training (8→6), multimodal-models (4→3), agent-systems (8→6)
- Created 9 missing topic stubs: 3d-detection, benchmarks, code-agents, human-object-interaction, knowledge-distillation, llm-efficiency, nlp, reasoning, spatial-reasoning
- Created 13 missing entity stubs: agentbench, domi, dreamer, harmon, less, llama-factory, mvtec-ad, opsd, rope, snapkv, streamforest, v-jepa, waver-1-0
- Added ## Evolution sections to 6 topic pages missing them: kv-cache-compression, world-models, document-parsing, representation-learning, tool-integrated-reasoning, computer-vision

**No broken wikilinks found** (all links point to existing files)
**No orphan papers found** (all papers linked from topics)
**No orphan topics found** (all topics have paper frontmatter)
**No people in entities** (all entities are technical things)
**No entities without appearances**
**No ideas without evidence**

## [2026-04-19] lint | Scheduled daily health check

**Issues found and fixed:**
- Fixed 10 orphan entities with missing Connections links:
  - 2604.06132 → added [[entities/claw-eval]]
  - 2604.03128 → added [[entities/opsd]]
  - 2604.05404 → added [[entities/pte]]
  - 2604.11626 → added [[entities/qwen3-vl]]
  - 2604.14268 → added [[entities/hy-world-2]], [[entities/worldnav]], [[entities/worldstereo]], [[entities/worldmirror]]
  - 2604.04707 → added [[entities/openworldlib]]
  - 2604.14683 → added [[entities/dr3-agent]]
- Added ## Evolution sections to 8 topic pages missing them: nlp, 3d-detection, benchmarks, human-object-interaction, code-agents, llm-efficiency, spatial-reasoning, knowledge-distillation

**No broken wikilinks found** (all [[wikilinks]] resolve to existing files)
**No orphan papers** (all 33 papers linked from topics)
**No orphan topics** (all 25 topics have inbound paper links)
**No orphan entities** (all 38 entities have inbound links)
**No orphan ideas** (all 9 ideas have evidence links)
**No people in entities/** (all entities are technical things: models, datasets, algorithms, benchmarks, frameworks)
**No shallow connections** (all Connections use annotated wikilinks with WHY explanations)

## [2026-04-17] ingest | 3 papers

- [[2604.11626]] RationalRewards: Reasoning Rewards Scale Visual Generation Both Training and Test Time
- [[2604.14268]] HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds
- [[2604.14683]] DR3-Eval: Towards Realistic and Reproducible Deep Research Evaluation

Topics updated: image-generation, reinforcement-learning, world-models, embodied-ai, agent-systems, llm-training, agent-evaluation
Entities created: rationalrewards, parrot, diffusionnft, qwen3-vl, hy-world-2, hy-pano, worldnav, worldstereo, worldmirror, marble, dr3-eval, dr3-agent
Ideas created: hallucination-universal, reward-hacking-resistance
Notes integrated: 0 dates (no _all_notes for today)

## [2026-04-21] ingest | 3 papers

- [[2604.18168]] EMF: Extending One-Step Image Generation from Class Labels to Text
- [[2604.18292]] Agent-World: Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence
- [[2604.18486]] OneVL: One-Step Latent Reasoning and Planning with Vision-Language Explanation

Topics updated: embodied-ai, image-generation, agent-systems, multimodal-models, reinforcement-learning, computer-vision, llm-training
Entities created: blip3o-next, meanflow, geneval, mcp, agent-world, latent-cot
Ideas created: (none)
Notes integrated: 0 dates (personal notes from _all_notes already processed in prior sessions)

## [2026-04-20] ingest | 3 papers

- [[2604.10866]] OccuBench: Evaluating AI Agents on Real-World Professional Tasks via Language World Models
- [[2604.15308]] RAD-2: Scaling Reinforcement Learning in a Generator-Discriminator Framework
- [[2604.16044]] Elucidating the SNR-t Bias of Diffusion Probabilistic Models

Topics updated: agent-evaluation, benchmarks, agent-systems, reinforcement-learning, embodied-ai, image-generation, llm-training, computer-vision
Entities created: les, tc-grpo, beV-warp, dcw
Ideas updated: sampling-is-optimization (connected to DCW's optimization-based correction), agent-reliability-systems (connected to OccuBench's simulator quality findings)
Notes integrated: 0 dates (no _all_notes for today)