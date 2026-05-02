---
title: "Agent Systems"
slug: agent-systems
paper_count: 9
last_updated: 2026-04-21
---

# Agent Systems

## Overview

AI agent research is maturing from individual capability measurement to collective intelligence and infrastructure for reliable deployment. The papers reveal three critical challenges: (1) agents fail inconsistently across runs, (2) real-world evaluation differs dramatically from sandbox benchmarks, and (3) skills remain static after deployment with no system-wide learning.

The key theme is that **agent reliability is a systems problem, not just a capability problem**. Even frontier models achieve only 33.3% on real-world tasks (ClawBench), yet skills can evolve collectively if infrastructure supports cross-user trajectory aggregation (SkillClaw).

## Evolution

Early April 2026 saw ClawBench reveal the massive gap between sandbox benchmarks and real-world everyday tasks. SkillClaw proposed that skills can evolve collectively rather than remaining static. ClawGUI provided end-to-end infrastructure. CodeTracer addressed debugging by identifying the evidence-to-action gap. DR3-Eval showed hallucination as the primary failure mode in deep research agents, and OccuBench revealed implicit fault handling difficulty in professional domains. On April 21, Agent-World introduced scalable real-world environment synthesis—mining 1978 environments and 19822 tools from the web—and continuous self-evolving training with diagnostic arena, demonstrating scaling laws where more environments and more evolution rounds monotonically improve agent performance.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06132]] Claw-Eval | 2026-04-08 | Trustworthy evaluation via full-trajectory auditing and three evidence channels |
| [[2604.06268]] RAGEN-2 | 2026-04-09 | Template collapse identification in agentic RL |
| [[2604.08377]] SkillClaw | 2026-04-10 | Collective skill evolution via agentic evolver |
| [[2604.08523]] ClawBench | 2026-04-10 | Real-world evaluation gap revelation |
| [[2604.11784]] ClawGUI | 2026-04-15 | Unified training/evaluation/deployment framework |
| [[2604.14683]] DR3-Eval | 2026-04-17 | Deep research agent evaluation with hallucination as primary failure mode |
| [[2604.10866]] OccuBench | 2026-04-20 | Professional domain LES simulation, implicit fault handling difficulty |
| [[2604.18292]] Agent-World | 2026-04-21 | Scaling real-world environment synthesis with 1978 environments and self-evolving training arena |
| [[2604.18394]] OpenGame | 2026-04-21 | Game development as testbed for complex code synthesis with multi-file consistency and Game Skill evolution |

## Patterns & Insights

- **Sandbox ≠ reality**: Real-world agent performance is dramatically worse than benchmark performance
- **Skills can compound**: Collective skill evolution means learning benefits all users, not just individual
- **Evidence-to-action gap**: Agents can gather information but fail to translate it into correct actions
- **Hallucination is universal**: Even frontier models hallucinate; this is not solvable by scale alone
- **Reliability is systems-level**: Individual capability improvements don't translate to reliability without infrastructure

## Open Problems

- How to make real-world evaluation scalable and reproducible
- Bridging the gap between benchmark performance and real-world reliability
- Designing agent architectures that support continuous skill evolution

## Connections

- [[topics/agent-evaluation]] — Evaluation frameworks like Claw-Eval and DR3-Eval measure what actually matters
- [[topics/embodied-ai]] — Embodied agents face similar reliability challenges
- [[ideas/collective-intelligence]] — SkillClaw exemplifies how agents can learn collectively