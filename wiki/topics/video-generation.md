---
title: "Video Generation"
slug: video-generation
paper_count: 6
last_updated: 2026-04-21
---

# Video Generation

## Overview

Video generation has advanced to include not just visual quality but temporal coherence, physics plausibility, audio synchronization, and controllable generation through multiple modalities. The papers reveal that the next frontier is **interactive video generation** where users can control aspects like character behavior, object counting, and audio synchronization.

The key theme is that **controllable video generation requires unified multimodal conditioning**—text, image, audio, and pose must be processed jointly, not sequentially.

## Evolution

In early April 2026, NUMINA showed that counting accuracy in video is achievable through attention head analysis. By mid-April, OmniShow demonstrated unified conditioning for human-object interaction video generation. Seedance 2.0 pushed the frontier on motion quality and audio-visual synchronization, achieving state-of-the-art across T2V, I2V, and R2V tasks. LPM 1.0 focused on character animation with speaking/listening capabilities. On April 21, MultiWorld extended video generation to multi-agent scenarios with shared environment simulation—multiple agents acting in coordinated ways across different viewpoints.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08546]] NUMINA | 2026-04-10 | Training-free counting alignment in T2V |
| [[2604.07823]] LPM 1.0 | 2026-04-13 | Character performance with interleaved audio |
| [[2604.11804]] OmniShow | 2026-04-14 | HOIVG with unified multimodal conditions |
| [[2604.14148]] Seedance 2.0 | 2026-04-16 | State-of-the-art T2V/I2V/R2V with audio |
| [[2604.14268]] HY-World 2.0 | 2026-04-17 | Unified 3D world reconstruction and generation with video |
| [[2604.18564]] MultiWorld | 2026-04-21 | Multi-agent multi-view world model for coordinated multi-player video and robot manipulation |

## Patterns & Insights

- **Audio is becoming standard**: Videos are expected to include synchronized audio
- **Counting accuracy matters**: Objects should appear as specified, not just look good
- **Character animation is specialized**: Different from general video—focus on identity, expression, listening

## Open Problems

- Real-time video generation with all modality controls
- Long-form video coherence (current models struggle beyond 10+ seconds)
- Physics simulation in generated video

## Connections

- [[topics/image-generation]] — Video extends image generation temporally
- [[topics/human-object-interaction]] — OmniShow addresses HOIVG specifically
- [[entities/waver-1-0]] — Base model for OmniShow's video generation