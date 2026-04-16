---
title: "Agent Systems"
slug: agent-systems
paper_count: 7
last_updated: 2026-04-16
---

# Agent Systems

## Overview

AI agent research is maturing from individual capability measurement to collective intelligence and infrastructure for reliable deployment. The papers reveal three critical challenges: (1) agents fail inconsistently across runs, (2) real-world evaluation differs dramatically from sandbox benchmarks, and (3) skills remain static after deployment with no system-wide learning.

The key theme is that **agent reliability is a systems problem, not just a capability problem**. Even frontier models achieve only 33.3% on real-world tasks (ClawBench), yet skills can evolve collectively if infrastructure supports cross-user trajectory aggregation (SkillClaw).

## Evolution

Early April 2026 saw ClawBench reveal the massive gap between sandbox benchmarks (65-75% on OSWorld) and real-world everyday tasks (33.3% for frontier models). SkillClaw proposed that skills can evolve collectively rather than remaining static—cross-user trajectories provide the signal. ClawGUI then provided the end-to-end infrastructure: scalable RL training, standardized evaluation, and deployment pathways. CodeTracer addressed debugging by identifying the evidence-to-action gap as the core failure mode in code agents.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08523]] ClawBench | 2026-04-10 | Real-world evaluation gap revelation |
| [[2604.06132]] Claw-Eval | 2026-04-08 | Trustworthy evaluation via full-trajectory auditing and three evidence channels |
| [[2604.08377]] SkillClaw | 2026-04-10 | Collective skill evolution via agentic evolver |
| [[2604.11784]] ClawGUI | 2026-04-15 | Unified training/evaluation/deployment framework |
| [[2604.11641]] CodeTracer | 2026-04-14 | Evidence-to-action gap diagnosis |

## Patterns & Insights

- **Sandbox ≠ reality**: Real-world agent performance is dramatically worse than benchmark performance
- **Skills can compound**: Collective skill evolution means learning benefits all users, not just individual
- **Evidence-to-action gap**: Agents can gather information but fail to translate it into correct actions
- **Reliability is systems-level**: Individual capability improvements don't translate to reliability without infrastructure

## Open Problems

- How to make real-world evaluation scalable and reproducible
- Bridging the gap between benchmark performance and real-world reliability
- Designing agent architectures that support continuous skill evolution

## Connections

- [[topics/agent-evaluation]] — Evaluation frameworks must measure real-world performance, not just capability
- [[topics/embodied-ai]] — Embodied agents face similar reliability challenges
- [[ideas/collective-intelligence]] — SkillClaw exemplifies how agents can learn collectively