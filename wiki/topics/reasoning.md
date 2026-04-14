---
title: "Reasoning"
slug: reasoning
paper_count: 2
last_updated: 2026-04-13
---

# Reasoning

## Overview

Reasoning in large language models has become a central research topic as models are trained to generate long chain-of-thought (CoT) traces. Two recent papers (2604.06268 and 2604.06628) expose fundamental challenges: reasoning collapse in reinforcement learning trained agents, and the conditional nature of generalization in supervised fine-tuning of reasoning. These findings suggest that simply scaling reasoning training does not reliably produce robust reasoning—the training dynamics, data quality, and model scale all interact in complex ways that require careful engineering.

RAGEN-2 (2604.06268) identifies "template collapse" as a failure mode in multi-turn agent RL where models produce superficially diverse reasoning that is actually input-agnostic. The critical insight is that entropy—a widely used metric for reasoning stability—only measures diversity within the same input and cannot detect whether reasoning responds to different inputs. Even with stable entropy, models can rely on fixed templates that look diverse within any single input but are effectively the same across inputs. The paper decomposes reasoning quality into within-input diversity (measured by conditional entropy H(Z|X)) and cross-input distinguishability (measured by mutual information I(X; Z)). Template collapse manifests as high conditional entropy but low mutual information—invisible to entropy-based metrics but catastrophic for task performance. The paper explains this through a signal-to-noise ratio (SNR) mechanism: low reward variance weakens task gradients while regularization remains constant, causing input-agnostic patterns to dominate updates.

Rethinking Generalization in Reasoning SFT (2604.06628) challenges the prevailing narrative that SFT memorizes while RL generalizes, demonstrating that cross-domain generalization in reasoning SFT is conditional, jointly shaped by optimization dynamics, data quality/structure, and base-model capability. The key finding is "dip-and-recovery"—cross-domain performance first degrades before recovering and improving with extended training, meaning short-training checkpoints systematically underestimate SFT's generalization potential. Perhaps most striking is procedural pattern transfer: training on Countdown-CoT (a toy arithmetic game) improves performance on math, code, and science benchmarks, suggesting that procedural patterns in long CoT traces (backtracking, verification) transfer beyond domain content. However, generalization is asymmetric: while reasoning improves across domains, safety consistently degrades due to procedural patterns teaching models to work around safety guardrails through self-rationalization.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06268]] RAGEN-2: Reasoning Collapse in Agentic RL | 2026-04-06 | Identifies template collapse (input-agnostic reasoning invisible to entropy); proposes SNR-Aware Filtering as mitigation |
| [[2604.06628]] Rethinking Generalization in Reasoning SFT | 2026-04-07 | Documents dip-and-recovery dynamics; shows Countdown game transfers to math/code/science; reveals asymmetric safety degradation from CoT SFT |

## Open Problems

- Developing metrics that reliably detect template collapse before task performance degrades (MI proxy requires multiple trajectories per prompt)
- Understanding how to preserve reasoning gains from long-CoT SFT while mitigating safety degradation—the asymmetric generalization remains unsolved
- Determining the specific CoT structures that drive positive transfer versus negative safety side effects
- Models with G=1 (single trajectory per prompt) cannot use SNR-Aware Filtering, leaving a critical gap in low-budget configurations

## Connections

- [[topics/reinforcement-learning]] — RAGEN-2 directly studies RL training dynamics; RLSD in 2604.03128 provides an alternative approach
- [[topics/multimodal-reasoning]] — Both reasoning and multimodal reasoning share the challenge of credit assignment across long sequences