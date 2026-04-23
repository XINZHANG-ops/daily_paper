---
title: "Multi-Agent Condition Module (MACM)"
slug: macm
type: algorithm
paper_count: 1
last_updated: 2026-04-21
---

# Multi-Agent Condition Module (MACM)

## What It Is

MACM is the architectural component in MultiWorld that enables precise control of multiple agents within a shared video world model. It consists of two sub-components: Agent Identity Embedding (AIE) using rotary position embeddings to distinguish different agents, and Adaptive Action Weighting (AAW) to prioritize active agents over static ones.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18564]] MultiWorld | core architecture | AIE breaks multi-agent identity symmetry via RoPE; AAW dynamically prioritizes agents causing environmental change |

## Connections

- [[2604.18564]] — MACM is the primary innovation enabling multi-agent controllability in MultiWorld; AIE resolves the "mirror action" ambiguity problem
- [[entities/rope]] — AIE uses rotary position embedding to compute agent identity embeddings, leveraging the same mathematical principle as RoPE in LLMs
- [[topics/world-models]] — MACM extends world models from single-agent to multi-agent settings by solving the agent identity and action association problems
