---
title: "Video Generation"
slug: video-generation
paper_count: 2
last_updated: 2026-04-10
---

# Video Generation

## Overview

Video generation research is tackling both numerical precision and expressive character performance. Two papers from this period address complementary challenges: accurate instance counting in text-to-video models, and high-quality character animation with real-time inference.

NUMINA identifies a critical limitation in text-to-video diffusion models: inability to accurately represent object counts specified in prompts. The root causes are semantic weakness (numerical tokens exhibit diffuse cross-attention responses compared to nouns, verbs, and adjectives) and instance ambiguity (heavily downsampled spatiotemporal latent space in DiT architectures limits separability of individual object representations). The key insight is that discriminative attention heads expose critical visual information about instance counts, and this can be exploited through a training-free identify-then-guide paradigm. The two-phase approach first selects instance-discriminative self-attention heads and text-concentrated cross-attention heads at a reference timestep, constructs a countable layout by fusing attention maps and comparing estimated cardinality against prompted numerals, then refines the layout conservatively (adding or removing objects while preserving spatial relationships) and modulates cross-attention through bias adjustments to guide regeneration. This approach achieves up to 7.4% counting accuracy improvement across Wan2.1-1.3B, 5B, and 14B models while maintaining or improving temporal consistency and CLIP alignment.

LPM 1.0 addresses the "performance trilemma" in video-based character animation: simultaneously achieving expressive quality, real-time inference, and long-horizon identity stability. The key insight is that conversation is the most comprehensive performance scenario—characters must simultaneously speak, listen, react, and emote while maintaining identity over time. The full-stack framework spans a curated multimodal dataset, a 17B-parameter Diffusion Transformer base model, and a distilled causal streaming generator for real-time deployment. The three core innovations are: (1) large-scale human-centric multimodal dataset with speaking-listening audio-video pairing and identity-aware multi-reference extraction; (2) 17B Base LPM trained on over 1.7 trillion multimodal tokens with interleaved speak/listen audio injection; (3) four-stage autoregressive distillation curriculum converting the base model into Online LPM for real-time, infinite-length synthesis. Notably, this introduces listening behavior modeling—previous systems focus only on speech-driven talking heads, neglecting attentive gaze, reactive expressions, and turn-taking cues. Human evaluations show Base LPM (720P) preferred over Kling-Avatar-2 (64.3%) and OmniHuman-1.5 (42.5%), while Online LPM (480P) preferred over LiveAvatar (82.5%) and SoulX (64.1%).

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08546]] When Numbers Speak: Aligning Textual Numerals and Visual Instances in T2V | 2026-04-08 | Training-free attention-based instance detection and layout-guided regeneration for numerical alignment in T2V; up to 7.4% accuracy improvement |
| [[2604.07823]] LPM 1.0: Video-based Character Performance Model | 2026-04-08 | Full-duplex conversational character animation with 17B base model and real-time 480P streaming; introduces listening behavior modeling |

## Open Problems

- **Instance separation at high density**: Generating very dense instances (tens or hundreds) remains unexplored due to difficulty separating individual instances in heavily downsampled latent spaces.
- **Multi-person scenes**: LPM 1.0 currently focuses on single-person full-duplex conversation; extending to multi-person scenes and broader performance scenarios.
- **Perceptual grouping cues**: When attention heads focus excessively on the most salient parts of an object (e.g., animal heads) rather than their entirety, over-segmented layouts result.
- **Zero-shot character generalization**: LPM requires identity-aware reference images for best performance, limiting zero-shot generalization.

## Connections

- [[topics/image-generation]] — NUMINA's numerical alignment techniques apply across image and video generation
- [[topics/benchmarks]] — Video understanding benchmarks like Video-MME-v2 reveal capabilities that video generation models should eventually exhibit