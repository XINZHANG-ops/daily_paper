---
title: "SnapKV"
slug: snapkv
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# SnapKV

## What It Is

SnapKV is a KV cache compression algorithm that uses post-RoPE observation window selection. It serves as the primary baseline for TriAttention.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04921]] TriAttention | baseline | SnapKV's post-RoPE approach limited by observation window problem |

## Connections

- [[entities/rope]] — SnapKV's approach affected by RoPE's rotation property
- [[topics/kv-cache-compression]] — KV compression algorithm that TriAttention outperforms