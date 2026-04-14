---
title: "Style Transfer"
slug: style-transfer
paper_count: 1
last_updated: 2026-04-10
---

# Style Transfer

## Overview

Style transfer research aims to separate and recombine the content and style of images, enabling artistic reinterpretation of photographs or transfer of artistic styles between images. A fundamental challenge has been constructing training datasets with intra-style consistent and inter-style diverse image pairs—the difficulty of collecting paired supervision where two images share the same style but differ in content stems from the fact that style is multi-dimensional and highly discriminative, with minor changes in creation producing perceptually different styles. Previous datasets relied on SOTA style transfer methods to generate style-consistent pairs, which produced limited style spaces, inconsistent intra-style pairs, and visible artifacts from models that themselves suffered from content leakage.

MegaStyle (2604.08364) introduces a paradigm shift by leveraging the consistent text-to-image style mapping capability of large generative models like Qwen-Image. Rather than generating style pairs via style transfer models, the approach generates images from style descriptions paired with diverse content prompts—the same style prompt produces images sharing that artistic style while containing different subject matter. This enables constructing datasets with 8,355 fine-grained artistic styles and 1.4M style images, vastly surpassing previous datasets in both scale and diversity.

The data curation pipeline has three stages: image pool collection builds content and style image pools from diverse sources (JourneyDB for Midjourney styles, WikiArt for painting styles, LAION-Aesthetics for non-stylized content); prompt curation uses Qwen3-VL for style and content captioning with specialized instructions for different aspects (objects and visual relationships for content, color composition and brushwork for style) and applies four-level hierarchical k-means clustering with mpnet embeddings for balanced sampling; style image generation pairs each style prompt with N content prompts using Qwen-Image with FlowMatchScheduler. The Style-Supervised Contrastive Learning (SSCL) objective combines supervised contrastive learning with SigLIP image-text contrastive loss, while MegaStyle-FLUX uses shifted RoPE on reference style tokens to prevent positional collision and content leakage.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08364]] MegaStyle: Constructing Diverse and Scalable Style Dataset | 2026-04-08 | Scalable data curation via consistent T2I style mapping; MegaStyle-1.4M with 8,355 styles; SSCL training objective; MegaStyle-FLUX achieving 76.16 style score on StyleBench |

## Open Problems

- VLM captioning produces vague descriptions for texture, brushwork, and medium elements—instruction prompts could be refined to better cover visual aspects
- Qwen-Image shows association bias toward certain styles (e.g., Japanese painting generating historical Japanese figures), limiting diversity
- Scaling to 10-million level datasets remains a goal but requires addressing generation consistency at that scale
- The relationship between style granularity and downstream style transfer quality requires further investigation

## Connections

- [[topics/image-generation]] — MegaStyle builds on T2I generation capabilities (Qwen-Image, FLUX) and serves as training data for style transfer models