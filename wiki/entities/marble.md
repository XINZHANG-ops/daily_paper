---
title: "Marble"
slug: marble
type: model
paper_count: 1
last_updated: 2026-04-17
---

# Marble

## What It Is

Marble is a closed-source world model that serves as the key quality benchmark for HY-World 2.0. While its internal architecture and training details are not publicly disclosed, HY-World 2.0 uses it as the comparison target because Marble represents the state of the art in generative world models for 3D scene reconstruction and simulation.

HY-World 2.0 achieves results comparable to Marble across text-to-panorama, image-to-panorama, and multi-view reconstruction tasks while being fully open-source. This is significant because it demonstrates that the quality gap between open and closed world models is closing, similar to the trend observed in LLMs. Marble's role in the wiki is as a reference point: it anchors the "what is currently possible" for world model quality.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14268]] | comparison | HY-World 2.0 quality comparable to this closed-source model; open-source SOTA catches closed-source quality |

## Connections

- [[entities/hy-world-2]] — HY-World 2.0 closes the open/closed quality gap by matching Marble's performance
- [[topics/world-models]] — Marble represents the closed-source frontier in world models; HY-World 2.0's matching performance marks a shift toward open dominance in this domain