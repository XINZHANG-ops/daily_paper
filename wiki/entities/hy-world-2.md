---
title: "HY-World 2.0"
slug: hy-world-2
type: framework
paper_count: 1
last_updated: 2026-04-17
---

# HY-World 2.0

## What It Is

HY-World 2.0 is a multi-modal world model framework for reconstructing, generating, and simulating 3D worlds from diverse inputs (text prompts, single-view images, multi-view images, videos). It addresses the gap between 3D world generation (sparse inputs) and world reconstruction (dense multi-view inputs).

The framework employs a four-stage pipeline:
1. **HY-Pano 2.0**: Panorama generation with adaptive P2E transformation
2. **WorldNav**: Trajectory planning with five heuristic modes
3. **WorldStereo 2.0**: World expansion in keyframe latent space with consistent memory
4. **WorldMirror 2.0 + 3DGS**: World composition with flexible resolution inference

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | core method | Unified framework achieving open-source SOTA, comparable to closed-source Marble |

## Connections

- [[entities/hy-pano]] — HY-Pano 2.0 handles scene initialization
- [[entities/worldnav]] — WorldNav handles trajectory planning
- [[entities/worldstereo]] — WorldStereo 2.0 handles world expansion
- [[entities/worldmirror]] — WorldMirror 2.0 handles world composition
- [[entities/marble]] — Marble is the closed-source comparison model
- [[topics/world-models]] — HY-World 2.0 demonstrates the perception-interaction-memory triplet