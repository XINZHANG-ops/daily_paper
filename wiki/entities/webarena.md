---
title: "WebArena"
slug: webarena
type: benchmark
paper_count: 3
last_updated: 2026-04-20
---

# WebArena

## What It Is

WebArena is a benchmark for evaluating web-based autonomous agents on realistic tasks across multiple websites. It provides sandboxed environments where agents must navigate live websites, search for information, fill forms, and complete multi-step workflows. In the April 2026 literature, WebArena serves as the primary baseline for comparing sandbox-based agent evaluation against real-world task evaluation.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06132]] | baseline | One of the benchmarks Claw-Eval evaluates across 300 tasks and 14 models |
| [[2604.08523]] | benchmark comparison | Achieves 65-75% success rates in sandboxed environments; ClawBench argues these rates don't reflect real-world performance because sandbox tasks lack the complexity and consequence of live production websites |
| [[2604.10866]] | baseline | Referenced as part of the agent evaluation landscape that OccuBench extends with professional domain coverage |

## Connections

- [[entities/osworld]] — Complementary sandbox benchmark: WebArena focuses on web tasks, OSWorld on operating system tasks. Both achieve high scores (65-75%) in controlled environments that ClawBench argues overestimate real-world capability
- [[entities/claw-eval]] — Claw-Eval's trajectory-opaque evaluation finding helps explain why WebArena's scores may be inflated: sandbox benchmarks miss safety and robustness failures that only appear under real-world fault conditions
- [[topics/agent-evaluation]] — WebArena represents the "sandbox benchmark" generation that newer frameworks (ClawBench, OccuBench) argue is insufficient for measuring true agent capability
- [[topics/agent-systems]] — WebArena tasks require the same core agent capabilities (planning, tool use, error recovery) that agent-systems research seeks to improve
