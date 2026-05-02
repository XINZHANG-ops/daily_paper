---
title: "LLM Training"
slug: llm-training
paper_count: 10
last_updated: 2026-04-17
---

# LLM Training

## Overview

LLM training research spans multiple dimensions: data selection (textual frequency, data-centric optimization), optimization strategies (curriculum learning), and knowledge transfer (distillation). The papers reveal that **training efficiency depends on matching data characteristics to model capabilities**—high-frequency data for prompting, data-centric methods (DataFlex) for unified selection/weighting, and thinking-pattern consistency for distillation.

The key theme is that training recipes are not universal—they must be adapted to the specific model, data distribution, and objective.

## Evolution

Early April 2026 saw Adam's Law establish textual frequency as a fundamental dimension for data selection—high-frequency data works better for both prompting and fine-tuning. A week later, 2604.06628 showed that cross-domain generalization in SFT follows a dip-and-recovery dynamic, challenging the "SFT memorizes, RL generalizes" assumption. KnowRL decomposed hints into atomic knowledge points for minimal-sufficient guidance. 2604.13016 analyzed on-policy distillation and found thinking-pattern consistency as the key condition for success.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.02176]] Adam's Law | 2026-04-09 | Textual frequency as training/prompting dimension |
| [[2603.26164]] DataFlex | 2026-04-06 | Unified framework for data-centric dynamic training |
| [[2604.06628]] Rethinking Generalization | 2026-04-13 | SFT has conditional generalization, not absent |
| [[2604.08377]] SkillClaw | 2026-04-10 | Collective skill evolution via agentic evolver |
| [[2604.11297]] MEDS | 2026-04-16 | Memory-enhanced reward shaping with error clustering |
| [[2604.12627]] KnowRL | 2026-04-15 | Atomic knowledge points for minimal-sufficient guidance |
| [[2604.13016]] Rethinking OPD | 2026-04-15 | Thinking-pattern consistency for distillation |
| [[2604.16044]] Elucidating SNR-t | 2026-04-20 | SNR-t bias in diffusion models affecting training |
| [[2604.11626]] RationalRewards | 2026-04-17 | Test-time prompt tuning matches RL fine-tuning |
| [[2604.18292]] Agent-World | 2026-04-21 | Multi-environment GRPO with self-evolving training arena |

## Patterns & Insights

- **Frequency matters**: High-frequency data improves both prompting and fine-tuning
- **SFT can generalize conditionally**: Not just memorization as previously thought
- **Distillation requires compatibility**: Thinking patterns must match between teacher and student
- **Test-time compute scaling**: Prompt tuning can match or exceed parameter-space training (RL)

## Open Problems

- Combining frequency-based selection with other dimensions (quality, diversity)
- Understanding when SFT vs RL is more appropriate for specific objectives
- Scaling distillation to very large teacher-student capability gaps

## Connections

- [[topics/reinforcement-learning]] — RL is one approach to post-training, with distinct tradeoffs from SFT
- [[topics/nlp]] — Textual frequency is especially relevant for NLP tasks
- [[entities/grpo]] — Used in multiple training recipes this period