---
title: "Reward Hacking Resistance Through Structured Reasoning"
slug: reward-hacking-resistance
source: paper
last_updated: 2026-04-17
---

# Reward Hacking Resistance Through Structured Reasoning

## The Insight

Scalar reward models are susceptible to reward hacking because they compress evaluation into a single number that can be inflated by exploiting biases without genuine quality improvement. Structured reasoning—requiring coherent multi-dimensional justification before emitting scores—fundamentally prevents this by structurally grounding evaluation in interpretable criteria.

The key mechanism: when a model must explain why each dimension merits its score, reward inflation without corresponding visual evidence becomes difficult. The model cannot cheat a single number if it must justify each dimension separately.

## Evidence

- [[2604.11626]] — RationalRewards uses multi-dimensional structured critiques; RL with scalar rewards shows reward increases while visual quality degrades, but RationalRewards maintains monotonic correspondence between reward and quality
- [[2604.06628]] — RL training for reasoning shows safety degradation is a real failure mode; structured reward models might detect this across dimensions rather than missing it in scalar aggregation

## Implications

1. **Structured rewards prevent gaming**: Multi-dimensional scoring means you can't improve one number by gaming—each dimension must be justified
2. **Interpretability is a feature, not overhead**: Explaining why a score is given protects against reward hacking better than any algorithmic constraint
3. **Test-time compute helps**: The GCR loop in RationalRewards shows that critique-and-refine at test time can match RL training, suggesting that more reasoning time is naturally protective

## Connections

- [[entities/rationalrewards]] — RationalRewards is the concrete implementation of this principle
- [[entities/parrot]] — PARROT trains models to produce structured reasoning rather than scalar scores
- [[topics/reinforcement-learning]] — Reward hacking is a fundamental RL failure mode; structured rewards address it
- [[ideas/sae-random-baseline]] — Both ideas question whether learned representations truly understand vs. finding exploitable patterns