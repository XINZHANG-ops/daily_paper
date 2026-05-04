---
title: "HY-Pano 2.0"
slug: hy-pano
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# HY-Pano 2.0

## What It Is

HY-Pano 2.0 is the panorama generation component of HY-World 2.0, performing **adaptive perspective-to-equirectangular (P2E) transformation** for scene initialization. Given sparse inputs (single image, text prompt, or multi-view), it generates a 360-degree equirectangular panorama as the foundation for subsequent world building.

The adaptive P2E transformation is the key innovation: unlike fixed-projection methods, HY-Pano 2.0 adapts its transformation parameters based on input geometry, producing panoramas that retain spatial consistency across different viewpoints. This is critical because the panorama quality directly determines downstream reconstruction quality—errors in the panorama propagate through the entire pipeline. It achieves SOTA among open-source methods for both text-to-panorama and image-to-panorama tasks.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | stage 1 | Adaptive P2E transformation for scene initialization; SOTA open-source panorama quality |

## Connections

- [[entities/hy-world-2]] — HY-Pano 2.0 is the first stage of the HY-World 2.0 four-stage pipeline; its panorama output initializes the scene for WorldNav trajectory planning and WorldStereo expansion
- [[entities/worldnav]] — WorldNav takes HY-Pano's panorama output and plans exploration trajectories
- [[topics/computer-vision]] — Panorama generation from sparse views is a longstanding CV challenge that HY-Pano advances via adaptive projection