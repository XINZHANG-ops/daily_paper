---
title: "Agent Evaluation"
slug: agent-evaluation
paper_count: 3
last_updated: 2026-04-14
---

# Agent Evaluation

## Overview

Agent evaluation has emerged as a critical challenge as autonomous AI systems become capable of complex multi-step tasks. Three papers now address systematic evaluation weaknesses: Claw-Eval exposes trajectory-opaque grading failures, ClawBench reveals the gap between sandbox benchmarks and real-world performance, and CodeTracer provides infrastructure for debugging failed trajectories.

CodeTracer (2604.11641) addresses the diagnostic challenge: given a failed agent run, where did it first go wrong and why? Its CodeTraceBench contains 3,326 annotated trajectories spanning 5 backbones and 4 frameworks. The key finding is that agents exhibit an "evidence-to-action gap"—they gather relevant information but fail to translate it into correct state-changing actions. This manifests as the ineffective action fraction nearly doubling from solved (22%) to unsolved (40%) runs.

Claw-Eval (2604.06132) identifies three systemic gaps in agent evaluation: trajectory-opaque grading that only checks final outputs without examining execution traces, underspecified safety and robustness evaluation that occurs in artificial rather than genuine task-completion contexts, and narrow modality coverage that fails to capture the breadth of real-world agent deployments. The paper demonstrates that trajectory-opaque evaluation misses 44% of safety violations and 13% of robustness failures—errors that would be caught by examining what the agent actually did versus what it reported. This triangulation of execution traces, audit logs, and environment snapshots transforms evaluation from trusting self-report to verifying actual behavior.

ClawBench (2604.08523) reveals a substantial gap between benchmark performance and real-world capability: Claude Sonnet 4.6 achieves 65-75% on OSWorld and WebArena but only 33.3% on ClawBench, while GPT-5.4 drops from similar scores to just 6.5%. This gap exists because existing benchmarks evaluate agents in offline sandboxes with static HTML and fixed DOM structures, or restrict evaluation to read-only information retrieval—removing exactly the complexities that make real-world web interaction difficult (cookie consent popups, dynamic JavaScript rendering, multi-step interaction chains, anti-bot defenses). The benchmark's 153 everyday online tasks across 144 live platforms fill a critical gap in evaluating write-heavy, state-changing workflows that people accomplish regularly.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.06132]] Claw-Eval: Toward Trustworthy Evaluation of Autonomous Agents | 2026-04-06 | Full-trajectory auditing with three evidence channels; multi-dimensional scoring (Completion, Safety, Robustness); reveals 44% of safety violations missed by trajectory-opaque evaluation |
| [[2604.08523]] ClawBench: Can AI Agents Complete Everyday Online Tasks? | 2026-04-08 | 153 real-world tasks on 144 live platforms; safe live-website evaluation via submission interception; shows 35+ point gap between existing benchmark saturation and real-world performance |
| [[2604.11641]] CodeTracer: Towards Traceable Agent States | 2026-04-14 | CodeTraceBench with 3,326 annotated trajectories; step-level failure localization achieving 46-48% macro F1; evidence-to-action gap analysis |

## Open Problems

- Multilingual coverage remains absent from both benchmarks, limiting evaluation of agents deployed globally
- Video understanding tasks remain the hardest challenge (10.7% average Pass^3 vs 32.3% for document/image), suggesting current multimodal architectures struggle with temporal reasoning over frames
- The safety-robustness tradeoff under genuine task-completion pressure versus artificial red-teaming requires deeper investigation
- Extending to mobile and desktop agent evaluation beyond browser-based web agents
- Diagnosing failures in longer-horizon tasks where early errors compound over many steps

## Connections

- [[topics/benchmarks]] — Both Claw-Eval and ClawBench represent new generations of benchmark design for agent systems
- [[topics/skill-evolution]] — SkillClaw's WildClawBench evaluation connects to this topic; agents that can evolve skills need better evaluation frameworks
- [[topics/code-agents]] — CodeTracer's debugging and failure localization is directly relevant to evaluating code agent capabilities