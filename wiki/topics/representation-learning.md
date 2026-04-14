---
title: "Representation Learning"
slug: representation-learning
paper_count: 1
last_updated: 2026-04-14
---

# Representation Learning

## Overview

Representation learning studies how neural networks encode, compress, and transform information into latent representations suitable for downstream tasks. The field has evolved from geometric properties (anisotropy, effective rank, curvature) and task-based metrics (InfoNCE, LiDAR, NESum) toward information-theoretic measures that capture the intrinsic uncertainty and information content of representations. Pseudo-Unification (2604.10949) represents a significant methodological advance by reformulating entropy computation in Reproducing Kernel Hilbert Spaces (RKHS), enabling entropy estimation for high-dimensional, variable-length embedding sequences without requiring explicit probability densities.

The key innovation is treating embedding sequences as empirical samples, modeling their similarity via Gaussian kernels, and interpreting entropy not as a function of probability density but as a geometric property of representation structure. This allows matrix-based Rényi entropy to quantify the intrinsic uncertainty (isotropy and spread) of embeddings, while conditional entropy proxy measures residual output uncertainty given the input. This framework bridges the gap between semantic geometry analysis (layer-wise representations in LLMs) and mechanistic understanding of multimodal unification.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.10949]] Pseudo-Unification: Entropy Probing | 2026-04-14 | Matrix-based Rényi entropy in RKHS for probing UMMs; dual-level framework (prompt entropy + response conditional entropy) for diagnosing unification |

## Open Problems

- **Theoretical foundations**: The entropy proxy is empirically validated but lacks formal Shannon-entropy guarantees
- **Cross-modal representations**: Extending RKHS entropy analysis to audio, video, and other modalities beyond text and images
- **Temporal dynamics**: How do representations evolve during generation (e.g., across diffusion timesteps or autoregressive steps)?
- **Representation compression**: The relationship between layer-wise entropy trajectories and model compression/sparsification

## Connections

- [[topics/vision-language-models]] — SteerViT's steerability analysis connects to representation geometry; language conditioning preserves visual representation quality while adding steerability
- [[topics/multimodal-models]] — Pseudo-Unification directly analyzes how multimodal models encode information differently across modalities
- [[topics/reasoning]] — Representation quality affects reasoning chains; entropy trajectories may reveal where reasoning happens in transformer layers