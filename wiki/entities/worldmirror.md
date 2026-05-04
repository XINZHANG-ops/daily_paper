---
title: "WorldMirror 2.0"
slug: worldmirror
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# WorldMirror 2.0

## What It Is

WorldMirror 2.0 is the world composition component of HY-World 2.0. Its key innovation is **normalized position encoding**, which enables flexible resolution inference without performance degradation. This solves a common problem in 3D Gaussian Splatting: when inference resolution differs from training resolution, naive position encodings cause artifacts. Normalized position encoding makes the encoding scale-invariant, so the model can generate at any resolution.

WorldMirror 2.0 combines this with 3D Gaussian Splatting (3DGS) and MaskGaussian to produce the final navigable 3D assets. MaskGaussian handles scene composition—when multiple panoramic views have been reconstructed, MaskGaussian determines which Gaussians contribute to each viewpoint, handling occlusion and overlap. The result is a complete, explorable 3D world produced in approximately 10 minutes end-to-end.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | stage 4 | Normalized position encoding for flexible resolution 3DGS; produces final navigable assets |

## Connections

- [[entities/hy-world-2]] — WorldMirror 2.0 is the final stage of the HY-World 2.0 pipeline, composing all reconstructed views into a unified navigable 3D world
- [[entities/worldstereo]] — WorldStereo 2.0 produces the expanded stereo views that WorldMirror 2.0 composites into the final 3DGS scene
- [[topics/computer-vision]] — Normalized position encoding for 3DGS is an advance in neural rendering that addresses a practical deployment constraint (resolution flexibility)