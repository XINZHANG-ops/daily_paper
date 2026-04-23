---
title: "Agent-World"
slug: agent-world
type: framework
paper_count: 1
last_updated: 2026-04-21
---

# Agent-World

## What It Is

Agent-World is a general-purpose agent training arena that unifies scalable real-world environment synthesis with continuous self-evolving training. It consists of two tightly coupled components: (1) Agentic Environment-Task Discovery that mines topic-aligned databases and executable tools from the web, synthesizing verifiable tasks with controllable difficulty, and (2) Continuous Self-Evolving Agent Training that combines multi-environment GRPO with a diagnostic arena for co-evolution of agent policies and environments.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18292]] Agent-World | core framework | Agent-World-8B and 14B outperform baselines across 23 agent benchmarks with scaling laws in environment diversity and evolution rounds |

## Connections

- [[entities/grpo]] — GRPO is the RL algorithm used for multi-environment agent training
- [[entities/mcp]] — MCP is the protocol connecting agents with the environment ecosystem
- [[topics/agent-systems]] — Agent-World directly advances general-purpose agent intelligence
- [[topics/reinforcement-learning]] — Self-evolving training uses GRPO-based RL
