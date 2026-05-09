---
title: "OSWorld"
slug: osworld
type: benchmark
paper_count: 3
last_updated: 2026-04-20
---

# OSWorld

## What It Is

OSWorld is a benchmark for evaluating operating system agents that interact with real computer environments through graphical user interfaces. Agents must perform tasks across multiple applications (browsers, file managers, terminals) by observing screenshots and emitting keyboard and mouse actions. Like WebArena, OSWorld operates in sandboxed environments and achieves high success rates (65-75%) that newer benchmarks argue overestimate real-world capability.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06132]] | baseline | One of the benchmarks evaluated in Claw-Eval's 300-task, 14-model comparison |
| [[2604.08523]] | benchmark comparison | Achieves 65-75% success in sandboxed OS tasks; ClawBench demonstrates that these scores don't translate to live production website tasks where even the best model achieves only 33.3% |
| [[2604.10866]] | baseline | Referenced in the agent evaluation landscape that OccuBench extends to professional domains |

## Connections

- [[entities/webarena]] — Complementary sandbox benchmark: OSWorld tests operating system tasks, WebArena tests web tasks. Both share the same limitation of high sandbox scores (65-75%) that don't reflect real-world performance
- [[entities/claw-eval]] — Claw-Eval's finding that trajectory-opaque evaluation misses 44% of safety violations explains why OSWorld's sandbox scores may be inflated relative to real-world agent reliability
- [[topics/agent-evaluation]] — OSWorld represents the second generation of agent benchmarks (after text-only) that added visual observation, but still operates in controlled environments unlike the latest real-world evaluation frameworks
- [[topics/agent-systems]] — OSWorld tasks require cross-application coordination and GUI manipulation, core capabilities for general-purpose agent systems
