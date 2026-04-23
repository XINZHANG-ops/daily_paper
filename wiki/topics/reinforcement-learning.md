---
title: "Reinforcement Learning"
slug: reinforcement-learning
paper_count: 10
last_updated: 2026-04-21
---

# Reinforcement Learning

## Overview

Reinforcement learning for LLMs has evolved significantly across the papers seen in this period. The focus has shifted from simple reward maximization to addressing fundamental failure modes like template collapse, reward sparsity, and sampling diversity collapse. Papers explore how RL training dynamics differ between reasoning and non-reasoning tasks, and how to maintain both capability improvement and safety.

The key theme emerging across papers is that RL training has multiple **independent failure modes** that must be addressed simultaneously: entropy-based monitoring fails to detect template collapse (RAGEN-2), long-CoT SFT enables safety guardrail workarounds (2604.06628), on-policy RL suffers from stable error basin collapse (MEDS), and reward sparsity remains fundamental (KnowRL, 2604.06628).

## Evolution

In early April 2026, RAGEN-2 revealed that template collapse is a fundamental failure mode invisible to entropy-based metrics. KnowRL tackled reward sparsity through minimal-sufficient knowledge guidance, and MEDS addressed sampling diversity collapse through error pattern clustering. By mid-April, 2604.13016 analyzed on-policy distillation and RLSD demonstrated separating credit assignment magnitude from update direction. RAD-2 applied generator-discriminator RL to motion planning. On April 21, OneVL introduced latent CoT with world model supervision for VLA planning, Agent-World demonstrated multi-environment GRPO with self-evolving training, and Weak Supervision provided a systematic framework for understanding when RLVR generalizes vs memorizes—training reward saturation dynamics and reasoning faithfulness are the key predictors.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06268]] RAGEN-2 | 2026-04-09 | Template collapse identification and SNR-aware filtering |
| [[2604.03128]] Self-Distilled RLVR | 2026-04-08 | Token-level credit assignment via privileged information gain |
| [[2604.06628]] Rethinking Generalization | 2026-04-13 | Dip-and-recovery dynamic, safety-asymmetry in reasoning SFT |
| [[2604.11297]] MEDS | 2026-04-16 | Memory-enhanced reward shaping with error pattern clustering |
| [[2604.12627]] KnowRL | 2026-04-15 | Minimal-sufficient knowledge guidance for reward sparsity |
| [[2604.13016]] Rethinking OPD | 2026-04-15 | On-policy distillation failure conditions and recovery |
| [[2604.11626]] RationalRewards | 2026-04-17 | Reasoning-based reward model with dual-space optimization |
| [[2604.15308]] RAD-2 | 2026-04-20 | Generator-discriminator RL for motion planning with TC-GRPO and BEV-Warp |
| [[2604.18486]] OneVL | 2026-04-21 | Latent CoT with world model supervision for VLA planning (RL-aligned training pipeline) |
| [[2604.18292]] Agent-World | 2026-04-21 | Multi-environment GRPO with self-evolving diagnostic arena |
| [[2604.18574]] Weak Supervision | 2026-04-21 | RLVR saturation dynamics; reasoning faithfulness predicts generalization vs memorization |

## Patterns & Insights

- **Multiple independent failure modes**: RL training has template collapse (RAGEN-2), reward sparsity (KnowRL), sampling diversity collapse (MEDS), and credit assignment asymmetry (RLSD)—each requiring different solutions
- **Entropy monitoring is insufficient**: Template collapse is invisible to entropy metrics; MI-based diagnostics are needed
- **Credit assignment is distinct from update direction**: RLSD shows that separating magnitude (from privileged info) from direction (from environment reward) resolves OPSD's mutual information gap
- **Entropy monitoring is insufficient**: Template collapse is invisible to entropy metrics; MI-based diagnostics are needed
- **Safety is not free**: Reasoning capability improvement consistently comes with safety degradation
- **On-policy RL is fragile**: Stable error basin collapse happens when policy repeatedly generates similar errors
- **Dual-space optimization**: Test-time compute (prompt tuning) can match or exceed parameter-space training (RL)

## Open Problems

- How to detect template collapse early without MI-based diagnostics that require additional computation
- Whether safety-asymmetry can be addressed without sacrificing reasoning capability
- How to combine SNR-aware filtering with error pattern clustering for comprehensive failure mode coverage

## Connections

- [[topics/reasoning]] — RL training for reasoning has distinct failure modes from RL for other tasks
- [[topics/llm-training]] — RL is one of several post-training approaches, each with tradeoffs
- [[entities/grpo]] — Primary RL algorithm across multiple papers in this period