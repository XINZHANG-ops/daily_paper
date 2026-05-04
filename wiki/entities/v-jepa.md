---
title: "V-JEPA"
slug: v-jepa
type: model
paper_count: 1
last_updated: 2026-04-18
---

# V-JEPA

## What It Is

V-JEPA (Video Joint Embedding Predictive Architecture) is a self-supervised learning approach for video understanding that learns representations by predicting masked spatio-temporal regions in latent space. Unlike generative approaches that reconstruct pixels, V-JEPA predicts in a learned embedding space—the model sees a partially masked video and must predict the embeddings of the masked regions.

OpenWorldLib positions V-JEPA as **perception-centric but incomplete** as a world model. Under the three-capability definition (perception, interaction, memory): V-JEPA excels at perception (learning rich video representations through latent prediction), has some memory capability (capturing temporal dependencies across frames), but crucially lacks **interaction**—it learns to observe and predict but cannot act. Its encoder focuses entirely on representation learning without action prediction or policy training, distinguishing it from approaches like Dreamer that use their models for planning.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04707]] OpenWorldLib | foundational method | Perception-centric approach with latent prediction; lacks interaction capability |

## Connections

- [[entities/dreamer]] — Dreamer uses its world model for interaction (latent imagination for policy training); V-JEPA's lack of this capability is OpenWorldLib's key critique—perception without interaction is incomplete
- [[topics/world-models]] — V-JEPA represents the perception-centric lineage of world models; its limitation motivates OpenWorldLib's emphasis on the full perception-interaction-memory triplet
- [[topics/video-understanding]] — Self-supervised video representation learning via latent prediction; the learned representations transfer to downstream video tasks