---
title: "MVTec AD"
slug: mvtec-ad
type: benchmark
paper_count: 1
last_updated: 2026-04-18
---

# MVTec AD

## What It Is

MVTec AD (Anomaly Detection) is an industrial inspection benchmark containing high-resolution images of 15 object and texture categories with pixel-level anomaly annotations. It is the standard benchmark for evaluating unsupervised anomaly detection and localization—the task of identifying manufacturing defects without labeled examples of what defects look like.

SteerViT achieves performance on MVTec AD that matches dedicated anomaly detection methods, despite not being trained for this task. This emergent capability arises from SteerViT's referential segmentation pretext: the model learns to attend to fine-grained visual differences (distinguishing "this object" from "that background"), and this attention behavior transfers to distinguishing "normal" from "anomalous" regions—a demonstration that visual representation quality can unlock unexpected downstream capabilities.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.02327]] Steerable ViT | benchmark | SteerViT matches dedicated anomaly detection methods via emergent transfer from referential segmentation |

## Connections

- [[entities/steervit]] — SteerViT's emergent anomaly detection demonstrates representation quality transfer
- [[topics/computer-vision]] — MVTec AD is the canonical anomaly detection benchmark; strong performance signals generalizable visual representations
- [[topics/representation-learning]] — SteerViT's MVTec AD result is evidence that good representations enable emergent capabilities beyond the training objective