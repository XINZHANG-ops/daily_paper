---
title: "SteerViT"
slug: steervit
type: model
paper_count: 1
last_updated: 2026-04-16
---

# SteerViT

## What It Is

SteerViT is a method for making frozen Vision Transformers steerable via natural language. It inserts lightweight gated cross-attention layers within frozen ViT blocks, conditioned on text via a pretrained RoBERTa encoder. Trained with a referential segmentation pretext task on 162k diverse images, it achieves a new Pareto frontier: 96% on CORE retrieval (vs 44% for vanilla DINOv2) while maintaining representation quality. Only ~21M trainable parameters are added.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.02327]] | introduced | SteerViT is the paper's main contribution |

## Connections

- [[topics/computer-vision]] — SteerViT enables controllable vision models without fine-tuning
- [[topics/representation-learning]] — Achieves new Pareto frontier between steerability and representation quality
