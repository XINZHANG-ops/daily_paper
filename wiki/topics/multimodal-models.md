---
title: "Multimodal Models"
slug: multimodal-models
paper_count: 1
last_updated: 2026-04-14
---

# Multimodal Models

## Overview

Unified Multimodal Models (UMMs) aim to synergize the creative reasoning of LLMs with the fidelity-driven generation of vision models, enabling both text generation and image synthesis within a single architecture. However, Pseudo-Unification (2604.10949) reveals a fundamental limitation: despite shared parameters, UMMs exhibit divergent response behaviors where text generation shows high-entropy creativity while image synthesis enforces low-entropy fidelity. This stems from two sources of divergence: modality-asymmetric encoding (vision and language follow divergent entropy trajectories shaped by architectural priors) and pattern-split response (text follows high-entropy creative pattern while image synthesis adheres to low-entropy fidelity regime). Only models that unify both encoding and generative logic (e.g., via contextual prediction) achieve genuine unification—Harmon (1.5B) actually outperforms BAGEL (14B) in cross-modal reasoning due to consistent information flow across modalities.

The field spans two architectural categories: (1) Native UMMs that unify text and image generation within a single architecture (e.g., Harmon, Janus-Pro, Show-o2 using all-in-one Transformers or Mixture-of-Transformers), and (2) MLLM + Diffusion Pipelines where a multimodal LLM generates text-based conditions and delegates image synthesis to a separate diffusion model (e.g., OmniGen2).

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.10949]] Pseudo-Unification: Entropy Probing | 2026-04-14 | Information-theoretic probing framework revealing pseudo-unification via dual divergence (modality-asymmetric encoding + pattern-split response); Harmon (1.5B) outperforms BAGEL (14B) via contextual prediction |

## Open Problems

- **True unification architectures**: What architectural modifications can achieve consistent information flow across modalities without relying on contextual prediction?
- **Scaling laws for unification**: Does the efficiency advantage of contextual prediction (Harmon vs BAGEL) hold at larger model scales?
- **Beyond text-image**: Extending unified probing to video generation, 3D synthesis, and other multimodal generation tasks
- **Training objectives**: Can training objectives be designed to encourage unified rather than split information flow?

## Connections

- [[topics/vision-language-models]] — VLMs provide the visual understanding backbone for UMMs; Pseudo-Unification analyzes why shared VLMs don't guarantee unified generation
- [[topics/multimodal-reasoning]] — Both address multimodal joint reasoning; multimodal-reasoning focuses on understanding while multimodal-models focuses on unified generation
- [[topics/video-generation]] — OmniShow extends unified multimodal conditioning to video generation with text, reference images, audio, and pose