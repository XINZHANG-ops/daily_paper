---
title: "3D Object Detection"
slug: 3d-detection
paper_count: 1
last_updated: 2026-04-13
---

# 3D Object Detection

## Overview

Monocular 3D object detection—estimating 3D bounding boxes from a single RGB image—represents a fundamental challenge in computer vision with applications in autonomous driving, robotics, and spatial understanding. The task requires reasoning about geometry, depth, and object relationships in 3D space while working from the information available in a 2D image. This constraint makes the problem fundamentally underdetermined, yet real-world applications demand reliable 3D understanding from commodity cameras.

WildDet3D (2604.08626) addresses open-vocabulary monocular 3D detection through two major contributions: a unified geometry-aware architecture and the largest open 3D detection dataset to date. The architecture accepts text, point, box, and exemplar prompts with optional depth input at inference time, employing dual-vision encoders (image + RGBD) with a depth fusion module based on ControlNet-style residual design. The 3D detection head uses deep supervision across transformer decoder layers with spherical harmonics ray features for camera geometry encoding. Notably, incorporating depth cues at inference time yields +20.7 AP average gain across settings, while training requires only 6-10x fewer epochs than prior methods (12 epochs vs 80-120).

The dataset WildDet3D-Data contains over 1M images across 13.5K categories—138x more than existing benchmarks like Omni3D—with human verification via multi-model candidate generation, VLM filtering, and human selection. The scale enables learning from substantially richer visual patterns while the open-vocabulary nature removes the constraint of predefined category taxonomies. Zero-shot transfer results are strong: 40.3 ODS on Argoverse 2 and 48.9 ODS on ScanNet, demonstrating the model's ability to generalize to new domains and sensor configurations without task-specific training.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.08626]] WildDet3D: Scaling Promptable 3D Detection in the Wild | 2026-04-08 | Unified promptable architecture with text/point/box/exemplar support; WildDet3D-Data with 1M images and 13.5K categories (138x existing benchmarks); 12-epoch training vs 80-120 for prior methods |

## Open Problems

- Single-image monocular detection lacks temporal integration that video-based approaches could leverage for improved stability and tracking
- Dataset construction relies on existing 2D annotations and VLM-human verification, which may introduce biases from the original annotation pipelines
- End-to-end 3D annotation pipelines that don't depend on 2D supervision remain future work
- Extension to diverse sensor modalities (event cameras, radar) beyond RGBD could enable robust detection in adverse conditions

## Connections

- [[topics/computer-vision]] — WildDet3D's dual encoder architecture (image + RGBD) represents state-of-the-art in geometric vision understanding
- [[topics/character-animation]] — Both papers involve 3D spatial understanding; LPM 1.0 addresses character performance in 3D space while WildDet3D focuses on object detection