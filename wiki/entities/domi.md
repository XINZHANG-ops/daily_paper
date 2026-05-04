---
title: "DoReMi"
slug: domi
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# DoReMi

## What It Is

DoReMi (Domain Reweighting with Minimax Optimization) is an algorithm for optimizing domain mixture proportions in LLM pretraining. Instead of uniform sampling across domains, DoReMi trains a small proxy model to identify which domains a larger model would benefit from most—domains where the proxy model performs worse get higher weights. The proxy model acts as a regret minimizer: it finds the mixture weights that minimize worst-case excess loss.

In DataFlex, DoReMi exemplifies the **Mix Trainer** paradigm, handling domain mixture optimization. DataFlex enables this method to run within a unified training pipeline without bespoke infrastructure, achieving both MMLU and perplexity improvements on SlimPajama compared to static baselines.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2603.26164]] DataFlex | paradigm | Mix Trainer domain mixture approach via proxy regret minimizer |

## Connections

- [[entities/less]] — LESS handles sample selection (Select Trainer), DoReMi handles domain mixture (Mix Trainer); together they represent two of DataFlex's three unified paradigms
- [[entities/llama-factory]] — LLaMA-Factory provides the training infrastructure that DataFlex layers DoReMi on top of
- [[topics/data-centric-ai]] — Domain-level data optimization as a complement to sample-level selection
- [[topics/llm-training]] — Dynamic domain mixture is an under-explored axis of LLM training optimization compared to architecture and recipe changes