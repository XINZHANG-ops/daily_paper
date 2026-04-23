---
title: "Spatial Reasoning"
slug: spatial-reasoning
paper_count: 1
last_updated: 2026-04-18
---

# Spatial Reasoning

## Overview

Spatial reasoning addresses how AI systems understand and reason about 3D space, object relationships, and geometric properties. Key challenge: providing deterministic ground truth for spatial relationships.

## Evolution

Mid-April 2026, SpatialEvo (2604.14144) established spatial reasoning through deterministic geometric environments with self-evolution. The key insight was that model voting fails for spatial tasks—geometric ground truth must come from deterministic computation, not model consensus. This contrasts with earlier embodied AI papers that relied on model agreement as a proxy for correctness. SpatialEvo's GRPO-based self-evolution on deterministic scenes shows that structured spatial intelligence requires structured evaluation.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.14144]] SpatialEvo | 2026-04-16 | Deterministic geometric environments for self-evolving spatial intelligence |

## Patterns & Insights

- **Model voting fails**: Geometric ground truth must come from deterministic computation, not model consensus
- **3D understanding builds on 2D**: Spatial reasoning extends planar vision

## Connections

- [[topics/3d-detection]] — Spatial reasoning builds on 3D detection
- [[topics/embodied-ai]] — Embodied agents need spatial reasoning
- [[entities/grpo]] — Used in SpatialEvo's self-evolution approach