---
title: "AgentBench"
slug: agentbench
type: benchmark
paper_count: 1
last_updated: 2026-04-18
---

# AgentBench

## What It Is

AgentBench is a comprehensive benchmark for evaluating LLMs as autonomous agents across 8 interactive environments (web browsing, coding, gaming, database operations, etc.). It evaluates agents based on task completion success rates—whether the agent achieved the specified goal.

Claw-Eval's critique is specific and empirical: AgentBench's **trajectory-opaque scoring** (evaluating only whether the final goal was met, not how it was met) misses 44% of safety violations and 13% of robustness failures that are visible in execution traces. An agent can pass AgentBench by achieving the goal through unsafe intermediate steps, inflating scores relative to real-world deployability. This finding is part of Claw-Eval's broader argument that agent evaluation must include trajectory auditing (execution traces + audit logs + environment snapshots), not just outcome checking.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06132]] Claw-Eval | baseline | AgentBench scores inflated due to trajectory opacity; 44% of safety violations missed |

## Connections

- [[entities/claw-eval]] — Claw-Eval provides transparent trajectory evaluation that reveals what AgentBench's outcome-only scoring misses; the two are complementary if trajectory auditing is added
- [[topics/agent-evaluation]] — AgentBench established the multi-environment agent evaluation paradigm; Claw-Eval's critique is that this paradigm needs trajectory transparency to be trustworthy
- [[topics/agent-systems]] — AgentBench scores inform understanding of agent capabilities, but Claw-Eval shows they must be interpreted with trajectory-level granularity