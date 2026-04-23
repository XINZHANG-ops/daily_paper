---
title: "MeanFlow"
slug: meanflow
type: algorithm
paper_count: 2
last_updated: 2026-04-21
---

# MeanFlow

## What It Is

MeanFlow is a principled flow matching framework for one-step generative modeling that learns a flow map between two time steps, enabling efficient single-step generation by predicting average velocity rather than instantaneous velocity. Unlike standard Flow Matching that models per-step instantaneous velocity, MeanFlow rigorously derives the relation between average and instantaneous velocities and designs a theoretically grounded training objective. MeanFlow achieves one-step generation performance comparable to standard multi-step models.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18168]] EMF | core method | EMF extends MeanFlow from class-conditional to text-conditional generation by identifying discriminability and disentanglement as key text representation properties |
| [[2604.18486]] OneVL | related concept | OneVL applies similar compression principles to latent CoT for VLA planning; both achieve single-pass inference through learned average representations |

## Connections

- [[entities/flow-matching]] — MeanFlow is a variant of Flow Matching that learns average velocity instead of instantaneous velocity
- [[entities/latent-cot]] — OneVL's latent CoT draws from MeanFlow's compression principle
- [[topics/image-generation]] — MeanFlow enables few-step and one-step image generation
- [[topics/computer-vision]] — MeanFlow has been applied to image synthesis tasks
