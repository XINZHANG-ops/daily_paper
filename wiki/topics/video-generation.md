---
title: "Video Generation"
slug: video-generation
paper_count: 3
last_updated: 2026-04-14
---

# Video Generation

## Overview

Video generation research addresses both numerical precision in representing specified content and expressive character animation. Three papers now span the spectrum: NUMINA's training-free attention-based instance counting, LPM 1.0's full-duplex conversational character animation, and OmniShow's unified multimodal human-object interaction video generation.

NUMINA identifies a critical limitation in text-to-video diffusion models: inability to accurately represent object counts specified in prompts. The root causes are semantic weakness (numerical tokens exhibit diffuse cross-attention responses compared to nouns, verbs, and adjectives) and instance ambiguity (heavily downsampled spatiotemporal latent space in DiT architectures limits separability of individual object representations). The key insight is that discriminative attention heads expose critical visual information about instance counts, and this can be exploited through a training-free identify-then-guide paradigm.

LPM 1.0 addresses the "performance trilemma" in video-based character animation: simultaneously achieving expressive quality, real-time inference, and long-horizon identity stability. The key insight is that conversation is the most comprehensive performance scenario—characters must simultaneously speak, listen, react, and emote while maintaining identity over time.

OmniShow introduces the first unified framework for Human-Object Interaction Video Generation (HOIVG), supporting all four conditions (text, reference image, audio, pose) in an end-to-end model. Built on Waver 1.0 (12B MMDiT), it achieves state-of-the-art or highly competitive performance across R2V, RA2V, and RP2V settings while being the smallest 10B-scale model (12.3B params). The key innovations are Unified Channel-wise Conditioning for seamless modality injection, Gated Local-Context Attention for precise audio-visual synchronization, and Decoupled-Then-Joint Training via model merging for leveraging heterogeneous datasets.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08546]] When Numbers Speak: Aligning Textual Numerals and Visual Instances in T2V | 2026-04-08 | Training-free attention-based instance detection and layout-guided regeneration for numerical alignment in T2V; up to 7.4% accuracy improvement |
| [[2604.07823]] LPM 1.0: Video-based Character Performance Model | 2026-04-08 | Full-duplex conversational character animation with 17B base model and real-time 480P streaming; introduces listening behavior modeling |
| [[2604.11804]] OmniShow: Unifying Multimodal Conditions for HOIVG | 2026-04-14 | First unified HOIVG framework with text, reference image, audio, and pose; Unified Channel-wise Conditioning; Gated Local-Context Attention; 12.3B params, SOTA on R2V/RA2V/RP2V |

## Open Problems

- **Instance separation at high density**: Generating very dense instances (tens or hundreds) remains unexplored due to difficulty separating individual instances in heavily downsampled latent spaces.
- **Multi-person scenes**: LPM 1.0 currently focuses on single-person full-duplex conversation; extending to multi-person scenes and broader performance scenarios.
- **Perceptual grouping cues**: When attention heads focus excessively on the most salient parts of an object (e.g., animal heads) rather than their entirety, over-segmented layouts result.
- **Zero-shot character generalization**: LPM requires identity-aware reference images for best performance, limiting zero-shot generalization.

## Connections

- [[topics/image-generation]] — NUMINA's numerical alignment techniques apply across image and video generation
- [[topics/benchmarks]] — Video understanding benchmarks like Video-MME-v2 reveal capabilities that video generation models should eventually exhibit
- [[topics/multimodal-conditions]] — OmniShow's four-condition unification represents the cutting edge of multimodal control in video generation
- [[topics/human-object-interaction]] — OmniShow's HOIVG benchmark and method directly advance human-object interaction video generation