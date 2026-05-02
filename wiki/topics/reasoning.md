---
title: "Reasoning"
slug: reasoning
paper_count: 11
last_updated: 2026-04-18
---

# Reasoning

## Overview

Reasoning research addresses how LLMs can chain thoughts, generalize across domains, and avoid failure modes like template collapse. Key themes: entropy monitoring is insufficient, dip-and-recovery dynamics in SFT, and distinct RL failure modes for reasoning tasks.

## Evolution

Early April 2026 saw Self-Distilled RLVR (2604.03128) advance token-level credit assignment for reasoning. RAGEN-2 (2604.06268) revealed template collapse as a fundamental failure mode invisible to entropy metrics. KnowRL (2604.12627) tackled reward sparsity through knowledge point guidance. MEDS (2604.11297) addressed sampling diversity collapse through error pattern clustering.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.03128]] Self-Distilled RLVR | 2026-04-08 | Token-level credit assignment via privileged information gain |
| [[2604.04921]] TriAttention | 2026-04-07 | Trigonometric KV compression for long reasoning |
| [[2604.06268]] RAGEN-2 | 2026-04-09 | Template collapse identification and SNR-aware filtering |
| [[2604.06628]] Rethinking Generalization | 2026-04-13 | Dip-and-recovery dynamic in reasoning SFT |
| [[2604.10949]] Pseudo-Unification | 2026-04-14 | Entropy probing reveals divergent multimodal reasoning |
| [[2604.12627]] KnowRL | 2026-04-15 | Minimal-sufficient knowledge guidance for reward sparsity |
| [[2604.11297]] MEDS | 2026-04-16 | Memory-enhanced reward shaping with error clustering |
| [[2604.11626]] RationalRewards | 2026-04-17 | Reasoning-based reward model |
| [[2604.05404]] Beyond Accuracy | 2026-04-08 | Inefficiency patterns in tool-integrated reasoning |
| [[2604.14683]] DR3-Eval | 2026-04-17 | Deep research evaluation revealing hallucination as primary failure |
| [[2604.18574]] Weak Supervision | 2026-04-21 | When LLMs can learn to reason with weak supervision |

## Patterns & Insights

- **Entropy monitoring fails**: Template collapse invisible to entropy; MI-based diagnostics needed
- **RL has distinct failure modes**: Different from RL for non-reasoning tasks
- **Dip-and-recovery**: Cross-domain generalization in SFT follows conditional pattern
- **Test-time compute scaling**: Prompt tuning can match RL fine-tuning

## Connections

- [[topics/reinforcement-learning]] — RL training for reasoning has unique failure modes
- [[topics/llm-training]] — Reasoning is a key post-training target
- [[entities/ppo]] — Primary RL algorithm for reasoning tasks