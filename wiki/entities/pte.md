---
title: "PTE"
slug: pte
type: metric
paper_count: 1
last_updated: 2026-04-16
---

# PTE (Prefill Token Equivalents)

## What It Is

PTE is a hardware-aware metric for measuring inference cost in Tool-Integrated Reasoning. It models the physical costs of transformer inference including the asymmetry between prefill (compute-bound) and decode (memory-bound) phases, KV-cache eviction during tool-call pauses, and the growing memory-bound decode overhead with cumulative context length. PTE achieves r=0.925 correlation with wall-clock latency (vs r=-0.375 for raw token counts).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.05404]] | introduced | PTE is the paper's main contribution |

## Connections

- [[topics/llm-efficiency]] — PTE provides the measurement framework for TIR efficiency
- [[topics/tool-integrated-reasoning]] — PTE is the foundational metric for this topic
