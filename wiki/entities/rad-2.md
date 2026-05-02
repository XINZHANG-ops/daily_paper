---
title: "RAD-2"
slug: rad-2
type: algorithm
paper_count: 1
last_updated: 2026-04-20
---

# RAD-2 (Reinforcement Learning in Agent-Discriminator Framework)

## What It Is

RAD-2 is a generator-discriminator RL framework for scaling reinforcement learning in motion planning. It addresses the instability of diffusion-based motion planners trained purely with imitation learning by adding an RL-trained discriminator that reranks trajectory candidates based on long-term outcomes. Key innovations include TC-GRPO (Temporally Consistent GRPO) for credit assignment and BEV-Warp for efficient simulation.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.15308]] | core method | RAD-2 is the paper's primary contribution; achieves 56% collision rate reduction over ResAD |

## Connections

- [[entities/tc-grpo]] — TC-GRPO is the credit assignment algorithm used in RAD-2's discriminator training
- [[entities/beV-warp]] — BEV-Warp is the simulation environment used for scalable RL training
- [[entities/senna-2]] — Senna-2 is the evaluation benchmark that RAD-2 improves upon
- [[topics/reinforcement-learning]] — RAD-2 demonstrates that decoupling high-dimensional output from low-dimensional reward stabilizes RL optimization
- [[topics/embodied-ai]] — RAD-2's application domain is autonomous driving in simulated 3D environments