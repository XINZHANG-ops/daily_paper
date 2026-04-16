---
title: "On-Policy RL Training Idling"
slug: on-policy-rl-idling
source: note
last_updated: 2026-04-16
---

# On-Policy RL Training Idling

## The Insight

Traditional on-policy RL training wastes GPU cycles because rollout generation has a long-tail latency distribution—when one rollout takes much longer than the rest, all other GPUs idle waiting. The solution (GLM-5 style) is to eliminate synchronization: each worker keeps generating rollouts independently, collecting N completions before training. But this introduces off-policy bias since the model changes during rollout generation. The fix is to record log-probabilities at generation time (using them as the old policy estimate) and mask gradients for tokens where the policy has shifted too far.

## Evidence

- [Note 2026-02-18] — GLM-5 paper describes the idling problem and solution: no synchronization, record log-probs at generation time, mask out-of-date gradients
- [[2604.03128]] — RLSD also addresses on-policy RL problems but from a different angle: credit assignment rather than rollout efficiency

## Implications

1. **Async rollout generation**: Eliminating synchronization barriers can dramatically improve GPU utilization
2. **Off-policy tolerance**: Masking gradients for out-of-date tokens provides a mechanism for tolerating off-policy rollouts
3. **Predictor-rewarder separation**: When predictor and rewarder are on different devices, token transport introduces noise; TITO (Token-in-Token-out) bypasses this by passing token IDs directly without decoding
4. **The idling problem is fundamental**: Any on-policy RL approach that requires synchronized rollouts will have this inefficiency

## Connections

- [[topics/reinforcement-learning]] — On-policy RL efficiency is a practical concern that affects all RL training methods
- [[entities/grpo]] — GRPO's group-relative advantage computation might have similar synchronization inefficiencies
