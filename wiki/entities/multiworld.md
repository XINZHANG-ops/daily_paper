---
title: "MultiWorld"
slug: multiworld
type: model
paper_count: 1
last_updated: 2026-04-21
---

# MultiWorld

## What It Is

MultiWorld is a scalable multi-agent multi-view video world model that generates consistent videos from multiple camera views given actions from multiple agents. It addresses three key challenges: multi-agent controllability (associating actions with specific agents), multi-view consistency (geometric coherence across viewpoints), and framework scalability (variable agent/camera counts).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18564]] MultiWorld | core method | Uses MACM for multi-agent control and GSE (VGGT backbone) for 3D-aware global state; achieves FVD=179, Action=89.8%, RPE=0.67 |

## Connections

- [[2604.18564]] — The primary model; introduces MACM and GSE as key architectural innovations for multi-agent world modeling
- [[entities/wan-vae]] — The base video diffusion backbone used by MultiWorld
- [[entities/vggt]] — VGGT provides the 3D-aware global state encoding in the GSE module
- [[topics/world-models]] — MultiWorld extends world models to multi-agent settings with shared environment simulation
- [[topics/video-generation]] — MultiWorld conditions video generation on multi-agent actions, extending interactive video generation to multi-player scenarios
