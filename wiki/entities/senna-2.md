---
title: "Senna-2"
slug: senna-2
type: benchmark
paper_count: 1
last_updated: 2026-04-20
---

# Senna-2

## What It Is

Senna-2 is a driving safety benchmark and evaluation protocol for autonomous vehicle planning systems. RAD-2 builds on Senna-2's protocol and improves upon it by adding a generator-discriminator RL framework, reducing collision rate from 0.281 (Senna-2 best) to 0.250 (RAD-2).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.15308]] RAD-2 | evaluation baseline | Senna-2 is the predecessor benchmark; RAD-2 achieves lower collision rate (0.250 vs 0.281) |

## Connections

- [[entities/rad-2]] — RAD-2 directly improves upon Senna-2 by adding RL-based discriminator evaluation
- [[topics/embodied-ai]] — Both Senna-2 and RAD-2 evaluate autonomous driving agents in simulated environments
- [[topics/agent-evaluation]] — Senna-2 provides the evaluation protocol that RAD-2 builds upon