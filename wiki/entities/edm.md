---
title: "EDM (Elucidating the Design Space of Diffusion Models)"
slug: edm
type: algorithm
paper_count: 1
last_updated: 2026-04-20
---

# EDM (Elucidating the Design Space of Diffusion Models)

## What It Is

EDM is a foundational framework for understanding the design space of diffusion probabilistic models (DPMs). It provides a unified analysis of how various design choices—noise schedule, network architecture, sampling parameters—affect the quality-speed trade-off in diffusion-based image generation. The SNR-t bias paper (2604.16044) extends EDM's analysis by revealing a fundamental bias in the inference process that EDM's design space did not account for.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.16044]] | baseline | EDM serves as the baseline model for SNR-t bias experiments; DCW significantly improves upon EDM |

## Connections

- [[entities/dcw]] — DCW provides a training-free correction for SNR-t bias that improves EDM's FID from 10.66 to 5.67 on CIFAR-10
- [[entities/flux]] — FLUX uses an EDM-inspired architecture with additional modifications
- [[topics/image-generation]] — EDM's framework for understanding diffusion model design space is foundational to all modern image generation approaches