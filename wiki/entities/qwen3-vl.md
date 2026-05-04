---
title: "Qwen3-VL"
slug: qwen3-vl
type: model
paper_count: 1
last_updated: 2026-04-17
---

# Qwen3-VL

## What It Is

Qwen3-VL is a multimodal vision-language model from Alibaba's Qwen family. In the RationalRewards paper, Qwen3-VL-32B-Instruct serves as the teacher model for PARROT training, generating high-quality rationales anchored to preference labels.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.11626]] | teacher model | Qwen3-VL-32B-Instruct provides rationale generation as teacher; 8B RationalRewards outperforms direct use of 32B model as judge |

## Connections

- [[entities/rationalrewards]] — RationalRewards is distilled from Qwen3-VL-32B; the distilled 8B model outperforms the 32B teacher as a judge, demonstrating that rationale-anchored distillation can produce smaller models with superior evaluation capability
- [[entities/parrot]] — PARROT uses Qwen3-VL as the teacher model for generating structured rationales anchored to preference labels; Qwen3-VL's strong multimodal reasoning makes it an effective rationale generator for visual generation reward modeling