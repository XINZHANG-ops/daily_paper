---
title: "Agent Evaluation"
slug: agent-evaluation
paper_count: 5
last_updated: 2026-04-20
---

# Agent Evaluation

## Overview

Agent evaluation has evolved from simple capability benchmarks to understanding the gap between sandbox performance and real-world reliability, and now to simulating professional environments without real infrastructure. The papers reveal that traditional accuracy metrics fail to capture what matters: whether agents can consistently perform tasks across variations, handle silent failures, and whether evaluation settings reflect actual use cases.

## Evolution

Mid-April 2026 saw Claw-Eval establish that trustworthy evaluation requires full-trajectory auditing across three evidence channels (final output, intermediate reasoning, tool call traces). DR3-Eval extended this to deep research agents, identifying hallucination as the primary failure mode and revealing that longer contexts degrade performance. At month's end, OccuBench introduced Language Environment Simulators (LES) that can simulate any professional domain without real infrastructure — revealing that implicit faults (truncated data, missing fields) cause larger drops than explicit errors (HTTP 500s) because agents lack error signals to trigger re-query behavior.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06132]] Claw-Eval | 2026-04-08 | Full-trajectory auditing across three evidence channels |
| [[2604.08523]] ClawBench | 2026-04-10 | Real-world vs sandbox performance gap revelation |
| [[2604.11641]] CodeTracer | 2026-04-14 | Evidence-to-action gap diagnosis in code agents |
| [[2604.14683]] DR3-Eval | 2026-04-17 | Deep research agent evaluation with realistic + reproducible design |
| [[2604.10866]] OccuBench | 2026-04-20 | LES-based professional domain simulation, revealing implicit fault hardness |

## Patterns & Insights

- **Full-trajectory auditing**: Evaluation must consider reasoning process, not just final output
- **Realism vs controllability**: Dynamic environments are realistic but not reproducible; static corpora are controllable but not dynamic
- **Hallucination is primary failure mode**: Across all models, hallucination dominates other failure modes
- **Longer contexts hurt**: Increased context length correlates with performance degradation
- **Implicit faults are hardest**: Silent data degradation (no error signals) causes larger drops than explicit errors with clear signals
- **Industry-specific capabilities**: Each model has distinct occupational specializations invisible to single-domain benchmarks

## Open Problems

- Bridging dynamic web environments with reproducible evaluation
- Detecting hallucination in real-time before output generation
- Scaling evaluation to cover diverse research agent scenarios
- Designing LES configurations that maintain fidelity across professional domains

## Connections

- [[topics/agent-systems]] — Evaluation frameworks define what "good" means for agent systems
- [[topics/benchmarks]] — Both Claw-Eval and DR3-Eval create benchmark datasets
- [[ideas/agent-reliability-systems]] — Agent reliability requires evaluation + training + deployment infrastructure