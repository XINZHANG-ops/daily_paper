---
title: "DINOv2"
slug: dinov2
type: model
paper_count: 1
last_updated: 2026-04-16
---

# DINOv2

## What It Is

DINOv2 is a frozen Vision Transformer backbone pretrained via self-supervised learning. SteerViT demonstrates that DINOv2 has latent steerability untapped by its original training—vanilla DINOv2 achieves only 44% on CORE text-guided retrieval, but with lightweight gated cross-attention conditioning, it reaches 96%. This 52-point gap shows that frozen pretrained models have far more capability than their original objectives exercise.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.02327]] | backbone model | DINOv2 is the frozen ViT whose latent steerability SteerViT unlocks |

## Connections

- [[topics/computer-vision]] — DINOv2 is a foundational pretrained vision model
- [[topics/representation-learning]] — SteerViT demonstrates that frozen representations have untapped capabilities
