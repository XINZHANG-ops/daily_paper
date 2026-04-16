---
title: "PPO"
slug: ppo
type: algorithm
paper_count: 3
last_updated: 2026-04-16
---

# PPO (Proximal Policy Optimization)

## What It Is

PPO is a policy gradient reinforcement learning algorithm that uses a clipped objective to prevent excessively large policy updates. In the April 2026 papers, PPO appears primarily in comparative analyses showing that template collapse is algorithm-agnostic (affecting PPO, DAPO, and GRPO equally), though manifesting differently in PPO's clipped objective.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06268]] | comparison | Template collapse is algorithm-agnostic (affects PPO, DAPO, GRPO) but manifests differently in PPO's clipped objective |
| [[2604.06628]] | baseline | Used in SFT generalization study as baseline RL algorithm |
| [[2604.03128]] | comparison | RLSD notes that PPO's critic-based approach is different from its self-distillation approach |

## Connections

- [[topics/reinforcement-learning]] — PPO is an established algorithm now often compared against newer methods
- [[entities/grpo]] — GRPO has largely replaced PPO for LLM training due to better efficiency
