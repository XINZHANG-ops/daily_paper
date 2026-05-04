---
title: "ResAD"
slug: resad
type: algorithm
paper_count: 1
last_updated: 2026-04-20
---

# ResAD (Residual Diffusion for Autonomous Driving)

## What It Is

ResAD (Residual Diffusion for Autonomous Driving) is a diffusion-based motion planner that generates vehicle trajectories by iteratively denoising random paths into feasible driving plans. Trained with imitation learning on expert demonstrations, ResAD produces diverse trajectory candidates but suffers from two structural weaknesses: **stochastic instability** (different runs produce very different trajectories from the same observation) and **lack of negative feedback** (no mechanism to learn from bad outcomes, only mimic good ones).

RAD-2 addresses both weaknesses by wrapping ResAD in a generator-discriminator framework: ResAD serves as the diffusion generator producing candidate trajectories, while an RL-trained discriminator scores candidates based on long-term outcomes (collision risk, progress). RAD-2 achieves a 56% lower collision rate (0.234 vs 0.533) and dramatically higher safety scores (0.730 vs 0.418 Safety@1) compared to standalone ResAD, demonstrating that imitation learning alone is insufficient for safety-critical planning.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.15308]] RAD-2 | baseline | Pure diffusion planner; 56% higher collision rate than RAD-2 with discriminator |

## Connections

- [[entities/rad-2]] — RAD-2 wraps ResAD in a generator-discriminator framework, keeping the diffusion generator but adding RL-based evaluation; the gap (0.533 CR vs 0.234 CR) quantifies the value of outcome-based feedback
- [[topics/embodied-ai]] — Autonomous driving is a canonical embodied AI task; ResAD's stability issues illustrate why pure imitation learning is insufficient for safety-critical physical domains
- [[topics/reinforcement-learning]] — The ResAD→RAD-2 trajectory shows a generalizable pattern: imitation learning for generation + RL for evaluation, applicable to other high-dimensional action spaces