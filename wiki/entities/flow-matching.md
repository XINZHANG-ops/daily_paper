---
title: "Flow Matching"
slug: flow-matching
type: algorithm
paper_count: 2
last_updated: 2026-04-21
---

# Flow Matching

## What It Is

Flow Matching is a generative modeling framework that learns a transformation (flow map) between a base distribution and the target data distribution. Unlike diffusion models that operate through a stochastic denoising process, Flow Matching uses deterministic ordinary differential equations to map samples. MeanFlow is a variant that learns average velocity instead of instantaneous velocity.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18168]] EMF | framework | EMF extends MeanFlow (a Flow Matching variant) from class-conditional to text-conditional generation |
| [[2604.18486]] OneVL | related | OneVL applies similar compression principles to latent CoT for VLA planning |

## Connections

- [[entities/meanflow]] — MeanFlow is a Flow Matching variant that learns average velocity (integrating over the full flow path) rather than instantaneous velocity at each timestep; this averaging makes training more stable and enables efficient one-step generation with fewer sampling steps than standard Flow Matching
- [[topics/image-generation]] — Flow Matching provides a deterministic (ODE-based) alternative to stochastic diffusion models (SDE-based) for image generation; the key tradeoff is that deterministic flows are more efficient at inference (fewer steps) but may produce less diverse samples than stochastic diffusion