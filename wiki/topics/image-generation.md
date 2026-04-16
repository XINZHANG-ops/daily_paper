---
title: "Image Generation"
slug: image-generation
paper_count: 5
last_updated: 2026-04-16
---

# Image Generation

## Overview

Image generation research has progressed along several dimensions: process-driven generation with interleaved reasoning, style transfer with consistent dataset curation, and numerical alignment for accurate object counts. The papers reveal that controllable image generation requires addressing both high-level semantic constraints (composition, style) and low-level structural constraints (counting, spatial relationships).

The key theme is that **generation quality depends on the granularity of control**: process-driven methods achieve fine-grained control through iterative refinement, style transfer methods achieve style control through dataset curation, and numerical alignment methods achieve counting accuracy through attention analysis.

## Evolution

In early April 2026, Think in Strokes introduced process-driven image generation with Plan→Sketch→Inspect→Refine cycles, showing that self-sampled critiques (learning from own errors) outperform external symbolic corrections. A day later, MegaStyle demonstrated that intra-style consistency in datasets is crucial—generated style pairs must share actual style characteristics, not just artist labels. Near the same time, NUMINA addressed counting accuracy by exploiting discriminative attention heads. By mid-April, OmniShow extended these ideas to video with human-object interaction, and Seedance 2.0 pushed the frontier on motion quality and audio-visual synchronization.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04746]] Think in Strokes | 2026-04-09 | Process-driven generation with self-sampled critiques |
| [[2604.08364]] MegaStyle | 2026-04-10 | Intra-style consistent dataset construction |
| [[2604.08546]] NUMINA | 2026-04-10 | Training-free counting alignment via attention heads |
| [[2604.11804]] OmniShow | 2026-04-14 | HOIVG with unified multimodal conditions |
| [[2604.14148]] Seedance 2.0 | 2026-04-16 | State-of-the-art video generation with audio |

## Patterns & Insights

- **Self-critique outperforms external correction**: Models internalize failure modes better from self-sampled data
- **Dataset quality matters for style**: Intra-style consistency, not artist labels, defines quality style datasets
- **Attention heads encode structural information**: Discriminative attention heads can identify instance boundaries
- **Audio-video synchronization is emerging frontier**: Beyond visual quality, audio synchronization becoming standard

## Open Problems

- How to scale process-driven generation to real-time applications without 8× cost increase
- Combining style transfer with process-driven generation for controllable stylized content
- General numerical alignment beyond counting (e.g., spatial relationships, proportions)

## Connections

- [[topics/computer-vision]] — Image generation is a core computer vision task
- [[topics/video-generation]] — Video generation extends image generation temporally
- [[entities/bagel]] — BAGEL used as base model for process-driven generation