---
title: "Global State Encoder (GSE)"
slug: gse
type: algorithm
paper_count: 1
last_updated: 2026-04-21
---

# Global State Encoder (GSE)

## What It Is

GSE is the component in MultiWorld that ensures coherent observations across different camera views by extracting a 3D-aware global environment state from multiple viewpoints. It uses a frozen VGGT (Visual Geometry Grounded Transformer) backbone to encode multi-view observations into a compact latent representation that preserves 3D spatial relationships.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18564]] MultiWorld | core architecture | VGGT extracts 3D-aware latents from multiple views; MLP aligns dimensions with DiT backbone; enables consistent multi-view video generation |

## Connections

- [[2604.18564]] — GSE is the second key innovation (alongside MACM) in MultiWorld; it solves the multi-view consistency problem by leveraging 3D geometry from VGGT
- [[entities/vggt]] — VGGT provides the 3D reconstruction foundation that GSE leverages for multi-view consistency
- [[topics/world-models]] — GSE enables world models to maintain geometric consistency across views—a prerequisite for true shared environment simulation
