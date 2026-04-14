---
title: "Multimodal Reasoning"
slug: multimodal-reasoning
paper_count: 2
last_updated: 2026-04-09
---

# Multimodal Reasoning

## Overview

Multimodal reasoning encompasses the ability of AI systems to jointly process and reason about information from multiple modalities—text, images, video, audio—and to generate coherent outputs across these modalities. Recent work has made significant strides in both understanding multimodal inputs (as in RLVR's multimodal reasoning benchmarks) and generating multimodal outputs (as in process-driven image generation). The field is moving beyond simple fusion toward tightly coupled reasoning where textual and visual states co-evolve.

Self-Distilled RLVR (2604.03128) addresses a fundamental challenge in multimodal reasoning training: the failure mode of On-Policy Self-Distillation (OPSD) where information asymmetry between teacher and student causes privileged information leakage and progressive degradation. The paper proves that OPSD suffers from an irreducible mutual information gap I(Yt;R|X, Y<t)>0 caused by the teacher receiving reference answers the student cannot observe. The proposed RLSD fundamentally repurposes self-distillation from a generative target to a magnitude evaluator—environment rewards determine update direction while the privileged teacher modulates update magnitude. This leak-free approach achieves 56.18% average accuracy across five multimodal reasoning benchmarks, with particularly strong gains on tasks like MathVision (+3.91%) where fine-grained discrimination of reasoning steps matters.

Think in Strokes (2604.04746) introduces process-driven image generation as a new paradigm for multimodal reasoning, decomposing image synthesis into interleaved Plan→Sketch→Inspect→Refine cycles where textual and visual states tightly co-evolve. The key innovation is that textual reasoning explicitly conditions how visual state should evolve, while the generated visual intermediate constrains and grounds the next round of textual reasoning. The approach addresses the supervision challenge for ambiguous intermediate states through scene-graph subsampling for contradiction-free incremental instructions and self-sampled critique traces that learn from the model's own errors. Notably, it achieves comparable performance to the 12B FLUX.1-dev model while using only 7B parameters, with particularly strong gains on position (+21%) and color attributes (+23%)—tasks that require the model to reason precisely about spatial and visual relationships.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.03128]] Self-Distilled RLVR | 2026-04-02 | RLSD: leak-free self-distillation for multimodal reasoning; 56.18% avg accuracy on MMMU, MathVista, MathVision, ZeroBench, WeMath |
| [[2604.04746]] Think in Strokes, Not Pixels | 2026-04-07 | Process-driven image generation with Plan→Sketch→Inspect→Refine cycles; 8x training data reduction vs PARM |

## Open Problems

- Generalizing RLSD's leak-free self-distillation approach to pure text reasoning and video understanding remains underexplored
- Process-driven generation could be extended to video and 3D content, requiring temporal coherence across multiple frames
- Self-sampled critique traces could be improved by explicitly modeling which error modes are learnable versus harmful
- The trade-off between reasoning trajectory length and output quality is not yet well understood

## Connections

- [[topics/reasoning]] — Both papers address reasoning patterns; RLVR directly contributes to reasoning benchmarks while Think in Strokes enables reasoning about visual composition
- [[topics/vision-language-models]] — The tightly coupled text-visual reasoning in Think in Strokes builds on VLM advances in visual representation learning