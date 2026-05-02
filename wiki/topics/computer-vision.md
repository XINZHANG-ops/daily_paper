---
title: "Computer Vision"
slug: computer-vision
paper_count: 11
last_updated: 2026-04-16
---

# Computer Vision

## Overview

Computer vision research spans multiple domains: image generation, 3D detection, style transfer, video understanding, and visual representation learning. The papers reveal that **vision capabilities are increasingly measured by controllability and real-world generalization**, not just benchmark accuracy. Key advances include steerable frozen ViTs, simple baselines that beat complex memory mechanisms, and better understanding of the perception-memory tradeoff in streaming scenarios.

## Evolution

Early April 2026 saw representation learning advances: SteerViT unlocked latent steerability in frozen ViTs, while SIMPLESTREAM showed simple sliding windows match complex memory for streaming. Mid-April brought generation improvements—NUMINA addressed counting alignment, MegaStyle handled style transfer, and OmniShow and Seedance 2.0 advanced video generation. WildDet3D extended vision to 3D open-vocabulary detection, and Pseudo-Unification revealed that shared parameters don't guarantee true multimodal unification.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.02327]] SteerViT | 2026-04-06 | Steerable frozen ViT via gated cross-attention, new representation quality/steerability Pareto frontier |
| [[2604.02317]] SIMPLESTREAM | 2026-04-06 | Simple sliding window matches complex memory mechanisms for streaming video |
| [[2604.04746]] Think in Strokes | 2026-04-09 | Process-driven image generation with self-correction |
| [[2604.04771]] MinerU2.5-Pro | 2026-04-07 | Document parsing with unified multimodal pipeline |
| [[2604.08364]] MegaStyle | 2026-04-10 | Style transfer with intra-style consistency |
| [[2604.08546]] NUMINA | 2026-04-10 | Counting alignment via attention heads in video |
| [[2604.08626]] WildDet3D | 2026-04-13 | Open-vocabulary 3D detection at scale |
| [[2604.10949]] Pseudo-Unification | 2026-04-14 | Entropy analysis of visual/linguistic encoding |
| [[2604.11804]] OmniShow | 2026-04-14 | Human-object interaction video generation |
| [[2604.18168]] EMF | 2026-04-21 | Extending one-step MeanFlow image generation to text-conditioned |
| [[2604.18486]] OneVL | 2026-04-21 | Latent CoT with world model supervision for embodied vision |

## Patterns & Insights

- **Controllability is key**: Models must support fine-grained control beyond generic quality
- **Real-world generalization**: Open-vocabulary and few-shot capabilities essential
- **Self-correction improves reliability**: Process-driven with inspection beats single-pass

## Connections

- [[topics/image-generation]] — Core computer vision generation task
- [[topics/3d-detection]] — 3D understanding extends 2D vision
- [[topics/video-generation]] — Video adds temporal dimension