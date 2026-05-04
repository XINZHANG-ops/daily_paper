---
title: "Dreamer"
slug: dreamer
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# Dreamer

## What It Is

Dreamer is a family of model-based reinforcement learning agents (DreamerV1-V3) that learn a world model from pixels and use it for planning. The core idea: instead of learning a policy directly from raw observations, Dreamer first learns a latent dynamics model (encoding observations → compact state → predicting future states and rewards), then trains an actor-critic policy entirely within the learned latent space ("imagination"). This decouples representation learning from policy learning.

Under OpenWorldLib's definition, Dreamer is a canonical world model: it has **perception** (encoding images to latent states), **interaction** (acting in imagination to train policies), and **long-term memory** (the recurrent state space model captures temporal dependencies). OpenWorldLib surveys Dreamer as one of the foundational approaches that informed its unified six-component framework.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04707]] OpenWorldLib | foundational method | Model-based RL approach with latent imagination, demonstrating the perception-interaction-memory triplet |

## Connections

- [[entities/v-jepa]] — Both are foundational world model methods: Dreamer uses model-based RL with latent dynamics, while V-JEPA uses self-supervised learning with a predictive objective; OpenWorldLib notes V-JEPA lacks Dreamer's explicit interaction capability
- [[topics/world-models]] — Represents the model-based RL lineage of world models; complements perception-centric and generation-centric approaches
- [[topics/reinforcement-learning]] — Dreamer's latent imagination policy training is a key model-based RL technique that decouples policy optimization from environment interaction