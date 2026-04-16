---
title: "BAGEL"
slug: bagel
type: model
paper_count: 2
last_updated: 2026-04-16
---

# BAGEL

## What It Is

BAGEL is a unified multimodal model that combines autoregressive text modeling with diffusion-based image generation. It serves as the base model for process-driven image generation in [[2604.04746]]. However, [[2604.10949]] reveals that BAGEL suffers from pseudo-unification—text generation shows high-entropy creativity while image synthesis enforces low-entropy fidelity.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04746]] | base model | Used for process-driven image generation with Plan→Sketch→Inspect→Refine cycles |
| [[2604.10949]] | analyzed model | Revealed to have modality-asymmetric encoding causing pseudo-unification |

## Connections

- [[topics/multimodal-models]] — BAGEL is a key unified multimodal model
- [[entities/harmon]] — Harmon is the only model achieving true unification, unlike BAGEL
- [[topics/image-generation]] — BAGEL used for image generation tasks