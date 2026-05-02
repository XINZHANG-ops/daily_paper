---
title: "Benchmarks"
slug: benchmarks
paper_count: 5
last_updated: 2026-04-20
---

# Benchmarks

## Overview

Benchmarks define what "good performance" means for AI systems. Recent papers emphasize that benchmarks should assess beyond per-question accuracy—consistency, coherence, and hierarchical capability matter—and that evaluation coverage must extend to professional domains previously considered inaccessible without real infrastructure.

## Evolution

Early April 2026, Video-MME-v2 (2604.05015) established that video understanding benchmarks must assess beyond per-question accuracy, introducing consistency and coherence metrics. A week later, DR3-Eval (2604.14683) extended this lesson to deep research agents, revealing hallucination as the primary failure mode. At month's end, OccuBench (2604.10866) introduced Language Environment Simulators enabling cross-industry evaluation in domains previously untestable (emergency triage, nuclear safety, customs processing) — revealing that no single model dominates all industries and that implicit faults are harder than explicit ones.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.05015]] Video-MME-v2 | 2026-04-08 | Next-generation video benchmark assessing consistency and coherence |
| [[2604.06132]] Claw-Eval | 2026-04-08 | Full-trajectory auditing benchmark for agent evaluation |
| [[2604.08523]] ClawBench | 2026-04-10 | Real-world everyday task benchmark revealing sandbox gap |
| [[2604.14683]] DR3-Eval | 2026-04-17 | Deep research agent evaluation with hallucination focus |
| [[2604.10866]] OccuBench | 2026-04-20 | Cross-industry LES-based evaluation revealing model specializations |

## Patterns & Insights

- **Per-question accuracy is insufficient**: Real capability assessment requires consistency checks
- **Benchmark quality varies dramatically**: Gap between sandbox and real-world performance (ClawBench)
- **LES extends benchmark coverage**: "Any domain an LLM can understand" becomes testable via configuration-only simulation
- **Industry-specific profiles**: Each model has distinct occupational capabilities invisible to single-domain benchmarks

## Connections

- [[topics/agent-evaluation]] — Benchmarks are tools for agent evaluation
- [[topics/video-understanding]] — Video benchmarks assess multimodal understanding