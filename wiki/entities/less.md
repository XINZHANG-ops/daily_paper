---
title: "LESS"
slug: less
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# LESS

## What It Is

LESS (Learned Sample Selection) is a dynamic data selection algorithm that uses gradient-based importance scoring to choose which training examples benefit the model most. Rather than training on all available data, LESS computes gradient similarity between candidate examples and a target validation set, selecting examples whose gradients align with the desired model behavior.

The method operates in two phases: (1) a warmup phase on a random subset to initialize representations, then (2) gradient-based selection at each training step where examples with low alignment scores get pruned. In DataFlex, LESS exemplifies the **Select Trainer** paradigm, seamlessly plugging into the unified framework. On Mistral-7B, LESS achieves a 5.8pp MMLU improvement over static full-data training, and DataFlex reduces its runtime by 57% on 8 GPUs through shared infrastructure compared to the original standalone implementation.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2603.26164]] DataFlex | algorithm | Select Trainer: gradient-based dynamic selection with 5.8pp MMLU improvement |

## Connections

- [[entities/domi]] — LESS handles sample selection (Select Trainer), DoReMi handles domain mixture (Mix Trainer); complementary paradigms unified in DataFlex
- [[topics/data-centric-ai]] — Gradient-aligned sample selection is a principled approach to reducing training data while preserving (or improving) quality
- [[topics/llm-training]] — Data selection as an alternative to scaling dataset size for improving training efficiency