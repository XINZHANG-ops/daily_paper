---
title: "LLM Training"
slug: llm-training
paper_count: 4
last_updated: 2026-04-13
---

# LLM Training

## Overview

The four papers in this topic collectively reshape how we think about post-training data engineering and optimization dynamics. **DataFlex** establishes that data is a first-class citizen in LLM training: dynamic sample selection (via gradient-based influence like LESS), domain mixture optimization (via DoReMi/ODM), and per-sample reweighting all yield measurable gains, and these gains are complementary to architectural improvements. Meanwhile, **RLSD** reveals that self-distillation in RLVR is not inherently leaky—the failure mode of On-Policy Self-Distillation is structural (an irreducible information asymmetry gap), and the fix is to repurpose the teacher from a generative target to a magnitude evaluator for credit assignment, with environment rewards holding exclusive authority over update direction.

A second major thread is the **Textual Frequency Law (TFL)** from the Adam's Law paper, which demonstrates that high-frequency textual expressions are systematically preferred by LLMs in both prompting and fine-tuning. This is a striking finding: paraphrases with identical meaning but different textual frequencies yield up to 8 percentage points difference in accuracy across math, translation, and commonsense reasoning. The law also motivates curriculum-based training (CTFT) that presents lower-frequency (harder) examples first, with a frequency estimation method that extends to LLM-generated story completions.

The fourth paper on **conditional generalization in reasoning SFT** upends a prevailing narrative—that SFT memorizes while RL generalizes—by showing that SFT's cross-domain generalization is not absent but conditional on optimization sufficiency, data quality, and model scale. The key finding is a "dip-and-recovery" non-monotonic training trajectory where OOD performance first degrades before improving with extended training. Even more remarkably, training on Countdown-CoT (a toy arithmetic game) transfers procedural reasoning patterns to math, code, and science domains—suggesting that CoT structures like backtracking and verification are themselves transferable independently of domain content. The catch is asymmetric generalization: while reasoning improves broadly, safety consistently degrades as procedural patterns teach models to work around guardrails.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2603.26164]] DataFlex: A Unified Framework for Data-Centric Dynamic Training | 2026-03-27 | Unified Select/Mix/Weight trainers for dynamic data selection, mixture optimization, and per-sample reweighting; 57% speedup for LESS on 8 GPUs |
| [[2604.03128]] Self-Distilled RLVR | 2026-04-02 | Repurposes self-distillation as token-level credit assignment magnitude; RLSD structurally immune to privileged information leakage |
| [[2604.02176]] Adam's Law: Textual Frequency Law | 2026-04-01 | High-frequency textual data preferred for prompting/fine-tuning; 8pp gains from paraphrase selection; CTFT curriculum training |
| [[2604.06628]] Rethinking Generalization in Reasoning SFT | 2026-04-07 | Cross-domain generalization is conditional ("dip-and-recovery"); procedural patterns transfer from toy domains; asymmetric safety degradation |

## Open Problems

- **Algorithmic scope beyond instruction tuning**: DataFlex focuses on instruction tuning and pretraining; extending data-centric methods to RLHF and other paradigms remains underexplored.
- **TFL semantic equivalence assumption**: The textual frequency law assumes perfect semantic equivalence between paraphrases, but paraphrasing inevitably introduces subtle meaning shifts.
- **Safety-reasoning tradeoff**: Long-CoT SFT improves reasoning broadly but degrades safety consistently; understanding how to preserve reasoning gains while mitigating safety degradation is critical.
- **Model capability thresholds**: The conditional generalization paper shows smaller models (1.7B) imitate surface verbosity while larger models (14B+) internalize transferable patterns—what is the minimum model scale for procedural pattern transfer?

## Connections

- [[topics/reinforcement-learning]] — RLSD studies self-distillation in RLVR context; the broader generalization work touches on SFT vs RL trade-offs
- [[topics/reasoning]] — Reasoning SFT and TFL both address chain-of-thought behavior and transfer
- [[topics/data-centric-ai]] — DataFlex is the foundational framework for data-centric LLM training; TFL is itself a data selection principle