---
title: "World Models"
slug: world-models
paper_count: 2
last_updated: 2026-04-13
---

# World Models

## Overview

The two papers in this topic address the foundational challenge of building AI systems that maintain internal representations of the world for prediction, interaction, and planning. **OpenWorldLib** confronts the fundamental lack of standardized definitions in world model research by proposing that a world model is "a model or framework centered on building internal representations from perception, equipped with action-conditioned simulation and long-term memory capabilities, for understanding and predicting the dynamics of a complex world." This definition explicitly distinguishes true world models from narrow applications like text-to-video generation (e.g., Sora) by emphasizing three core capabilities: perception, interaction, and long-term memory. The paper introduces OpenWorldLib as a unified inference framework organizing world model tasks into five core modules (Operator, Synthesis, Reasoning, Representation, Memory) coordinated by a Pipeline module, validated across interactive video generation, 3D scene generation, and Vision-Language-Action (VLA) tasks. A key observation is that current byte organization favors next-token prediction, suggesting that achieving ideal world models may require hardware iterations and foundational model structure changes.

**HY-Embodied-0.5** provides the embodied AI complement—foundation models designed specifically for physical agents that require fine-grained visual perception alongside advanced reasoning. The architecture introduces a Mixture-of-Transformers (MoT) with non-shared parameters for visual and text tokens (doubling visual parameter capacity without overhead), a native-resolution Vision Transformer (HY-ViT 2.0) supporting arbitrary-resolution inputs via knowledge distillation, and a three-stage training pipeline: large-scale pre-training (600B+ tokens), iterative self-evolving post-training (GRPO + rejection sampling SFT), and large-to-small on-policy distillation. The 2B model achieves SOTA on 16/22 benchmarks; the 32B MoE variant achieves 67.0% average, surpassing Gemini 3.0 Pro at 63.6%. Notably, it demonstrates real-world robot control with 85%, 80%, and 75% success rates on packing, stacking, and hanging tasks.

The two papers together reveal a convergence: OpenWorldLib argues that world models require perception + interaction + memory, while HY-Embodied-0.5 demonstrates this convergence in an embodied agent that perceives (HY-ViT 2.0), interacts (VLA policy), and reasons (MoT backbone with iterative self-evolution). OpenWorldLib's insight that current hardware favors next-token prediction may explain why HY-Embodied-0.5's VLA approach (predicting actions, not tokens) is particularly challenging yet critical.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04707]] OpenWorldLib: A Unified Codebase and Definition of Advanced World Models | 2026-04-05 | Standardized definition distinguishing world models from video generation; five-core architecture (Operator/Synthesis/Reasoning/Representation/Memory); validated across interactive video, 3D, and VLA tasks |
| [[2604.07430]] HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents | 2026-04-07 | MoT architecture with modality-adaptive computing; HY-ViT 2.0 native-resolution encoder; 600B+ token pre-training; 67.0% on 22 benchmarks (surpasses Gemini 3.0 Pro); real robot control at 85%/80%/75% |

## Open Problems

- **Hardware alignment**: OpenWorldLib notes current byte organization favors next-token prediction; world models may require hardware iterations and architectural changes beyond token-based Transformers.
- **Next-frame prediction bias**: Current world model architectures focus heavily on next-frame prediction, which aligns with human sensory processing but differs from how LLMs are pre-trained on internet text.
- **Scaling to diverse robot morphologies**: HY-Embodied-0.5 demonstrates strong results but acknowledges extending to more diverse robot morphologies remains challenging.
- **Balancing RL and SFT**: The iterative self-evolving paradigm requires careful balancing between reinforcement learning and supervised fine-tuning to avoid capability regression.

## Connections

- [[topics/agent-systems]] — HY-Embodied-0.5 integrates perception, interaction, and memory for embodied agent capabilities; OpenWorldLib's Pipeline module addresses orchestration for agent tasks
- [[topics/robotics]] — Robot control experiments (packing, stacking, hanging) in HY-Embodied-0.5
- [[topics/video-understanding]] — OpenWorldLib's interactive video generation evaluation connects to streaming video understanding
- [[topics/computer-vision]] — HY-ViT 2.0 and dual-vision encoder architecture; WildDet3D's 3D detection relates to OpenWorldLib's Representation module