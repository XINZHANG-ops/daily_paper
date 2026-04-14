---
title: "Human-Object Interaction"
slug: human-object-interaction
paper_count: 1
last_updated: 2026-04-14
---

# Human-Object Interaction

## Overview

Human-Object Interaction (HOI) research focuses on understanding and generating realistic interactions between humans and objects in visual content. The task spans 3D reconstruction, motion sequence synthesis, and increasingly, video generation where human actors interact with objects in temporally coherent ways. OmniShow (2604.11804) extends this into video generation, synthesizing high-quality videos conditioned on text, reference images, audio, and pose—a practical but challenging task with applications in e-commerce, short video production, and interactive entertainment.

Previous HOI video generation approaches like AnchorCrafter, HunyuanVideo-HOMA, and DreamActor-H1 suffer from strict input requirements (mandatory object masks, trajectories, or body mesh templates) and cannot leverage audio cues, limiting their flexibility and generation quality. OmniShow's unified approach achieves superior reference consistency, audio-visual synchronization, and pose accuracy by harmonizing all four modality conditions in an end-to-end framework.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.11804]] OmniShow: Unifying Multimodal Conditions for HOIVG | 2026-04-14 | First unified HOIVG framework with text, reference image, audio, and pose; Unified Channel-wise Conditioning; Gated Local-Context Attention; Decoupled-Then-Joint Training |

## Open Problems

- **Complex interaction dynamics**: Generating realistic hand-object contact and object manipulation with proper physics
- **Multi-person scenes**: Current approaches focus on single-person interaction; multi-person HOI remains challenging
- **Audio-visual-physical coherence**: Ensuring audio speech matches lip movements, body poses align with object physics, and reference appearance is preserved
- **Long-form interaction**: Extending from 5-10 second clips to full scenes with sustained interactions

## Connections

- [[topics/video-generation]] — HOIVG is a specialized subdomain of video generation with specific multimodal conditioning requirements
- [[topics/multimodal-conditions]] — The four-condition unification (text, image, audio, pose) is the core technical challenge