---
title: "ResAD"
slug: resad
type: algorithm
paper_count: 1
last_updated: 2026-04-20
---

# ResAD (Residual Diffusion for Autonomous Driving)

## What It Is

ResAD is a diffusion-based autonomous driving planner that serves as a baseline in the RAD-2 paper. RAD-2 achieves 56% lower collision rate (0.234 vs 0.533) compared to ResAD by adding a discriminator-based reranking mechanism on top of the diffusion generator.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.15308]] RAD-2 | baseline | ResAD is the primary baseline; RAD-2 significantly outperforms it |

## Connections

- [[entities/rad-2]] — RAD-2 builds upon ResAD by adding RL discriminator evaluation
- [[topics/embodied-ai]] — Both ResAD and RAD-2 address autonomous driving planning in simulated environments
- [[topics/reinforcement-learning]] — ResAD uses pure imitation learning; RAD-2 shows that adding RL-based evaluation improves upon this approach