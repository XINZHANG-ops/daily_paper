---
title: "FLUX"
slug: flux
type: model
paper_count: 1
last_updated: 2026-04-20
---

# FLUX

## What It Is

FLUX is a flagship text-to-image diffusion model known for its high-quality generation. The SNR-t bias paper (2604.16044) shows that DCW (Differential Correction in Wavelet domain) significantly improves FLUX's generation quality by correcting the SNR-timestep misalignment during inference. With DCW, FLUX achieves noticeable reduction in artifacts like over-smoothing and over-exposure.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.16044]] | evaluation target | FLUX + DCW demonstrates the practical value of SNR-t bias correction on a production-grade model |

## Connections

- [[entities/edm]] — FLUX builds upon EDM's architectural principles
- [[entities/dcw]] — DCW is applied to FLUX as a post-processing correction step, improving visual quality
- [[topics/image-generation]] — FLUX represents the state-of-the-art in text-to-image generation; DCW provides a universal improvement applicable to FLUX and similar models