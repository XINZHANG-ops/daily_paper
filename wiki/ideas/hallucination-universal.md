---
title: "Hallucination Is Universal Across Model Scale"
slug: hallucination-universal
source: paper
last_updated: 2026-04-17
---

# Hallucination Is Universal Across Model Scale

## The Insight

Hallucination is the primary failure mode for complex AI agents, regardless of model scale or capability level. DR3-Eval reveals that even frontier models (Claude Sonnet 4, which performs best) still hallucinate. This suggests hallucination is not solvable by scale alone—it emerges from the fundamental nature of generative models optimizing next-token prediction.

## Evidence

- [[2604.14683]] — DR3-Eval finds hallucination as the primary failure mode across all models tested; even Claude Sonnet 4 (best performer) still hallucinates
- [[2604.08546]] — NUMINA addresses counting errors as a failure mode in video generation; similar to hallucination in textual generation

## Implications

1. **Scale doesn't solve hallucination**: Bigger models don't reliably hallucinate less; they may hallucinate differently
2. **Evaluation must measure hallucination directly**: Traditional accuracy metrics miss hallucination; need factuality checks
3. **Agents need self-monitoring**: Since agents can't know when they're hallucinating, evaluation must be external

## Connections

- [[topics/agent-evaluation]] — Hallucination detection is a key evaluation metric
- [[topics/agent-systems]] — Deep research agents are particularly vulnerable to hallucination in citation and factual claims
- [[ideas/agent-reliability-systems]] — Hallucination is the core reliability challenge that systems must address