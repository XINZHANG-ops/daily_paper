---
title: "Claw-Eval"
slug: claw-eval
type: benchmark
paper_count: 1
last_updated: 2026-04-16
---

# Claw-Eval

## What It Is

Claw-Eval is a trustworthy evaluation framework for autonomous agents with 300 tasks and 14 frontier models. It introduces full-trajectory auditing via three independent evidence channels (execution traces, audit logs, environment snapshots) and integrated multi-dimensional scoring (Completion, Safety, Robustness). Claw-Eval reveals that trajectory-opaque evaluation misses 44% of safety violations and 13% of robustness failures, and that question quality (r=0.87) predicts multi-turn success far better than quantity (r=0.07).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06132]] | introduced | Claw-Eval is the paper's main contribution |

## Connections

- [[topics/agent-evaluation]] — Claw-Eval is the foundational framework for trustworthy agent evaluation
- [[topics/agent-systems]] — Provides the evaluation infrastructure for agent research
