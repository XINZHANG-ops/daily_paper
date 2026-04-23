---
title: "RationalRewards"
slug: rationalrewards
type: model
paper_count: 1
last_updated: 2026-04-17
---

# RationalRewards

## What It Is

RationalRewards is a reasoning-based reward model (8B parameters) for visual generation that produces structured multi-dimensional critiques before assigning scores. Unlike scalar reward models (ImageReward, EditReward, PickScore) that compress judgments into a single number, RationalRewards generates explicit reasoning about what to improve and why, then derives scores from that reasoning.

The model transforms reward models from passive evaluators into active optimization tools by enabling dual-space optimization: parameter-space RL and test-time prompt refinement.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.11626]] | core method | Reasoning-based reward model for visual generation; achieves SOTA preference prediction with 10-20× less training data |

## Connections

- [[entities/parrot]] — PARROT is the training framework that produces RationalRewards
- [[entities/diffusionnft]] — DiffusionNFT uses RationalRewards for RL fine-tuning
- [[entities/qwen3-vl]] — Qwen3-VL-32B-Instruct is the teacher model for PARROT training
- [[ideas/reward-hacking-resistance]] — RationalRewards' structured reasoning fundamentally prevents reward hacking