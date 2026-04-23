---
title: "RoPE"
slug: rope
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# RoPE

## What It Is

RoPE (Rotary Position Embedding) is a positional encoding mechanism whose rotation property creates Q/K geometry instabilities that TriAttention exploits for efficient KV compression.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04921]] TriAttention | positional encoding | RoPE's rotation property central to TriAttention's method |

## Connections

- [[entities/snapkv]] — SnapKV's post-RoPE approach affected by the same geometry
- [[topics/kv-cache-compression]] — RoPE's properties enable compression techniques