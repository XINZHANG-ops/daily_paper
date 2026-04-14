---
title: "Character Animation"
slug: character-animation
paper_count: 1
last_updated: 2026-04-13
---

# Character Animation

## Overview

Video-based character animation aims to generate realistic human performance—simultaneously speaking, listening, reacting, and maintaining identity over time—from video inputs. The task faces a "performance trilemma": simultaneously achieving expressive quality, real-time inference, and long-horizon identity stability. Previous work has focused on speech-driven talking heads, treating character animation as a单向 generation problem where an audio signal drives facial and body movement. This approach misses the critical role of listening behavior—the way characters attend, react, and express emotion when not actively speaking—which is central to natural human interaction.

LPM 1.0 (2604.07823) introduces a full-stack framework spanning dataset, base model, and distilled online model. The key insight is that conversation is the most comprehensive performance scenario—characters must simultaneously speak, listen, react, and emote while maintaining identity over time. The system builds on three core innovations: a large-scale human-centric multimodal dataset with speaking-listening audio-video pairing and identity-aware multi-reference extraction (23M speaker clips, 5M conversation/listen clips after aggressive quality filtering); a 17B Base LPM trained on over 1.7 trillion multimodal tokens with interleaved speak/listen audio injection (speaking audio conditions even-numbered cross-attention layers, listening audio conditions odd-numbered layers); and a four-stage autoregressive distillation curriculum that converts the base model into Online LPM—a causal backbone-refiner streaming generator for real-time, infinite-length synthesis.

The dataset construction pipeline processes diverse long-form videos through scene detection, quality filtering (removing post-processing artifacts, blur, overlays), conversation detection with LR-ASD fine-tuned for three-state frame-level classification (speak/listen/idle), and captioning. A semantic verification stage using fine-tuned Qwen3-Omni filters false positives, achieving 78.37 F1. Human preference evaluations show Base LPM (720P) preferred over Kling-Avatar-2 (64.3%) and OmniHuman-1.5 (42.5%), while Online LPM (480P) is preferred over LiveAvatar (82.5%) and SoulX (64.1%). Notably, at matched resolution, human raters judge Base LPM and Online LPM indistinguishable in 42-88% of cases—demonstrating that real-time causal generation need not sacrifice perceived realism.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.07823]] LPM 1.0: Video-based Character Performance Model | 2026-04-08 | Full-duplex conversational modeling with listening behavior; 17B Base LPM with 1.7T multimodal tokens; four-stage AR distillation to real-time Online LPM; LPM-Bench with 1,000 test cases |

## Open Problems

- Extending to multi-person scenes where characters interact with each other, not just with the viewer
- Broader performance scenarios beyond conversation—gestures, expressions, full-body movement
- Zero-shot character generalization without identity-aware reference images
- Tradeoff optimization between visual resolution and real-time constraints
- The relationship between listening behavior quality and overall perceived realism requires deeper analysis

## Connections

- [[topics/video-generation]] — LPM 1.0 builds on diffusion transformer advances for video synthesis; the 17B base model uses architecture similar to image-to-video foundation models
- [[topics/3d-detection]] — Both papers address spatial understanding; WildDet3D focuses on object detection in 3D while LPM addresses character performance which requires understanding 3D body pose and spatial context