---
title: "VGGT (Visual Geometry Grounded Transformer)"
slug: vggt
type: model
paper_count: 1
last_updated: 2026-04-21
---

# VGGT (Visual Geometry Grounded Transformer)

## What It Is

VGGT is a pretrained end-to-end 3D reconstruction foundation model. In MultiWorld, a frozen VGGT backbone is used as the Global State Encoder (GSE) to extract 3D-aware latent representations from multiple camera views, enabling geometrically consistent multi-view video generation.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18564]] MultiWorld | 3D backbone | Frozen VGGT provides 3D geometry priors for GSE; outperforms Wan VAE and DINOv2 for multi-view consistency |

## Connections

- [[2604.18564]] — VGGT is the backbone of the Global State Encoder; its 3D reconstruction capabilities are essential for MultiWorld's multi-view consistency
- [[entities/gse]] — GSE uses VGGT as its frozen backbone to encode multi-view observations into 3D-aware global state
- [[topics/computer-vision]] — VGGT represents the state-of-the-art in visual geometry understanding; its pretrained 3D priors transfer effectively to video world modeling
