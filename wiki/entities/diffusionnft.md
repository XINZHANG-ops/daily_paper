---
title: "DiffusionNFT"
slug: diffusionnft
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# DiffusionNFT

## What It Is

DiffusionNFT is an online RL framework for diffusion models that operates on the forward diffusion process via flow matching, avoiding the need for likelihood estimation, solver restrictions, or classifier-free guidance required by reverse-process approaches.

The algorithm frames RL for diffusion models as supervised contrastive learning: at each iteration, it samples K images, evaluates them with a reward function, splits into positive (high-reward) and negative (low-reward) subsets, and updates via contrastive flow-matching loss. The velocity-field difference between positive and negative policies defines a reinforcement guidance direction that guarantees policy improvement.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.11626]] | RL algorithm | DiffusionNFT uses RationalRewards for parameter-space optimization; achieves +9.37 points on UniGenBench++ |

## Connections

- [[entities/rationalrewards]] — RationalRewards provides multi-dimensional reward signals for DiffusionNFT
- [[topics/reinforcement-learning]] — DiffusionNFT is an alternative to PPO/GRPO for visual generation RL