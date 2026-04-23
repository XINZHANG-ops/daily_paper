---
title: "DR3-Eval"
slug: dr3-eval
type: benchmark
paper_count: 1
last_updated: 2026-04-17
---

# DR3-Eval

## What It Is

DR3-Eval is a benchmark for evaluating Deep Research Agents (DRAs). It addresses the challenge of realistic and reproducible evaluation by combining:
- Authentic multimodal user files
- Controlled static sandbox corpus (supportive documents, distractors, noise)
- Reverse-construction methodology ensuring verifiable solution paths
- Multi-dimensional evaluation framework (Information Recall, Factual Accuracy, Citation Coverage, Instruction Following, Depth Quality)

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14683]] | core method | Benchmark for deep research agent evaluation; Claude Sonnet 4 performs best; hallucination is primary failure mode |

## Key Findings

- Longer contexts lead to performance degradation
- Better instruction following does NOT guarantee factual accuracy
- Hallucination is the primary failure mode across all models
- Significant performance variations across different domains

## Connections

- [[entities/dr3-agent]] — DR3-Agent is the multi-agent system used in the benchmark
- [[topics/agent-evaluation]] — DR3-Eval is a contribution to agent evaluation research