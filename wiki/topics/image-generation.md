---
title: "Image Generation"
slug: image-generation
paper_count: 5
last_updated: 2026-04-21
---

# Image Generation

## Overview

Image generation research has progressed along several dimensions: process-driven generation with interleaved reasoning, style transfer with consistent dataset curation, and numerical alignment for accurate object counts. The papers reveal that controllable image generation requires addressing both high-level semantic constraints (composition, style) and low-level structural constraints (counting, spatial relationships).

The key theme is that **generation quality depends on the granularity of control**: process-driven methods achieve fine-grained control through iterative refinement, style transfer methods achieve style control through dataset curation, and numerical alignment methods achieve counting accuracy through attention analysis.

## Evolution

In early April 2026, Think in Strokes introduced process-driven image generation with Plan→Sketch→Inspect→Refine cycles. MegaStyle demonstrated that intra-style consistency in datasets is crucial. NUMINA addressed counting accuracy by exploiting discriminative attention heads. By mid-April, OmniShow extended these ideas to video with human-object interaction, and Seedance 2.0 pushed the frontier on motion quality and audio-visual synchronization. RationalRewards showed that reasoning-based reward models resist hacking better than scalar scores, and DCW addressed SNR-timestep bias. On April 21, EMF extended MeanFlow's one-step class-conditional generation to text conditioning by identifying discriminability and disentanglement as the two key text representation properties—achieving GenEval 0.90 with only 4 steps.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04746]] Think in Strokes | 2026-04-09 | Process-driven generation with self-sampled critiques |
| [[2604.08364]] MegaStyle | 2026-04-10 | Intra-style consistent dataset construction |
| [[2604.11626]] RationalRewards | 2026-04-17 | Reasoning-based reward model for visual generation |
| [[2604.16044]] SNR-t Bias | 2026-04-20 | DCW correction for diffusion model SNR-timestep bias |
| [[2604.18168]] EMF | 2026-04-21 | Extending MeanFlow one-step generation to text conditioning via discriminative text representations |

## Patterns & Insights

- **Self-critique outperforms external correction**: Models internalize failure modes better from self-sampled data
- **Dataset quality matters for style**: Intra-style consistency, not artist labels, defines quality style datasets
- **Attention heads encode structural information**: Discriminative attention heads can identify instance boundaries
- **Audio-video synchronization is emerging frontier**: Beyond visual quality, audio synchronization becoming standard
- **Reasoning rewards resist hacking**: Multi-dimensional structured reasoning prevents reward hacking better than scalar scores
- **SNR-t bias is universal**: All DPMs suffer from misalignment between sample SNR and timestep during inference; DCW provides training-free remedy

## Open Problems

- How to scale process-driven generation to real-time applications without 8× cost increase
- Combining style transfer with process-driven generation for controllable stylized content
- General numerical alignment beyond counting (e.g., spatial relationships, proportions)

## Connections

- [[topics/computer-vision]] — Image generation is a core computer vision task
- [[topics/video-generation]] — Video generation extends image generation temporally
- [[entities/bagel]] — BAGEL used as base model for process-driven generation