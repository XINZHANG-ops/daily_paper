---
title: "Qwen3.5-27B"
slug: qwen3-5-27b
type: model
paper_count: 1
last_updated: 2026-04-21
---

# Qwen3.5-27B

## What It Is

Qwen3.5-27B is a large language model from Alibaba's Qwen family, serving as the backbone for domain-specialized code models like GameCoder-27B. The GameCoder-27B paper (2604.18394) uses Qwen3.5-27B as the base and applies continual pre-training (CPT), supervised fine-tuning (SFT), and reinforcement learning (RL) to specialize it for web game development.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18394]] OpenGame | base model | Qwen3.5-27B serves as the backbone for GameCoder-27B; three-stage training adds game-specific architectural priors |

## Connections

- [[entities/gamecoder-27b]] — GameCoder-27B is built on Qwen3.5-27B
- [[entities/qwen3-vl]] — Qwen3-VL is a related multimodal variant of the Qwen family
- [[topics/llm-training]] — CPT→SFT→RL pipeline demonstrates modern domain adaptation methodology