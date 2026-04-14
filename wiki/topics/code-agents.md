---
title: "Code Agents"
slug: code-agents
paper_count: 1
last_updated: 2026-04-14
---

# Code Agents

## Overview

Code agents are LLM-powered systems that autonomously interact with software repositories and development environments to solve complex engineering tasks such as repository-level bug fixing and system configuration. CodeTracer (2604.11641) reveals that these agents face a fundamental debugging challenge: early missteps can trap agents in unproductive loops or cascade into hidden error chains, making it hard to tell when and why the agent goes off track. Analyzing 3,326 trajectories across 5 backbones and 4 agent frameworks, the paper uncovers consistent behavioral patterns that define the current capabilities and limitations of code agents.

The evidence-to-action gap emerges as a critical finding: across all five models tested, the ineffective action fraction nearly doubles from solved (22%) to unsolved (40%) runs, while correct state changes drop from 30% to 21%. This suggests agents successfully gather relevant information through exploration but fail to translate it into effective state-changing actions—a comprehension bottleneck rather than an information retrieval problem. This pattern held across all backbone models, with Qwen3-Coder-480B and Kimi-K2-Instruct showing the sharpest drops (11.7 and 10.3 percentage points respectively).

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.11641]] CodeTracer: Towards Traceable Agent States | 2026-04-14 | Hierarchical tracing architecture with evolving extraction, tree indexing, and diagnosis; 46-48% macro F1 in step-level failure localization; evidence-to-action gap analysis across 5 backbones |

## Open Problems

- **Early failure detection**: How can we detect and prevent the initial wrong commitment before it cascades into downstream errors?
- **Reflection strategies**: What reflective replay strategies are most effective for recovering from failures under matched budgets?
- **Agent design efficiency**: Why does architectural complexity (SWE-Agent, OpenHands at 2× token cost of MiniSWE-Agent) yield only modest success gains?
- **Industrial vs academic agents**: Industrial agents like Claude Code employ richer tooling (40+ specialized tools) and parallel execution, introducing ordering-sensitivity issues absent from sequential academic frameworks

## Connections

- [[topics/agent-systems]] — Code agents are a major application within the broader agent systems landscape
- [[topics/agent-evaluation]] — CodeTraceBench and trajectory analysis methodology connect to trustworthy agent evaluation
- [[topics/benchmarks]] — SWE-bench, TerminalBench provide the evaluation infrastructure for code agent research