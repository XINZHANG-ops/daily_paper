---
title: "OPSD"
slug: opsd
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# OPSD

## What It Is

OPSD (On-Policy Self-Distillation) has a mutual information gap problem that RLSD fixes. The gap arises because on-policy constraints prevent the student from fully leveraging the teacher's knowledge.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.03128]] Self-Distilled RLVR | baseline | RLSD fixes OPSD's mutual information gap |

## Connections

- [[entities/rlsd]] — RLSD addresses OPSD's mutual information gap
- [[topics/reasoning]] — On-policy distillation for reasoning tasks