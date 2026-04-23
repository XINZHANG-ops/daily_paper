---
title: "World Models"
slug: world-models
paper_count: 3
last_updated: 2026-04-21
---

# World Models

## Overview

World models aim to enable agents to understand, predict, and interact with complex physical environments. The papers reveal a critical distinction: **most "world models" in literature do not meet the definition**—they lack one or more of the three necessary capabilities: perception, interaction, and long-term memory. OpenWorldLib provides the first unified framework and clear definition, surveying prior work (Dreamer, V-JEPA, Ha & Schmidhuber) and organizing them under the perception-interaction-memory triplet. HY-World 2.0 demonstrates that this triplet can be achieved in practice through a unified four-stage pipeline.

## Evolution

Early April 2026, OpenWorldLib established the formal definition of world models as requiring perception, interaction, and long-term memory. This revealed that many prior approaches like V-JEPA are incomplete—they have perception but lack interaction. HY-World 2.0 then demonstrated that the perception-interaction-memory triplet can be achieved through a unified reconstruction-generation framework for 3D worlds, representing the first practical instantiation of a complete world model. On April 21, MultiWorld extended world models to multi-agent settings—solving the challenge of shared environment simulation where multiple agents act simultaneously from different viewpoints.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04707]] OpenWorldLib | 2026-04-07 | Unified definition and framework for world models |
| [[2604.14268]] HY-World 2.0 | 2026-04-17 | Unified reconstruction-generation framework for 3D worlds |
| [[2604.18564]] MultiWorld | 2026-04-21 | Scalable multi-agent multi-view video world models with MACM and GSE |

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
