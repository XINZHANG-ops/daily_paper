---
title: "KV Cache Compression"
slug: kv-cache-compression
paper_count: 1
last_updated: 2026-04-16
---

# KV Cache Compression

## Overview

KV cache compression addresses the memory bottleneck created by massive KV caches during long chain-of-thought reasoning. The papers reveal that **pre-RoPE concentration is the key to stable long-context importance estimation**—TriAttention exploits the fact that before positional rotation, queries and keys cluster around fixed non-zero centers, providing a stable geometric structure for scoring which tokens to retain.

## Evolution

Early April 2026, TriAttention established the pre-RoPE concentration insight as the foundation for stable long-context importance estimation. This geometric approach to KV compression achieves 10.7x memory reduction while maintaining full accuracy on AIME25 and MATH 500. The approach contrasts with prior methods like SnapKV that suffer from the observation window problem after RoPE rotation.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04921]] TriAttention | 2026-04-07 | Pre-RoPE trigonometric series for 10.7x KV memory reduction |

## Patterns & Insights

- **Pre-RoPE concentration enables stable scoring**: After RoPE rotation, query-key similarity is unstable; before rotation it's geometrically structured
- **Trigonometric series captures geometry**: Q/K center relationships are preserved in trigonometric features
- **Same accuracy, 10.7x memory reduction**: Compression achieves full accuracy retention on AIME25 and MATH 500

## Open Problems

- Extending pre-RoPE concentration insights to other compression methods
- Adaptive compression budgets for different token importance levels
- Combining compression with efficient attention architectures

## Connections

- [[topics/llm-efficiency]] — KV cache compression is a key efficiency technique
- [[topics/reasoning]] — Long-context reasoning is the primary use case
- [[entities/snapkv]] — The primary baseline that TriAttention outperforms
