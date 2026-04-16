---
title: "RLSD"
slug: rlsd
type: algorithm
paper_count: 1
last_updated: 2026-04-16
---

# RLSD (Reinforcement Learning with Self-Distillation)

## What It Is

RLSD repurposes self-distillation from distribution matching to token-level credit assignment. The key insight is separating *update direction* (from environment reward) from *update magnitude* (from privileged information gain, the ratio of teacher-to-student log-probabilities). This resolves the mutual information gap that caused OPSD to fail. RLSD achieves 56.18% average accuracy across 5 multimodal reasoning benchmarks, outperforming GRPO by 2.32%.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.03128]] | introduced | The algorithm is the paper's main contribution |

## Connections

- [[topics/reinforcement-learning]] — RLSD addresses credit assignment failure in on-policy RL
- [[entities/opsd]] — RLSD fixes OPSD's mutual information gap problem
