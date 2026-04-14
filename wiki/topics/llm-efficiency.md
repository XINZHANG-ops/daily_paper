---
title: "LLM Efficiency"
slug: llm-efficiency
paper_count: 2
last_updated: 2026-04-13
---

# LLM Efficiency

## Overview

The two papers in this topic address complementary aspects of LLM inference efficiency: memory-bound KV cache compression during generation, and the asymmetric prefill/decode costs in tool-integrated reasoning. **TriAttention** identifies a fundamental flaw in existing KV cache compression methods: they estimate token importance from post-RoPE attention scores, but queries rotate with position during RoPE, creating only a tiny observation window that causes poor top-key selection and unstable reasoning. The key discovery is "Q/K concentration" in pre-RoPE space—Q and K vectors are highly concentrated around fixed non-zero centers and remain stable across positions, enabling attention to follow predictable distance preferences via a trigonometric series. This allows reliable key importance estimation from stable Q/K centers rather than volatile post-RoPE observations. TriAttention achieves 2.5x higher throughput or 10.7x KV memory reduction while matching Full Attention accuracy on AIME25, and enables deployment of Qwen3-32B (INT4) on a single RTX 4090 (24GB) where Full Attention causes OOM.

**Beyond Accuracy** identifies a critical blind spot in Tool-Integrated Reasoning (TIR) evaluation: accuracy benchmarks are well-established but efficiency metrics are largely absent. Existing metrics like token counts and tool-call counts fail to capture the asymmetric costs of compute-bound prefill and memory-bound decode phases, particularly KV-Cache eviction during tool calls and the memory overhead from long tool responses. The paper introduces PTE (Prefill Token Equivalents), a hardware-aware metric that unifies internal reasoning and external tool-use costs by modeling the prefill-decode asymmetry inherent in transformer inference. PTE achieves r=0.9253 correlation with wall-clock latency vs r=-0.3750 for naive token counts, validated on an 8xH200 cluster with 256 parallel requests. The paper identifies four inefficiency patterns (Confirmatory Tool Usage, Tool-Mixing, Lack of Tool Priors, Tool Format Collapse) with cost multipliers ranging from 1.77x to 2.42x, with a striking finding that trajectories with higher PTE costs tend to have lower reasoning correctness.

Together, these papers reveal that inference efficiency is not a single dimension—it involves KV cache management in autoregressive generation (TriAttention) and the asymmetric cost structure of multi-turn tool use (Beyond Accuracy). Both papers validate across multiple architectures and benchmarks, suggesting their findings generalize beyond specific models or tasks.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04921]] TriAttention: Efficient Long Reasoning with Trigonometric KV Compression | 2026-04-05 | Q/K concentration discovery enables trigonometric series scoring; 2.5x throughput or 10.7x KV memory reduction at equivalent accuracy; enables Qwen3-32B on single RTX 4090 |
| [[2604.05404]] Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning | 2026-04-06 | PTE metric (r=0.9253 with wall-clock latency); four inefficiency patterns with 1.77x-2.42x cost multipliers; higher PTE correlates with lower correctness |

## Open Problems

- **Dedicated inference kernels**: TriAttention's trigonometric series computation and cache pruning could be optimized with hardware-aware kernels not yet developed.
- **PTE generalization**: PTE measures transformer computation, omitting real-world costs like API latency; validation was limited to specific tasks and models.
- **Thinking mode over-thinking**: Beyond Accuracy shows thinking mode is beneficial on AIME25 (1.8x PTE for +16.7% accuracy) but harmful on SimpleQA (4.2x PTE for -3.4% accuracy)—understanding when thinking is justified remains open.
- **Cross-domain KV compression**: TriAttention validates on mathematical reasoning; evaluation on coding and agentic tasks beyond math is needed.

## Connections

- [[topics/kv_cache_compression]] — TriAttention is the landmark method for KV cache compression via trigonometric scoring
- [[topics/tool-integrated-reasoning]] — Beyond Accuracy is the foundational paper for inefficiency analysis in tool-augmented reasoning
- [[topics/llm-training]] — RLSD addresses efficiency in reasoning training; TriAttention's long-context scenarios benefit from efficient inference