---
title: "Human-Object Interaction"
slug: human-object-interaction
paper_count: 1
last_updated: 2026-04-18
---

# Human-Object Interaction

## Overview

Human-object interaction (HOI) video generation focuses on creating videos where humans and objects interact naturally and coherently.

## Evolution

Mid-April 2026, OmniShow (2604.11804) established HOI video generation through unified multimodal conditions, combining reference identity, action description, and environment context in a single generation framework. This represents a step toward more controllable video generation where human characters can be placed in specified environments performing specified actions—critical for applications like robotics imitation learning and interactive AI assistants.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.11804]] OmniShow | 2026-04-14 | Unified multimodal conditions for HOIVG |

## Patterns & Insights

- **Unified condition control is essential**: OmniShow's unified multimodal approach (identity + action + environment) shows that separate condition handling leads to inconsistency
- **HOI enables downstream applications**: Robotics imitation learning and interactive AI assistants both need human-object coherence—HOI is foundational for these applications
- **Video generation for HOI vs text-to-video**: HOI requires maintaining human identity and object relationships across frames—standard T2V struggles with this specificity

## Connections

- [[topics/video-generation]] — HOI is a specific video generation task
- [[topics/multimodal-models]] — HOI requires multimodal understanding