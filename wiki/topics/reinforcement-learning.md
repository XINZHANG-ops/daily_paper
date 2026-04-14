---
title: "Reinforcement Learning"
slug: reinforcement-learning
paper_count: 2
last_updated: 2026-04-09
---

# Reinforcement Learning

## Overview

Two papers from this period address critical failure modes in reinforcement learning for language and agent systems: self-distillation credit assignment and reasoning collapse in multi-turn agent training. Together they reveal that standard RL objectives contain structural vulnerabilities that progressive training amplifies in opposite directions.

RLSD (Self-Distilled RLVR) addresses a fundamental failure mode in On-Policy Self-Distillation where a single model serves as both teacher and student with asymmetric information. The theoretical analysis proves that OPSD suffers from an irreducible mutual information gap I(Yt;R|X, Y<t)>0 caused by information asymmetry—the student's optimization cannot eliminate this gap because it is independent of theta. The gradient decomposition shows that early in training, beneficial marginal matching gradients dominate, but as training progresses and the student approaches the marginal teacher distribution, the pathological r-specific deviation dominates, driving the model toward encoding privileged information correlations. RLSD fundamentally repurposes self-distillation: instead of using the teacher for token-level distribution matching (which causes leakage), it uses the teacher for magnitude evaluation while anchoring update directions to environment rewards. The key property is that sign(A-hat) = sign(A)—the environment reward has exclusive authority over update direction.

RAGEN-2 identifies template collapse, a different failure mode where models produce superficially diverse reasoning that is actually input-agnostic. The key insight is that entropy—widely used to monitor reasoning stability—only measures diversity within the same input and cannot detect whether reasoning actually responds to different inputs. Even with stable entropy, models can rely on fixed templates that look diverse within any single input but are effectively the same across inputs. The paper decomposes reasoning quality into two axes: within-input diversity (conditional entropy H(Z|X)) and cross-input distinguishability (mutual information I(X;Z)). Template collapse manifests as high conditional entropy but low mutual information—reasoning appears diverse within each input but becomes input-agnostic across inputs. The SNR mechanism explains this: low reward variance weakens task gradients while input-agnostic regularization (KL divergence and entropy regularization) remains constant, causing regularization to dominate updates and erase cross-input reasoning differences.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.03128]] Self-Distilled RLVR | 2026-04-02 | Proves OPSD has irreducible mutual information gap; RLSD repurposes self-distillation for magnitude evaluation with environment rewards directing update direction |
| [[2604.06268]] RAGEN-2: Reasoning Collapse in Agentic RL | 2026-04-06 | Identifies template collapse where reasoning is input-agnostic despite stable entropy; proposes SNR-Aware Filtering to select high-signal prompts |

## Open Problems

- **Unified view of RL failure modes**: RLSD addresses information asymmetry in self-distillation while RAGEN-2 addresses signal-to-noise ratio in multi-turn agents—are these manifestations of a common underlying problem?
- **Generalization under stochastic environments**: When reward variance is uniformly low (80-100% stochasticity), SNR-Aware Filtering loses discriminative power.
- **Format validity vs content sensitivity**: Structural correctness and semantic input-dependence are separate dimensions—a model can have high format validity but low mutual information with inputs.
- **Leakage-free self-distillation**: RLSD shows leakage can be structurally prevented via stop-gradient, but can this principle be extended to settings requiring richer privileged information?

## Connections

- [[topics/agent-systems]] — Agent RL training often encounters template collapse; RLSD credit assignment could help
- [[topics/benchmarks]] — Benchmark insights about capability-reliability divide (Pass@3 vs Pass^3) connect to RL training dynamics