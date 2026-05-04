---
title: "WorldNav"
slug: worldnav
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# WorldNav

## What It Is

WorldNav is the trajectory planning component of HY-World 2.0. It uses five heuristic modes for semantic-aware trajectory planning:
- Surrounding Trajectories
- Reconstruct-Aware Trajectories
- Depth-Aware Trajectories
- Structure-Aware Trajectories
- Hybrid Trajectories

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | stage 2 | WorldNav handles trajectory planning to ensure optimal scene coverage |

## Connections

- [[entities/hy-world-2]] — WorldNav is the second stage of the HY-World 2.0 four-stage pipeline; its five heuristic modes determine which trajectories the system follows, directly affecting the quality of downstream stereo expansion (WorldStereo 2.0) and final composition (WorldMirror 2.0)
- [[entities/hy-pano]] — WorldNav takes HY-Pano's panorama output as its starting point and plans the optimal exploration path across the scene
- [[entities/worldstereo]] — WorldStereo 2.0 executes the trajectories that WorldNav plans; poor trajectory planning directly degrades stereo consistency
- [[topics/embodied-ai]] — Trajectory planning for scene exploration is a core capability for embodied agents navigating previously unseen 3D environments