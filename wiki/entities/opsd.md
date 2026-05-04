---
title: "OPSD"
slug: opsd
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# OPSD

## What It Is

OPSD (On-Policy Self-Distillation) is a training approach that combines reinforcement learning with self-distillation: a teacher model generates privileged information, and a student model trained with on-policy RL tries to match the teacher's distribution while also optimizing for environment reward.

RLSD identifies a fundamental limitation in OPSD: the **mutual information gap**. Because the student generates outputs on-policy (constrained by its own current policy), it cannot access the full distribution of the teacher's privileged information. This creates an irreducible gap—no amount of distillation loss can close it because the student literally cannot see the teacher's high-quality outputs for states the student's policy doesn't visit. RLSD fixes this by repurposing self-distillation from distribution matching to token-level credit assignment, using teacher/student log-probability ratios as importance weights anchored to the environment reward signal.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.03128]] Self-Distilled RLVR | baseline | RLSD fixes OPSD's mutual information gap by repurposing distillation for credit assignment |

## Connections

- [[entities/rlsd]] — RLSD addresses OPSD's fundamental limitation by shifting distillation from output matching to credit assignment
- [[topics/reinforcement-learning]] — The mutual information gap is a structural vulnerability in on-policy RL + distillation combinations that may affect other RL training recipes
- [[ideas/on-policy-rl-idling]] — A complementary on-policy inefficiency: OPSD wastes information (student can't use teacher), while idling wastes computation (GPU idle during rollout)