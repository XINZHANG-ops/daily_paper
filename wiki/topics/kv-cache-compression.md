---
title: "KV Cache Compression"
slug: kv-cache-compression
paper_count: 1
last_updated: 2026-04-07
---

# KV Cache Compression

## Overview

Long chain-of-thought reasoning creates a severe memory bottleneck as the KV cache grows linearly with context length, making memory-bound decode phases increasingly expensive. Standard attention mechanisms must retain all key-value pairs for every token in context, making long sequences infeasible even with substantial GPU memory. KV cache compression methods aim to reduce memory footprint while preserving the critical information needed for accurate reasoning—identifying which tokens are most important to retain versus which can be discarded.

Prior KV compression approaches score token importance from post-RoPE attention scores, but TriAttention (2604.04921) reveals a fundamental flaw in this strategy: queries rotate with position during RoPE, creating only a tiny observation window for importance estimation. The most recent queries retain up-to-date orientations while earlier queries rotate away, so important keys may receive low attention scores during the observation window and be permanently evicted—causing up to 50% accuracy degradation at equivalent compression ratios. This explains why prior methods like R-KV achieve only ~20% accuracy at the same efficiency that Full Attention achieves 40.8%.

The key insight is "Q/K concentration" in pre-RoPE space: Q and K vectors are highly concentrated around fixed non-zero centers and remain stable across positions (Mean Resultant Length R approaching 1.0 for most heads). This concentration enables predictable distance preferences via a trigonometric series—attention follows a stable curve determined by Q/K centers rather than volatile post-RoPE observations. TriAttention uses this to score keys via the trigonometric series derived from stable Q/K centers plus norm-based signals, achieving 2.5× higher throughput or 10.7× KV memory reduction at equivalent accuracy to Full Attention on AIME25. Cross-architecture validation confirms Q/K concentration holds across Qwen3, Qwen2.5, Llama3 (GQA), and GLM-4.7 (MLA) architectures, making this a model-intrinsic property robust to calibration data choice.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04921]] TriAttention: Efficient Long Reasoning with Trigonometric KV Compression | 2026-04-05 | Discovers Q/K concentration in pre-RoPE space; trigonometric series scoring from stable Q/K centers; 2.5× throughput or 10.7× KV memory reduction vs Full Attention |

## Open Problems

- Dedicated hardware-aware inference kernels optimized for trigonometric series computation could further improve efficiency
- Evaluation on broader domains beyond mathematical reasoning—particularly coding and agentic tasks—remains future work
- Head-specific compression budgets could improve efficiency-accuracy tradeoffs beyond uniform budget allocation
- MLA architecture shows even stronger Q/K concentration (96.6% heads with R>0.95 vs 84.7% for GQA), suggesting architecture-specific optimization opportunities

## Connections

- [[topics/reasoning]] — Long chain-of-thought reasoning is the primary beneficiary of KV cache compression; TriAttention enables reasoning over 32K-token sequences with limited memory
- [[topics/llm-efficiency]] — Hardware-aware PTE metric (from 2604.05404) could be extended to measure KV compression efficiency in real deployment scenarios