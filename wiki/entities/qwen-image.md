---
title: "Qwen-Image"
slug: qwen-image
type: model
paper_count: 1
last_updated: 2026-04-16
---

# Qwen-Image

## What It Is

Qwen-Image is a text-to-image model with consistent style mapping capability. It's the key technology enabling MegaStyle's dataset construction—its consistent T2I style mapping allows generating images in the same style from a given style description, which is crucial for creating intra-style consistent training pairs.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.08364]] | data generation | Used to generate MegaStyle-1.4M with consistent intra-style pairs |

## Connections

- [[topics/image-generation]] — Qwen-Image's consistent style mapping enables quality style datasets
- [[entities/qwen3-vl]] — Related model used for captioning in MegaStyle pipeline