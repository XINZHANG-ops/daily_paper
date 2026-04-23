---
title: "Embodied AI"
slug: embodied-ai
paper_count: 7
last_updated: 2026-04-21
---

# Embodied AI

## Overview

Embodied AI research focuses on enabling models to understand and interact with physical environments. The papers reveal two complementary approaches: (1) scalable foundation models with large-scale pre-training and self-evolution (HY-Embodied-0.5, SpatialEvo), and (2) specialized 3D detection with open-vocabulary capabilities (WildDet3D).

The key theme is that **physical grounding requires deterministic feedback**, not model consensus. When ground truth is computable from geometry (as in 3D spatial reasoning), deterministic feedback outperforms self-evolution based on model voting.

## Evolution

Early April 2026 saw HY-Embodied-0.5 introduce Mixture-of-Transformers architecture for modality-adaptive computing with embodied-RL. WildDet3D followed with open-vocabulary 3D detection at scale. By mid-April, SpatialEvo proposed Deterministic Geometric Environments where ground truth comes from geometry computation, not model consensus, and HY-World 2.0 extended to unified 3D world reconstruction and generation. RAD-2 applied BEV-Warp simulation to motion planning RL. On April 21, OneVL introduced latent CoT with dual-modal world model supervision, achieving the first latent CoT method to surpass explicit CoT while matching answer-only inference speed—demonstrating that world model prediction (future-frame visual tokens) provides the causal grounding that purely linguistic latents lack.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04707]] OpenWorldLib | 2026-04-07 | Unified definition and framework for world models with perception-interaction-memory triplet |
| [[2604.07430]] HY-Embodied-0.5 | 2026-04-10 | MoT architecture with embodied foundation models |
| [[2604.08626]] WildDet3D | 2026-04-13 | Open-vocabulary 3D detection with 138× more categories |
| [[2604.14144]] SpatialEvo | 2026-04-16 | Deterministic Geometric Environments for spatial reasoning |
| [[2604.14268]] HY-World 2.0 | 2026-04-17 | Unified 3D world reconstruction and generation |
| [[2604.15308]] RAD-2 | 2026-04-20 | BEV-Warp simulation for motion planning RL |
| [[2604.18486]] OneVL | 2026-04-21 | Latent CoT with world model supervision for VLA planning |

## Patterns & Insights

- **Physical grounding needs deterministic feedback**: Geometry provides ground truth that model consensus cannot
- **Open-vocabulary is essential**: Real-world environments have unlimited categories, closed vocabularies fail
- **Self-evolution can reinforce errors**: Model voting in self-evolution can compound errors rather than correct them

## Open Problems

- Combining deterministic physics with learned representations
- Real-time embodied perception and action at scale
- Transfer from simulation to real-world environments

## Connections

- [[topics/agent-systems]] — Embodied agents require similar reliability infrastructure
- [[topics/3d-detection]] — 3D detection is foundational for spatial understanding
- [[topics/spatial-reasoning]] — SpatialEvo specifically addresses spatial reasoning