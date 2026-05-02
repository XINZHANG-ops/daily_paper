---
title: "3D Detection"
slug: 3d-detection
paper_count: 1
last_updated: 2026-04-18
---

# 3D Detection

## Overview

3D detection extends computer vision from 2D image understanding to spatial scene interpretation. Papers in this wiki focus on open-vocabulary 3D detection and scaling to real-world complexity.

## Evolution

Mid-April 2026, two papers established complementary approaches to 3D detection. WildDet3D (2604.08626) tackled open-vocabulary detection at scale, achieving 138× more categories than previous methods through language-guided localization. Three days later, SpatialEvo (2604.14144) approached spatial understanding through deterministic self-evolution, emphasizing that model voting fails for geometric ground truth—only deterministic computation provides reliable spatial priors. Together they show that 3D detection is evolving from category-based recognition toward open-world spatial understanding with geometric grounding.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08626]] WildDet3D | 2026-04-13 | Open-vocabulary 3D detection at scale (138× more categories) |

## Patterns & Insights

- **Geometric ground truth is deterministic**: Unlike other ML domains where model voting works, 3D detection benefits from deterministic computation—point clouds and camera poses provide objective spatial ground truth
- **Open-vocabulary over fixed-category**: The 138× improvement from WildDet3D shows that scaling detection to real-world vocabulary matters more than refining fixed categories
- **Embodied agents need 3D understanding**: Both papers connect to embodied AI, suggesting spatial detection is foundational for robotic systems

## Connections

- [[topics/computer-vision]] — 3D detection extends 2D vision to spatial understanding
- [[topics/spatial-reasoning]] — Spatial reasoning builds on 3D detection capabilities
- [[topics/embodied-ai]] — 3D detection is foundational for embodied agents