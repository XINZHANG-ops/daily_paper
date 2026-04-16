---
title: "GRPO"
slug: grpo
type: algorithm
paper_count: 5
last_updated: 2026-04-16
---

# GRPO (Group Relative Policy Optimization)

## What It Is

GRPO is a reinforcement learning algorithm that computes group-relative advantages by normalizing rewards within each sampled group. It has become the dominant RL algorithm for LLM training in the April 2026 period, appearing across reasoning, embodied AI, and reward shaping papers. Its simplicity (no critic network needed) and efficiency make it the default choice for RLVR experiments.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.03128]] | baseline | GRPO is the primary baseline RLSD compares against; RLSD outperforms GRPO by 2.32% average accuracy |
| [[2604.07430]] | core method | Used for task-aware RL with hybrid rewards in HY-Embodied-0.5 |
| [[2604.11297]] | core method | MEDS uses GRPO with error pattern clustering for reward shaping |
| [[2604.12627]] | baseline | KnowRL uses GRPO as baseline, shows it suffers from reward sparsity |
| [[2604.14144]] | core method | SpatialEvo uses GRPO with adaptive task scheduling for self-evolution |

## Connections

- [[topics/reinforcement-learning]] — GRPO is the primary RL algorithm in this period's research
- [[entities/ppo]] — PPO is an alternative algorithm used in some papers for comparison
