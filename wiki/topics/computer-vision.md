---
title: "Computer Vision"
slug: computer-vision
paper_count: 2
last_updated: 2026-04-13
---

# Computer Vision

## Overview

The two papers in this topic represent complementary advances in visual representation learning and 3D perception. **SteerViT** introduces a paradigm shift from late fusion to early vision-language fusion via gated cross-attention layers interleaved within frozen ViT blocks, producing "steerable visual representations" that can be directed with natural language while preserving the underlying representation quality of the frozen backbone. The key insight is that standard ViTs suffer from "photographer bias"—they tend to focus on the most salient objects with no mechanism to redirect attention. SteerViT addresses this by allowing text to influence visual processing even at early layers, achieving 96% retrieval accuracy on CORE (vs 44% for vanilla DINOv2) while adding only ~21M trainable parameters. The tanh-gated cross-attention with zero-initialized gates enables smooth interpolation between vanilla ViT and fully text-conditioned state via a continuous scaling factor.

**WildDet3D** tackles the challenge of open-vocabulary monocular 3D object detection through two contributions: a unified geometry-aware architecture supporting text, point, box, and exemplar prompts with optional depth input, and WildDet3D-Data—a dataset with 1M images across 13.5K categories, 138x larger than existing benchmarks. The architecture employs dual-vision encoders (image + RGBD) with ControlNet-style depth fusion, and achieves 34.2 AP3D on Omni3D with text prompts, with a striking +20.7 AP average gain when depth signals are available at inference time. Particularly notable is the training efficiency: 12 epochs vs 80-120 for competing approaches, achieved through auxiliary 2D detection and depth estimation heads providing complementary supervision.

The two papers together advance the trajectory from passive image understanding toward active spatial intelligence—SteerViT by giving vision models language-directed attention control, and WildDet3D by extending detection to full 3D space with flexible prompting. Both emphasize parameter efficiency: SteerViT's 21M added parameters vs billion-parameter MLLMs, and WildDet3D's 12-epoch efficiency vs prior methods' 80-120 epochs.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.02327]] SteerViT: Steerable Visual Representations | 2026-04-01 | Early V-L fusion via gated cross-attention in frozen ViT; 96% CORE accuracy vs 44% DINOv2; 21M trainable params; zero-shot transfer to personalized object discrimination, anomaly detection |
| [[2604.08626]] WildDet3D: Scaling Promptable 3D Detection in the Wild | 2026-04-08 | Unified text/point/box/exemplar promptable 3D detection; WildDet3D-Data (1M images, 13.5K categories, 138x existing benchmarks); 12 epochs training vs 80-120; +20.7 AP with depth cues |

## Open Problems

- **Cross-architecture generalization**: SteerViT conclusions are coupled to transformer-based vision encoders; extension to CNN-based architectures unexplored. WildDet3D focuses on single-image monocular detection; video-based temporal integration could improve tracking and stability.
- **Depth availability**: WildDet3D shows dramatic gains (+20.7 AP) with depth, but graceful degradation to monocular mode when depth is unavailable means the benefit depends on sensor availability.
- **Structural vs content understanding**: MinerU2.5-Pro (in data-centric-ai) notes that advancing from content extraction to structured semantic understanding is the next step—this applies equally to 3D detection where relationships between objects are as important as individual detections.
- **Evaluation coverage**: Both papers use existing benchmarks (CORE, Omni3D) that may not fully capture real-world diversity; domain-specific evaluation sets for vertical applications remain needed.

## Connections

- [[topics/vision_language_models]] — SteerViT is directly relevant to VLM architecture improvements; early vs late fusion debates
- [[topics/3d-detection]] — WildDet3D is the primary paper for open-vocabulary 3D detection
- [[topics/data-centric-ai]] — WildDet3D's data engine (1M images, 13.5K categories) represents massive data engineering; the data-centric principle (performance from data quality, not just model scale) applies broadly