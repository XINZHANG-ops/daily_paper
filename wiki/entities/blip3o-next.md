---
title: "BLIP3o-NEXT"
slug: blip3o-next
type: model
paper_count: 1
last_updated: 2026-04-21
---

# BLIP3o-NEXT

## What It Is

BLIP3o-NEXT is a native image generation model that uses a powerful LLM-based text encoder validated to possess high discriminability and disentanglement properties—two key properties required for effective few-step MeanFlow generation. As shown in EMF (Extending MeanFlow to T2I), BLIP3o-NEXT's text encoder consistently outperforms other encoders (SANA-1.5, CLIP, T5) on both discriminability (0.734 vs others) and disentanglement (0.999) metrics. These properties reduce the semantic discrimination burden under limited denoising steps.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18168]] EMF | base model | BLIP3o-NEXT serves as the base model and text encoder for EMF's few-step MeanFlow adaptation; achieves GenEval 0.90 with 4 steps |

## Connections

- [[entities/meanflow]] — BLIP3o-NEXT's text encoder properties enable effective MeanFlow adaptation for few-step generation
- [[entities/geneval]] — GenEval is the primary benchmark for evaluating BLIP3o-NEXT's image generation quality
- [[topics/image-generation]] — BLIP3o-NEXT is a state-of-the-art text-to-image generation model
- [[topics/multimodal-models]] — BLIP3o-NEXT bridges language understanding with visual generation
