---
title: "Multimodal Reasoning"
slug: multimodal-reasoning
paper_count: 3
last_updated: 2026-04-14
---

# Multimodal Reasoning

## Overview

Multimodal reasoning encompasses the ability of AI systems to jointly process and reason about information from multiple modalities—text, images, video, audio—and to generate coherent outputs across these modalities. Three papers now address complementary challenges: Self-Distilled RLVR's leak-free self-distillation for training multimodal reasoning, Think in Strokes' process-driven image generation with interleaved reasoning, and Pseudo-Unification's information-theoretic analysis of why Unified Multimodal Models fail to achieve true synergy between text and image generation.

Self-Distilled RLVR (2604.03128) addresses a fundamental challenge in multimodal reasoning training: the failure mode of On-Policy Self-Distillation (OPSD) where information asymmetry between teacher and student causes privileged information leakage and progressive degradation.

Think in Strokes (2604.04746) introduces process-driven image generation as a new paradigm for multimodal reasoning, decomposing image synthesis into interleaved Plan→Sketch→Inspect→Refine cycles where textual and visual states tightly co-evolve.

Pseudo-Unification (2604.10949) takes a different approach, analyzing why existing UMMs fail to achieve true multimodal synergy. The key finding: despite shared parameters, text generation shows high-entropy creativity while image synthesis enforces low-entropy fidelity. This "pseudo-unification" stems from dual divergence in both encoding (vision and language follow different entropy trajectories) and response patterns (text vs image generation behave differently). Only models like Harmon that use contextual prediction for both modalities achieve genuine unification, suggesting that architectural choices fundamentally determine whether reasoning transfers across modalities.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.03128]] Self-Distilled RLVR | 2026-04-02 | RLSD: leak-free self-distillation for multimodal reasoning; 56.18% avg accuracy on MMMU, MathVista, MathVision, ZeroBench, WeMath |
| [[2604.04746]] Think in Strokes, Not Pixels | 2026-04-07 | Process-driven image generation with Plan→Sketch→Inspect→Refine cycles; 8x training data reduction vs PARM |
| [[2604.10949]] Pseudo-Unification: Entropy Probing | 2026-04-14 | Information-theoretic analysis of UMM unification; reveals dual divergence (modality-asymmetric encoding + pattern-split response) |

## Open Problems

- Generalizing RLSD's leak-free self-distillation approach to pure text reasoning and video understanding remains underexplored
- Process-driven generation could be extended to video and 3D content, requiring temporal coherence across multiple frames
- Self-sampled critique traces could be improved by explicitly modeling which error modes are learnable versus harmful
- The trade-off between reasoning trajectory length and output quality is not yet well understood

## Connections

- [[topics/reasoning]] — Both papers address reasoning patterns; RLVR directly contributes to reasoning benchmarks while Think in Strokes enables reasoning about visual composition
- [[topics/vision-language-models]] — The tightly coupled text-visual reasoning in Think in Strokes builds on VLM advances in visual representation learning