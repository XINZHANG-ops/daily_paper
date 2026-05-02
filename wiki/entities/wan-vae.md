---
title: "Wan VAE"
slug: wan-vae
type: model
paper_count: 1
last_updated: 2026-04-21
---

# Wan VAE

## What It Is

Wan VAE is the video VAE backbone used by MultiWorld for encoding video content into latent representations. MultiWorld's experiments show that VGGT significantly outperforms Wan VAE as the backbone for the Global State Encoder (GSE) module, suggesting that 3D-aware visual features are more valuable than 2D video features for multi-view world modeling.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18564]] MultiWorld | backbone | Wan VAE serves as the baseline video encoder in MultiWorld's ablation study; VGGT outperforms it for 3D-aware encoding |

## Connections

- [[entities/vggt]] — VGGT outperforms Wan VAE for multi-view consistency; MultiWorld uses VGGT as the GSE backbone
- [[entities/multiworld]] — MultiWorld compares Wan VAE vs VGGT and selects VGGT as the superior backbone
- [[topics/video-generation]] — Wan VAE is part of the video generation pipeline; MultiWorld shows that the choice of video encoder significantly impacts world model quality