---
title: "Temporally Consistent Group Relative Policy Optimization (TC-GRPO)"
slug: tc-grpo
type: algorithm
paper_count: 1
last_updated: 2026-04-20
---

# TC-GRPO (Temporally Consistent Group Relative Policy Optimization)

## What It Is

TC-GRPO is a reinforcement learning algorithm introduced in RAD-2 (2604.15308) that exploits temporal coherence to alleviate the credit assignment problem in high-dimensional continuous action spaces like motion planning. It is used to train the discriminator in RAD-2's generator-discriminator framework for autonomous driving.

## Core Motivation

Standard RL algorithms struggle with credit assignment in continuous action spaces because sparse scalar rewards fail to distinguish which specific variations within a sampled group contribute to superior outcomes. TC-GRPO addresses this by enforcing temporal dependencies across consecutive decision steps, ensuring that candidate trajectories are evaluated within a persistent behavioral context.

## Method Details

**Temporally Consistent Rollout**:
- Uses latched execution strategy: once an optimal trajectory is selected, it is reused over a fixed horizon H_reuse for behavioral coherence
- For each relative offset h in {0, ..., H_reuse - 1}, the corresponding control command is executed sequentially
- This stabilizes the exploratory direction, ensuring cumulative reward more accurately reflects the quality of the selected trajectory

**Group-Relative Advantage Computation**:
- For rollout O_i with sequence-level reward r_i, the standardized advantage is computed relative to a group {O_i}_G_{i=1} generated from the same initial state:
- `A_i = (r_i - mean({r_1, ..., r_G})) / std({r_1, ..., r_G})`
- Group size of 4 was found optimal in ablation experiments

**Clipped Objective with Adaptive Entropy Regularization**:
- `L_{i,t∈K_i} = min(ρ_{i,t} A_i, clip(ρ_{i,t}, 1-ε, 1+ε) A_i)`
- Where ρ_{i,t} = D_φ(τ*_{i,t}|o_{i,t}) / D_φ_old(τ*_{i,t}|o_{i,t}) is the importance sampling ratio
- Adaptive entropy regularization prevents premature convergence and sigmoid saturation

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.15308]] | credit assignment method | Trains discriminator in RAD-2's generator-discriminator framework |

## Connections

- [[entities/beV-warp]] — BEV-Warp provides the simulation environment that generates rollout data for TC-GRPO training
- [[entities/ppo]] — TC-GRPO is a variant of PPO adapted for temporally structured trajectory evaluation
- [[topics/reinforcement-learning]] — TC-GRPO addresses the credit assignment problem specific to high-dimensional continuous action spaces