---
title: "Tool-Integrated Reasoning"
slug: tool-integrated-reasoning
paper_count: 1
last_updated: 2026-04-08
---

# Tool-Integrated Reasoning

## Overview

Tool-Integrated Reasoning (TIR) enables LLMs to use external tools (search, code execution, file operations) to augment their reasoning capabilities. While accuracy benchmarks for TIR are well-established, efficiency metrics that reflect real-world inference latency have been largely absent. Existing metrics like token counts and tool-call counts fail to capture the asymmetric costs of compute-bound prefill and memory-bound decode phases, particularly the KV-cache eviction during tool calls and the memory overhead from long tool responses that inflate context length. This blind spot means researchers may optimize for accuracy while introducing severe efficiency regressions that make deployment impractical.

The paper introduces PTE (Prefill Token Equivalents) as a hardware-aware metric that unifies internal reasoning and external tool-use costs by modeling prefill-decode asymmetry. PTE achieves r=0.9253 correlation with wall-clock latency compared to r=-0.3750 for naive token counts, maintaining consistent model efficiency rankings across diverse hardware profiles (Spearman ρ>0.95 across H100, H200, A100, RTX 4090, V100). The metric's insight is that decode phase costs grow with cumulative context length Lseq, not just current token generation—so tool calls that evict KV-cache force recomputation while long intermediate outputs make every subsequent decode step more expensive. This models reality more accurately than token counts.

Four inefficiency patterns are identified and quantified: Confirmatory Tool Usage (1.77x multiplier, 81% frequency) where models solve problems internally then call tools to "verify" known results; Tool-Mixing (2.42x multiplier, 59% frequency) where trajectories use multiple distinct tool types without accuracy benefit; Lack of Tool Priors (2.15x multiplier, 33% frequency) where tool calls return empty output due to missing print statements; and Tool Format Collapse (2.42x multiplier, 100% frequency) where models use incompatible tool formats from training. Strikingly, trajectories with higher PTE costs tend to have lower reasoning correctness—the quality-efficiency tradeoff is negative, meaning inefficiency is not just costly but actively harmful to reasoning quality.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.05404]] Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning | 2026-04-06 | PTE metric with r=0.9253 latency correlation; identifies four inefficiency patterns with 1.77x-2.42x cost multipliers; reveals negative quality-efficiency tradeoff in TIR |

## Open Problems

- PTE omits real-world costs like API latency and network transmission, limiting accuracy in production deployments
- The γ coefficient (decode-to-prefill cost ratio) is a simplified abstraction that may not capture hardware-specific optimizations
- Generalizability of the low PTE-high quality correlation requires further exploration across models and tasks
- The interaction between thinking mode and tool use efficiency (AIME benefits 1.8x PTE for +16.7% accuracy; SimpleQA costs 4.2x PTE for -3.4% accuracy) suggests task-dependent optimal strategies

## Connections

- [[topics/llm-efficiency]] — PTE extends the hardware-aware efficiency analysis to tool-augmented reasoning contexts
- [[topics/agent-evaluation]] — Claw-Eval's agent evaluation framework could incorporate PTE to measure both capability and efficiency