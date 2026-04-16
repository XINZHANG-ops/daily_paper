---
title: "Reinforcement Learning"
slug: reinforcement-learning
paper_count: 8
last_updated: 2026-04-16
---

# Reinforcement Learning

## Overview

Reinforcement learning for LLMs has evolved significantly across the papers seen in this period. The focus has shifted from simple reward maximization to addressing fundamental failure modes like template collapse, reward sparsity, and sampling diversity collapse. Papers explore how RL training dynamics differ between reasoning and non-reasoning tasks, and how to maintain both capability improvement and safety.

The key theme emerging across papers is that RL training has multiple **independent failure modes** that must be addressed simultaneously: entropy-based monitoring fails to detect template collapse (RAGEN-2), long-CoT SFT enables safety guardrail workarounds (2604.06628), on-policy RL suffers from stable error basin collapse (MEDS), and reward sparsity remains fundamental (KnowRL, 2604.06628).

## Evolution

In early April 2026, RAGEN-2 revealed that template collapse is a fundamental failure mode invisible to entropy-based metrics—reasoning appears diverse within inputs but becomes input-agnostic across inputs. Three days later, 2604.06628 showed that cross-domain generalization in reasoning SFT follows a "dip-and-recovery" dynamic and that safety degradation is an unavoidable cost of reasoning improvement. Around the same time, KnowRL tackled reward sparsity through minimal-sufficient knowledge point guidance, and MEDS addressed sampling diversity collapse through error pattern clustering. By mid-April, 2604.13016 analyzed on-policy distillation and found that thinking-pattern consistency and genuinely new knowledge are the two conditions for successful teacher-student transfer. RLSD (2604.03128) further advanced the field by demonstrating that separating token-level credit assignment magnitude (from privileged information) from update direction (from environment reward) resolves the mutual information gap that plagued earlier on-policy self-distillation approaches.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06268]] RAGEN-2 | 2026-04-09 | Template collapse identification and SNR-aware filtering |
| [[2604.03128]] Self-Distilled RLVR | 2026-04-08 | Token-level credit assignment via privileged information gain |
| [[2604.06628]] Rethinking Generalization | 2026-04-13 | Dip-and-recovery dynamic, safety-asymmetry in reasoning SFT |
| [[2604.11297]] MEDS | 2026-04-16 | Memory-enhanced reward shaping with error pattern clustering |
| [[2604.12627]] KnowRL | 2026-04-15 | Minimal-sufficient knowledge guidance for reward sparsity |
| [[2604.03128]] Self-Distilled RLVR | 2026-04-08 | Token-level credit assignment via privileged information gain |
| [[2604.13016]] Rethinking OPD | 2026-04-15 | On-policy distillation failure conditions and recovery |

## Patterns & Insights

- **Multiple independent failure modes**: RL training has template collapse (RAGEN-2), reward sparsity (KnowRL), sampling diversity collapse (MEDS), and credit assignment asymmetry (RLSD)—each requiring different solutions
- **Entropy monitoring is insufficient**: Template collapse is invisible to entropy metrics; MI-based diagnostics are needed
- **Credit assignment is distinct from update direction**: RLSD shows that separating magnitude (from privileged info) from direction (from environment reward) resolves OPSD's mutual information gap
- **Entropy monitoring is insufficient**: Template collapse is invisible to entropy metrics; MI-based diagnostics are needed
- **Safety is not free**: Reasoning capability improvement consistently comes with safety degradation
- **On-policy RL is fragile**: Stable error basin collapse happens when policy repeatedly generates similar errors

## Open Problems

- How to detect template collapse early without MI-based diagnostics that require additional computation
- Whether safety-asymmetry can be addressed without sacrificing reasoning capability
- How to combine SNR-aware filtering with error pattern clustering for comprehensive failure mode coverage

## Connections

- [[topics/reasoning]] — RL training for reasoning has distinct failure modes from RL for other tasks
- [[topics/llm-training]] — RL is one of several post-training approaches, each with tradeoffs
- [[entities/grpo]] — Primary RL algorithm across multiple papers in this period