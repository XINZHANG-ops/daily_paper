---
title: "World Models"
slug: world-models
paper_count: 1
last_updated: 2026-04-16
---

# World Models

## Overview

World models aim to enable agents to understand, predict, and interact with complex physical environments. The papers reveal a critical distinction: **most "world models" in literature do not meet the definition**—they lack one or more of the three necessary capabilities: perception, interaction, and long-term memory. OpenWorldLib provides the first unified framework and clear definition, surveying prior work (Dreamer, V-JEPA, Ha & Schmidhuber) and organizing them under the perception-interaction-memory triplet.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04707]] OpenWorldLib | 2026-04-07 | Unified definition and framework for world models |

## Patterns & Insights

- **Perception-interaction-memory triplet is necessary and sufficient**: A model without all three is not a true world model
- **Text-to-video is NOT a world model**: Video generation without complex perceptual inputs does not qualify
- **V-JEPA is incomplete**: It has perception and prediction but lacks interaction capabilities

## Open Problems

- Building world models that scale to open-world physical environments
- Combining the three capabilities (perception, interaction, memory) in a unified architecture
- Evaluating world models against the formal definition

## Connections

- [[topics/embodied-ai]] — World models are foundational for embodied AI tasks
- [[topics/video-generation]] — Interactive video generation is a key world model capability
- [[entities/dreamer]] — Foundational world model approach predating OpenWorldLib
- [[entities/v-jepa]] — Perception-centric approach that OpenWorldLib positions as incomplete
