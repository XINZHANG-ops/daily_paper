---
title: "Sampling Is Optimization"
slug: sampling-is-optimization
source: note
last_updated: 2026-04-16
---

# Sampling Is Optimization

## The Insight

LLM sampling strategies (top-k, nucleus/top-p, temperature) are all solving the same underlying optimization problem on the probability simplex. The Mirror Ascent algorithm provides a general framework: given a target distribution and K samples, iteratively optimize the probability of drawing from that distribution. The different strategies (top-k's hard cutoff, top-p's probabilistic threshold, temperature's entropy scaling) are just different regularization terms in the same optimization objective.

## Evidence

- [Note 2026-02-25] — Paper on "Decoding as Optimisation on the Probability Simplex: From Top-K to Top-P (Nucleus) to Best-of-K Samplers" presents Mirror Ascent as a general solver for the sampling optimization problem
- [[2604.05404]] — PTE introduces hardware-aware cost modeling for inference; if sampling is optimization, then cost-aware sampling is bi-level optimization (choose samples that are good AND cheap)

## Implications

1. **Unified framework**: All sampling hyperparameters are just different regularizers in one optimization problem
2. **Cost-aware decoding**: If sampling is optimization and inference has asymmetric prefill/decode costs, then optimal sampling should be cost-aware
3. **Better hyperparameter tuning**: Instead of tuning top-k, top-p, and temperature independently, the unified view suggests a single control parameter with cost constraints

## Connections

- [[topics/llm-efficiency]] — Sampling is part of the inference pipeline; understanding it as optimization enables cost-aware decoding
- [[ideas/entropy-is-misleading]] — If sampling is optimization, then entropy-based metrics miss the actual objective being optimized
