---
title: "Image Generation"
slug: image-generation
paper_count: 3
last_updated: 2026-04-10
---

# Image Generation

## Overview

Image generation research is evolving beyond single-pass synthesis toward process-driven, controllable, and style-aware generation. Three papers from this period address fundamental challenges: process-driven generation with interleaved textual-visual reasoning, large-scale style dataset construction, and numerical alignment in video (which also illuminates image generation challenges).

Think in Strokes introduces process-driven image generation as a multi-step paradigm decomposing image synthesis into interleaved reasoning trajectories. Unlike traditional single-pass generation where a model commits to an entire scene in one forward pass, this approach unfolds across multiple iterations: Plan (generate incremental instruction and scene description), Sketch (synthesize partial visual draft), Inspect (identify inconsistencies between sketch and prompt), and Refine (emit correction if needed). The tight coupling between textual and visual reasoning is key: textual reasoning explicitly conditions how visual state should evolve, while the generated visual intermediate constrains and grounds the next round of textual reasoning. The two supervised signals are scene-graph subsampling (for logically ordered incremental instructions) and self-sampled critique traces (learning from the model's own error trajectories). Results show 8x reduction in training data and 7.6x inference cost reduction compared to PARM while achieving comparable or better performance to the 12B FLUX.1-dev model.

MegaStyle addresses the fundamental challenge of constructing large-scale, intra-style consistent, inter-style diverse style datasets for image style transfer. The core innovation leverages the consistent text-to-image style mapping capability of large generative models like Qwen-Image, which can generate images in the same style from a given style description with high fidelity. This overcomes limitations of previous datasets that relied on style transfer methods producing limited style spaces, inconsistent intra-style pairs, and visible artifacts. The pipeline curates 170K style prompts and 400K content prompts, generating up to 68B content-style combinations. From this, MegaStyle-1.4M containing 1.4M style images with 8,355 fine-grained artistic styles is constructed. The Style-Supervised Contrastive Learning (SSCL) objective combines supervised contrastive learning with SigLIP image-text contrastive loss, and MegaStyle-FLUX applies shifted RoPE on reference style tokens to prevent positional collision and content leakage.

NUMINA addresses numerical alignment in text-to-video but reveals insights applicable to image generation: discriminative attention heads expose critical visual information about object counts, and instance ambiguity in heavily downsampled latent spaces limits separability of individual object representations. The training-free identify-then-guide paradigm identifies misalignments via attention analysis and corrects them through layout-guided regeneration, achieving up to 7.4% counting accuracy improvement. While focused on video, these findings about attention-based instance detection and layout construction translate to image generation challenges with multiple objects.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04746]] Think in Strokes, Not Pixels: Process-Driven Image Generation via Interleaved Reasoning | 2026-04-07 | Four-stage process-driven generation (Plan→Sketch→Inspect→Refine) with 8x training data reduction and 7.6x inference cost reduction |
| [[2604.08364]] MegaStyle: Constructing Diverse and Scalable Style Dataset | 2026-04-08 | Scalable style dataset pipeline generating 68B combinations; 1.4M images with 8,355 fine-grained styles via consistent T2I style mapping |
| [[2604.08546]] When Numbers Speak: Aligning Textual Numerals and Visual Instances in T2V | 2026-04-08 | Attention-based instance detection and layout-guided regeneration for numerical alignment (training-free, applicable to images) |

## Open Problems

- **Process-driven generation for complex scenes**: The model autonomously determines trajectory length based on task difficulty, but this may not always align with desired output quality.
- **Style dataset caption quality**: VLMs may produce vague descriptions for texture, brushwork, and medium elements when instruction prompts don't specify target visual aspects.
- **Instance separation at high counts**: Generating very dense instances (tens or hundreds) remains unexplored due to difficulty separating individual instances in downsampled latent spaces.
- **Style association bias**: Qwen-Image shows association bias toward some styles (e.g., Japanese painting generating figures from specific historical periods).

## Connections

- [[topics/video-generation]] — Video generation models like LPM also face instance alignment challenges; NUMINA methods apply across modalities
- [[topics/image-generation]] — Style transfer techniques in MegaStyle connect to broader image generation research