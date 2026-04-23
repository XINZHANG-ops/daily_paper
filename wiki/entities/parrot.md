---
title: "PARROT"
slug: parrot
type: algorithm
paper_count: 1
last_updated: 2026-04-17
---

# PARROT (Preference-Anchored Rationalization)

## What It Is

PARROT is a variational training framework that trains reasoning-based reward models from readily available preference data without costly rationale annotations. It treats rationales as latent variables inferred from pairwise preference data via an Evidence Lower Bound (ELBO) objective.

The framework implements a three-phase pipeline that maps directly to the ELBO decomposition:
1. **Rationale Generation (Hindsight)**: Teacher VLM generates candidate rationales anchored to known preference labels
2. **Consistency Filtering**: Retain only rationales where preference can be recovered from (x, z) alone
3. **Student SFT (Foresight)**: Train student model to generate rationales without seeing the answer

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.11626]] | training framework | PARROT trains RationalRewards (8B) from preference data; direct distillation without PARROT underperforms by 6.8-17.3 points |

## Connections

- [[entities/rationalrewards]] — RationalRewards is the output of PARROT training
- [[entities/qwen3-vl]] — Qwen3-VL-32B-Instruct serves as the teacher model