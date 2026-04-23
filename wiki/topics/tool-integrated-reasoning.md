---
title: "Tool-Integrated Reasoning"
slug: tool-integrated-reasoning
paper_count: 1
last_updated: 2026-04-16
---

# Tool-Integrated Reasoning

## Overview

Tool-Integrated Reasoning (TIR) enables LLMs to use external tools during reasoning. The papers reveal that **inference efficiency in TIR is fundamentally different from accuracy**—PTE achieves r=0.925 correlation with wall-clock latency while raw token counts show r=-0.375. Four specific inefficiency patterns are identified: Confirmatory Tool Usage, Redundant Tool Usage, Tool-Mixing, and Superfluous Tool Usage, each with 1.77x-2.42x cost multipliers.

## Evolution

Mid-April 2026, Beyond Accuracy established that TIR efficiency is orthogonal to accuracy—inefficient strategies are counterproductive, not just costly. The PTE metric revealed that prefill/decode asymmetry dominates memory-bound decode costs, and that token counts are misleading (r=-0.375 correlation with latency). This shifted focus from accuracy optimization to inference efficiency in tool-augmented reasoning.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.05404]] Beyond Accuracy | 2026-04-08 | PTE metric and 4 inefficiency patterns in tool-integrated reasoning |

## Patterns & Insights

- **Token counts are misleading**: r=-0.375 correlation with actual latency
- **Four inefficiency patterns**: Confirmatory, Redundant, Mixing, Superfluous tool usage
- **Higher PTE = lower correctness**: Inefficient strategies are counterproductive, not just costly
- **Prefill/decode asymmetry dominates**: Memory-bound decode costs grow with cumulative context

## Open Problems

- Developing methods to automatically detect and correct inefficiency patterns
- Designing TIR strategies that minimize PTE while maintaining accuracy
- Extending PTE analysis to multi-turn agent scenarios

## Connections

- [[topics/llm-efficiency]] — TIR efficiency is a key deployment concern
- [[topics/agent-systems]] — Tool use is central to agent capabilities
- [[topics/reasoning]] — TIR is a reasoning-specific efficiency challenge
