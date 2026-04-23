---
title: "LLM Efficiency"
slug: llm-efficiency
paper_count: 3
last_updated: 2026-04-18
---

# LLM Efficiency

## Overview

LLM efficiency addresses the challenge of deploying large models at reasonable memory and compute costs. Key techniques include KV cache compression, inference budget measurement, and cost-aware decoding.

## Evolution

Early to mid-April 2026, three papers established the efficiency landscape from different angles. TriAttention (2604.04921) introduced trigonometric KV cache compression achieving 10.7x memory reduction while maintaining accuracy on math benchmarks. Beyond Accuracy (2604.05404) revealed that standard token-count metrics are fundamentally misleading (r=-0.375 with latency) and introduced PTE as a hardware-aware alternative (r=0.925). MEDS (2604.11297) then applied efficiency thinking to RL training through memory-enhanced reward shaping, showing that efficiency is relevant not just for inference but for training as well. Together they suggest that memory efficiency and runtime efficiency are related but distinct problems requiring different solutions.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04921]] TriAttention | 2026-04-07 | Trigonometric KV cache compression for long-context reasoning |
| [[2604.05404]] Beyond Accuracy | 2026-04-08 | PTE metric and inefficiency patterns in tool-integrated reasoning |
| [[2604.11297]] MEDS | 2026-04-16 | Memory-enhanced reward shaping |

## Patterns & Insights

- **KV cache compression**: Reduces memory footprint without sacrificing performance
- **Inference budget measurement**: PTE framework reveals where compute goes
- **Sampling as optimization**: Cost-aware decoding enables inference efficiency

## Connections

- [[topics/llm-training]] — Efficiency affects training and deployment
- [[topics/kv-cache-compression]] — KV compression is a specific efficiency technique
- [[topics/reasoning]] — Long-context reasoning is primary use case