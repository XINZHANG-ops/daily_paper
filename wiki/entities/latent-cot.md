---
title: "Latent Chain-of-Thought"
slug: latent-cot
type: concept
paper_count: 1
last_updated: 2026-04-21
---

# Latent Chain-of-Thought

## What It Is

Latent Chain-of-Thought (Latent CoT) is an approach that compresses explicit reasoning chains into continuous latent representations, enabling faster inference by replacing autoregressive token generation with parallel latent token prediction. Previous methods (COCONUT, CODI, SIM-CoT) used purely linguistic latent representations, which compress symbolic abstractions rather than causal dynamics. OneVL extends this with dual-modal supervision (language + visual world model) to ensure latents encode genuine causal scene structure.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18486]] OneVL | core concept | OneVL is the first latent CoT method to surpass explicit CoT through dual-modal supervision |

## Connections

- [[entities/meanflow]] — OneVL's latent CoT draws from MeanFlow's compression principle; both achieve single-pass inference through learned representations
- [[topics/embodied-ai]] — Latent CoT for VLA planning in autonomous driving
- [[topics/reinforcement-learning]] — OneVL's training pipeline uses RL-aligned warmup stages
