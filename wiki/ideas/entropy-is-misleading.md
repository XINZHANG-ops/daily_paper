---
title: "Entropy Is Misleading"
slug: entropy-is-misleading
type: idea
source: synthesis
last_updated: 2026-04-16
---

# Entropy Is Misleading

## The Insight

High entropy does not guarantee diverse, high-quality reasoning. Entropy measures within-prompt variability but cannot detect whether that variability is actually responsive to input differences. A model can have high entropy (seemingly diverse outputs) while being input-agnostic (all outputs are variations of the same template).

This pattern appears across multiple papers: entropy metrics fail to detect template collapse in RL (RAGEN-2), and high-textual-frequency data works better despite having lower "complexity" metrics (Adam's Law).

## Evidence

- [[2604.06268]] — Entropy correlates +0.39 with performance but template collapse has high entropy and poor performance. MI-based diagnostics (+0.39 correlation) outperform entropy (-0.14).
- [[2604.02176]] — High-frequency textual data outperforms low-frequency despite having lower complexity scores (Max Dependency Tree Depth, Flesch-Kincaid). This suggests complexity ≠ quality for LLM understanding.
- [[2604.11297]] — MEDS addresses "stable error basin" where sampling diversity collapses not because entropy is low, but because the model keeps sampling from the same error pattern

## Implications

For evaluation and training:

1. **Don't trust entropy alone** as a training health metric
2. **Cross-input analysis matters**: Check if model behavior changes across different inputs, not just within a single prompt
3. **High-frequency might mean "well-represented"**: Data that appears simple may actually be better learned

## Connections

- [[ideas/template-collapse]] — Template collapse exemplifies entropy's failure to capture true diversity
- [[topics/reinforcement-learning]] — RL training health monitoring requires better metrics than entropy