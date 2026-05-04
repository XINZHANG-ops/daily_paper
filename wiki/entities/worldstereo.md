---
title: "WorldStereo 2.0"
slug: worldstereo
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# WorldStereo 2.0

## What It Is

WorldStereo 2.0 is the world expansion component of HY-World 2.0 that extends the scene from sparse views to dense coverage. Operating in **keyframe latent space**, it performs stereo matching to generate new viewpoints between existing keyframes, progressively filling in unseen angles.

The key challenge is cross-keyframe consistency: when generating a new viewpoint between two existing keyframes, the generated content must be geometrically consistent with both. WorldStereo 2.0 addresses this with two memory mechanisms:
- **Global-Geometric Memory**: maintains the overall 3D structure of the scene, ensuring new viewpoints respect the global geometry
- **Spatial-Stereo Memory++**: tracks fine-grained correspondences between adjacent keyframes, ensuring local texture and detail consistency

Together these enable coherent expansion—the world grows denser without accumulating geometric drift or texture artifacts. This stage produces the complete set of stereo views that WorldMirror 2.0 then composites into the final 3DGS scene.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | stage 3 | Keyframe latent space stereo matching with Global-Geometric Memory and Spatial-Stereo Memory++ for consistent expansion |

## Connections

- [[entities/hy-world-2]] — WorldStereo 2.0 is the third stage of the HY-World 2.0 pipeline; it takes WorldNav's planned trajectories and expands the views before WorldMirror composites them
- [[entities/worldmirror]] — WorldStereo 2.0 produces the expanded views that WorldMirror 2.0's normalized position encoding transforms into flexible-resolution 3DGS assets
- [[entities/worldnav]] — WorldNav determines which trajectories to follow; WorldStereo generates the views along those trajectories
- [[topics/computer-vision]] — Stereo matching in latent space with memory mechanisms represents an advance in consistent multi-view reconstruction