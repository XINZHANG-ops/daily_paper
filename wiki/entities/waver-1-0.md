---
title: "Waver-1-0"
slug: waver-1-0
type: model
paper_count: 1
last_updated: 2026-04-18
---

# Waver-1-0

## What It Is

Waver-1-0 is a 12.3B parameter video generation model based on the **MMDiT (Multi-Modal Diffusion Transformer)** architecture with latent diffusion. It generates videos from text prompts in a compressed latent space, with the DiT backbone providing strong scalability for high-resolution generation.

OmniShow builds on Waver-1-0 as its base model, extending it from pure text-to-video to human-object interaction video generation (HOIVG). OmniShow adds three new capabilities on top of Waver-1-0: Unified Channel-wise Conditioning (injecting multimodal conditions via pseudo-frame tokens), Gated Local-Context Attention (for temporal alignment of audio), and Decoupled-Then-Joint Training (separate R2V/A2V training then joint fine-tuning). Waver-1-0 provides the generative backbone while OmniShow adds the conditioning infrastructure.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.11804]] OmniShow | base model | 12.3B MMDiT latent diffusion model serving as generative backbone for HOIVG |

## Connections

- [[topics/video-generation]] — Waver-1-0 is a text-to-video base model; OmniShow extends it to human-object interaction by adding multimodal conditioning
- [[topics/human-object-interaction]] — The base model is extended from general video generation to HOI-specific tasks through OmniShow's conditioning stack
- [[topics/multimodal-models]] — MMDiT-based architecture represents the integration of diffusion and transformer architectures for multimodal generation