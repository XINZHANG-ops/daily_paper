---
title: "Code Agents"
slug: code-agents
paper_count: 2
last_updated: 2026-04-21
---

# Code Agents

## Overview

Code agents use LLMs to write, debug, and reason about code. Key challenges include evidence-to-action gap, cross-file consistency, and game development as a testbed for complex code synthesis.

## Evolution

Mid-April 2026, CodeTracer revealed the evidence-to-action gap as the primary failure mode in code agents—not that models don't know the right answer, but that they fail to correctly attribute failures to their true causes. On April 21, OpenGame demonstrated that game development is an ideal testbed for code agents because: (1) it requires complex multi-file synthesis with cross-file consistency, (2) game engines like Phaser have text-based APIs amenable to LLMs, and (3) evaluation can be automated through headless browser execution. OpenGame's Game Skill approach—combining Template Skill for scaffolding and Debug Skill for cumulative error repair—shows that domain-specific infrastructure is essential for reliable code generation.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.11641]] CodeTracer | 2026-04-14 | Debugging infrastructure via evidence-to-action gap diagnosis |
| [[2604.18394]] OpenGame | 2026-04-21 | Game development as testbed for complex code synthesis with multi-file consistency |

## Patterns & Insights

- **Evidence-to-action gap is the primary failure mode**: CodeTracer shows that debugging failure isn't about wrong answers but misattribution—models know the failure happened but attribute it to wrong causes
- **Complex multi-file consistency is the real challenge**: OpenGame shows game development requires maintaining consistency across many files with cross-references—simpler than real software but tractable enough to evaluate
- **Domain-specific infrastructure enables reliability**: GameCoder-27B's Template+Debug skill pattern suggests that scaffolding + cumulative repair is essential for reliable code generation

## Connections

- [[topics/agent-systems]] — Code agents are a type of agent system
- [[topics/agent-evaluation]] — Code agent reliability needs proper evaluation