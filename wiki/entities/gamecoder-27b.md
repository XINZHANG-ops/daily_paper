---
title: "GameCoder-27B"
slug: gamecoder-27b
type: model
paper_count: 1
last_updated: 2026-04-21
---

# GameCoder-27B

## What It Is

GameCoder-27B is a domain-specialized code model built on Qwen3.5-27B backbone, trained specifically for web game development using the Phaser framework. It is the core code generation engine powering the OpenGame agentic framework.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18394]] OpenGame | core method | Trained via CPT→SFT→RL pipeline; achieves BH=63.9, VU=57.0, IA=54.1 on OpenGame-Bench |

## Connections

- [[2604.18394]] — GameCoder-27B is the foundation model for OpenGame; three-stage training (continual pre-training, SFT, execution-grounded RL) instills game engine architectural priors that general LLMs lack
- [[entities/qwen3-5-27b]] — Base backbone; GameCoder-27B inherits Qwen3.5-27B's general capabilities and adds game-specific specialization
- [[topics/llm-training]] — The CPT→SFT→RL training progression exemplifies modern domain adaptation for code models
