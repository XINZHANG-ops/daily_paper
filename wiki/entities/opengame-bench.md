---
title: "OpenGame-Bench"
slug: opengame-bench
type: benchmark
paper_count: 1
last_updated: 2026-04-21
---

# OpenGame-Bench

## What It Is

OpenGame-Bench is an evaluation pipeline for agentic game generation, measuring three dimensions: Build Health (compilation/runtime stability), Visual Usability (rendering coherence), and Intent Alignment (requirement satisfaction). Unlike static code tests, it uses headless browser execution and VLM judging to assess dynamic playability.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18394]] OpenGame | evaluation | 150 diverse game prompts across 5 genres; measures BH/VU/IA via headless browser + VLM judge |

## Connections

- [[2604.18394]] — The primary evaluation benchmark for OpenGame; provides the first systematic assessment of agentic game generation capabilities
- [[2604.08523]] ClawBench — Both evaluate agents in interactive software domains; ClawBench measures everyday task agents while OpenGame-Bench measures code generation quality
- [[topics/agent-evaluation]] — OpenGame-Bench exemplifies the shift from static benchmarks to dynamic execution-based evaluation
