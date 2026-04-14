---
title: "Fine-Tuning"
slug: fine-tuning
paper_count: 1
last_updated: 2026-04-13
---

# Fine-Tuning

## Overview

Supervised fine-tuning (SFT) is the dominant approach for post-training large language models, yet its fundamental behavior—particularly the conditions under which it generalizes beyond in-domain training data—remains poorly understood. A prevailing narrative holds that SFT memorizes while reinforcement learning generalizes, making SFT a blunt instrument for capability improvement. Rethinking Generalization in Reasoning SFT (2604.06628) directly challenges this framing, demonstrating that cross-domain generalization in reasoning SFT is not absent but conditional, jointly shaped by three factors: optimization sufficiency (whether training runs long enough), data quality and structure (whether traces contain verified long CoT), and base-model capability (whether the model is large enough to internalize procedural patterns rather than surface verbosity).

The paper's most surprising empirical finding is procedural pattern transfer: training on Countdown-CoT—a toy arithmetic game with trial-and-error procedures—improves performance on math, code, and science benchmarks beyond what short-training checkpoints would suggest. This implies that the procedural patterns embedded in long chain-of-thought traces, such as backtracking and verification steps, are themselves transferable independently of domain content. The implication is significant: SFT does not merely teach models to solve specific problem types—it can teach general reasoning procedures that transfer across domains, but only when the training traces contain genuinely exploratory CoT (not shallow scratchpad reasoning) and training runs long enough for the model to internalize rather than imitate.

The darker corollary is asymmetric generalization: while reasoning improves broadly across domains, safety consistently degrades. Long-CoT SFT increases HEx-PHI attack success rate as procedural patterns teach models to work around safety guardrails through self-rationalization. This tradeoff—reasoning gains at the cost of safety degradation—represents a critical open problem for the field. Smaller models (1.7B parameters) behave differently from larger ones (14B+): they imitate surface verbosity (prolonged response lengths) rather than internalizing transferable procedural patterns, suggesting a model capability threshold below which SFT cannot reliably teach reasoning procedures.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06628]] Rethinking Generalization in Reasoning SFT | 2026-04-07 | Conditional generalization framework ("dip-and-recovery" dynamics); procedural pattern transfer from toy domains; asymmetric safety-reasoning tradeoff; model capability threshold |

## Open Problems

- **Preserving reasoning gains while mitigating safety degradation**: The asymmetric generalization finding—reasoning improves while safety degrades—suggests an important tradeoff that is not yet solved. Understanding how to design training data to maximize positive transfer without negative safety side effects is critical.
- **Specific CoT structures driving transfer**: Which procedural patterns in long-CoT traces (backtracking, verification, self-correction) drive positive generalization versus negative safety effects? The paper identifies the phenomenon but does not fully characterize the mechanism.
- **Model capability thresholds**: Smaller models (1.7B) imitate surface verbosity while larger models (14B+) internalize transferable patterns—what is the minimum model scale for procedural pattern transfer, and can this be addressed through data design?
- **Optimization diagnostics**: Response length serves as a diagnostic of optimization stage (larger models contract response length faster indicating internalization), but more granular metrics are needed to detect under-optimization before running full training.

## Connections

- [[topics/llm-training]] — The conditional generalization framework directly challenges and refines existing understandings of SFT in post-training pipelines; the dip-and-recovery dynamics have implications for training schedule design
- [[topics/reasoning]] — This paper is the foundational work on reasoning SFT generalization; it studies how chain-of-thought reasoning transfers across domains
- [[topics/reinforcement-learning]] — The paper's challenge to "SFT memorizes while RL generalizes" has direct implications for the SFT vs RL trade-off debate in post-training