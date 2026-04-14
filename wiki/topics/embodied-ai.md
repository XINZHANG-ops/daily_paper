---
title: "Embodied AI"
slug: embodied-ai
paper_count: 1
last_updated: 2026-04-10
---

# Embodied AI

## Overview

Embodied AI research bridges the gap between general Vision-Language Models and the demanding requirements of real-world agent deployment. HY-Embodied-0.5 from Tencent's Robotics X and HY Vision teams represents a significant step toward foundation models purpose-built for physical interaction, achieving state-of-the-art on 16/22 benchmarks while demonstrating practical robot control capabilities.

The core challenge is that general VLMs lack the fine-grained visual perception required for physical grounding while embodied AI requires advanced reasoning for prediction, interaction, and planning in dynamic environments. HY-Embodied-0.5 addresses this through three architectural innovations: a Mixture-of-Transformers (MoT) architecture enabling modality-adaptive computing with non-shared parameters for visual and text tokens, effectively doubling visual parameter capacity without significant overhead; an efficient native-resolution Vision Transformer (HY-ViT 2.0) supporting arbitrary-resolution inputs through knowledge distillation from a larger internal model; and visual latent tokens bridging vision and language modalities through learnable tokens supervised by global features from a large ViT.

The training pipeline employs a three-stage approach: large-scale pre-training on 600B+ tokens covering visual perception, spatial reasoning, and embodied understanding; an iterative self-evolving post-training paradigm combining reinforcement learning with rejection sampling fine-tuning; and large-to-small on-policy distillation to transfer advanced capabilities from the 32B model to the efficient 2B variant. The self-evolution process alternates between RL (GRPO) and rejection sampling SFT to progressively improve thinking capabilities. Results show MoT-2B achieving state-of-the-art on 16/22 benchmarks with 58.0% average, while MoE-A32B achieves 67.0% average, surpassing Gemini 3.0 Pro at 63.6%. Practical robot control experiments demonstrate 85%, 80%, and 75% success rates on real-world packing, stacking, and hanging tasks respectively.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.07430]] HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents | 2026-04-07 | Mixture-of-Transformers architecture with native-resolution visual encoder; 67.0% on 22 benchmarks surpassing Gemini 3.0 Pro; 85%/80%/75% success on packing/stacking/hanging |

## Open Problems

- **Scaling to complex embodied scenarios**: While HY-Embodied-0.5 demonstrates strong performance, scaling to even more complex multi-step physical interactions remains challenging.
- **Iterative self-evolution balancing**: The iterative self-evolution paradigm requires careful balancing between RL and supervised fine-tuning to avoid capability regression.
- **Diverse robot morphologies**: Extending the framework to handle different robot embodiments and physical configurations.
- **Edge deployment optimization**: Efficient 2B model achieves strong results but edge deployment in real-time robotics contexts may require further optimization.
- **Physical world simulation integration**: Scalable training through physical simulation for diverse interaction scenarios.

## Connections

- [[topics/agent-systems]] — Embodied foundation models provide the perception and action capabilities central to agent systems; OpenWorldLib defines the world model framework these models fit within
- [[topics/reinforcement-learning]] — Iterative self-evolving post-training combines RL (GRPO) with rejection sampling, connecting to RL training methodology research