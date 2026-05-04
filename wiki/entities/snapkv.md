---
title: "SnapKV"
slug: snapkv
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# SnapKV

## What It Is

SnapKV is a KV cache compression algorithm that reduces memory during LLM inference by selectively retaining only the most important key-value pairs. It operates **post-RoPE**: after position encoding has been applied, it uses an observation window to score the importance of each KV entry and prunes those below a threshold.

TriAttention identifies a fundamental limitation: post-RoPE observation windows are inherently unstable because RoPE rotation disperses Q/K vectors, making importance scores unreliable for distant tokens. TriAttention achieves 2.5x throughput improvement at equivalent accuracy compared to SnapKV by moving to pre-RoPE importance scoring with trigonometric series-based compression. Despite this limitation, SnapKV remains an influential baseline because it was the first to demonstrate that KV pruning could maintain accuracy for long-context tasks.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04921]] TriAttention | baseline | Post-RoPE observation window approach; limited by rotation-induced instability |

## Connections

- [[entities/rope]] — SnapKV's post-RoPE design means it can only observe keys affected by RoPE dispersion; TriAttention exploits pre-RoPE concentration that SnapKV's architecture cannot access
- [[topics/kv-cache-compression]] — SnapKV established the viability of KV pruning; TriAttention improves on it by fixing the observation window problem
- [[topics/llm-efficiency]] — KV compression is a key technique for making long-context LLM inference practical