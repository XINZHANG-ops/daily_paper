---
title: "Template Collapse"
slug: template-collapse
type: idea
source: paper
last_updated: 2026-04-16
---

# Template Collapse

## The Insight

Template collapse is a failure mode in multi-turn RL training where models produce diverse but input-agnostic reasoning. Within a single prompt, reasoning appears diverse and high-entropy, but across different prompts, the model produces similar "templates" regardless of input. Critically, this failure mode is **invisible to entropy-based metrics**—the standard approach for monitoring RL training.

The mechanism: high within-prompt reward variance suggests the model generates varied responses (good), but actually each prompt triggers a fixed template. The responses vary but are equally wrong for the specific input.

## Evidence

- [[2604.06268]] — RAGEN-2 identifies template collapse via MI-based diagnostics, shows entropy correlates +0.39 with performance while MI correlates -0.14 (entropy misses the failure)
- [[2604.07430]] — HY-Embodied-0.5 uses SNR-aware filtering to prevent template collapse during training
- [[2604.11297]] — MEDS addresses similar sampling diversity collapse with different mechanism (error pattern clustering)

## Implications

Template collapse means models can appear to train successfully (high entropy, stable rewards) while actually converging to useless input-agnostic responses. This has implications for:

1. **Evaluation**: Can't rely on entropy alone to monitor training health
2. **Safety**: Template collapse combined with safety training might produce models that appear safe but have hidden failure modes
3. **Reliability**: Agents that work during training may fail silently in deployment

## Connections

- [[topics/reinforcement-learning]] — Template collapse is a fundamental RL training failure mode
- [[ideas/entropy-is-misleading]] — Template collapse makes entropy monitoring insufficient for training health