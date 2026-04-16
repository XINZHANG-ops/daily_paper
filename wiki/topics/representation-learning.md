---
title: "Representation Learning"
slug: representation-learning
paper_count: 1
last_updated: 2026-04-16
---

# Representation Learning

## Overview

Representation learning focuses on learning representations that are useful for multiple tasks. The papers reveal that **frozen pretrained models have latent capabilities that only need lightweight interfaces to exploit**—SteerViT achieves a new Pareto frontier by adding gated cross-attention to frozen ViTs, simultaneously improving steerability and maintaining representation quality.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.02327]] SteerViT | 2026-04-06 | Steerable frozen ViT via gated cross-attention, new representation/steerability Pareto frontier |

## Patterns & Insights

- **Frozen models have latent steerability**: DINOv2's 44% to 96% on CORE retrieval shows untapped capability
- **Early fusion beats late fusion**: Interleaving cross-attention within ViT blocks preserves representation quality
- **Referential segmentation as pretext**: Natural supervision for vision-language alignment without degrading ViT

## Open Problems

- Scaling steerability to open-world natural language queries
- Combining steerability with other model capabilities (e.g., reasoning)
- Understanding why frozen representations remain high-quality after minimal conditioning

## Connections

- [[topics/computer-vision]] — Visual representation learning is foundational
- [[topics/multimodal-models]] — Steerability requires vision-language alignment
- [[entities/dinov2]] — The frozen ViT backbone whose latent steerability SteerViT unlocks
