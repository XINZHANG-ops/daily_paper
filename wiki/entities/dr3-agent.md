---
title: "DR3-Agent"
slug: dr3-agent
type: framework
paper_count: 1
last_updated: 2026-04-17
---

# DR3-Agent

## What It Is

DR3-Agent is the multi-agent system used in DR3-Eval for evaluating deep research agents. It has a hierarchical architecture designed for complex research tasks, separating planning, retrieval, synthesis, and citation capabilities.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.14683]] | evaluation agent | DR3-Agent is the agent architecture evaluated in DR3-Eval |

## Connections

- [[entities/dr3-eval]] — DR3-Agent is the reference architecture evaluated in DR3-Eval; the benchmark's key findings (longer contexts → performance degradation, hallucination as primary failure mode) were discovered specifically through this agent's hierarchical design, which separates planning, retrieval, and synthesis into distinct components, making failure attribution traceable to specific subsystems rather than treating the agent as a black box
- [[topics/agent-systems]] — DR3-Agent's hierarchical architecture (planning → retrieval → synthesis → citation) represents a design pattern for deep research agents that structures complex multi-step reasoning