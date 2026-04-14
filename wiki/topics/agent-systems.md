---
title: "Agent Systems"
slug: agent-systems
paper_count: 5
last_updated: 2026-04-14
---

# Agent Systems

## Overview

Agent systems research is rapidly evolving beyond static, single-deployment paradigms toward architectures that support continuous learning, collective improvement, and real-world deployment at scale. The five papers in this topic define the emerging frontiers: world models for internal simulation and long-term memory, collective skill evolution across multi-user deployments, trustworthy evaluation frameworks, real-world web benchmarks, and debugging/tracing infrastructure for code agents.

OpenWorldLib establishes the foundational definition that distinguishes true world models from mere video generation systems, emphasizing three core capabilities: perception of the physical world, action-conditioned simulation, and long-term memory.

CodeTracer reveals a fundamental debugging challenge in code agents: early missteps can trap agents in unproductive loops or cascade into hidden error chains. Its three-stage pipeline (evolving extraction, tree indexing, diagnosis) achieves 46-48% macro F1 in step-level failure localization, and the diagnostic signals enable reflective replay that recovers originally failed runs.

SkillClaw addresses a critical gap in agent deployment: skills remain static after launch despite users encountering similar workflows, tool usage patterns, and failure modes across sessions. The collective skill evolution architecture aggregates interaction trajectories across users, groups evidence by skill, and uses an agentic evolver to perform evidence-driven refinements. The conservative validation mechanism with nighttime evaluation ensures monotonic improvement—the skill pool never degrades while improvements discovered in one context propagate to all users. The substantial gains (+52% Search & Retrieval, +88% Creative Synthesis) demonstrate that cross-user knowledge transfer is both feasible and impactful.

Evaluating agent systems reliably remains an open challenge. Claw-Eval introduces full-trajectory auditing with three independent evidence channels (execution traces, audit logs, environment snapshots) to verify actual behavior rather than trusting self-report. The striking finding that trajectory-opaque evaluation misses 44% of safety violations and 13% of robustness failures exposes fundamental weaknesses in current evaluation practice. ClawBench extends this into real-world web interactions, revealing a substantial capability gap: Claude Sonnet 4.6 achieves 65-75% on OSWorld and WebArena but only 33.3% on real everyday tasks. This benchmark saturation effect suggests existing environments understate the difficulty of real-world deployment.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04707]] OpenWorldLib: A Unified Codebase and Definition of Advanced World Models | 2026-04-05 | Standardized definition of world models with five-core architecture (Operator, Synthesis, Reasoning, Representation, Memory) |
| [[2604.08377]] SkillClaw: Let Skills Evolve Collectively with Agentic Evolver | 2026-04-08 | Collective skill evolution framework with agentic evolver and conservative validation achieving +52-88% gains |
| [[2604.06132]] Claw-Eval: Toward Trustworthy Evaluation of Autonomous Agents | 2026-04-06 | Full-trajectory auditing with multi-dimensional scoring revealing 44% safety violations missed by opaque evaluation |
| [[2604.08523]] ClawBench: Can AI Agents Complete Everyday Online Tasks? | 2026-04-08 | Real-world web benchmark exposing 35+ point gap between existing benchmarks and live website performance |
| [[2604.11641]] CodeTracer: Towards Traceable Agent States | 2026-04-14 | Hierarchical tracing for code agents with evolving extraction, tree indexing, and diagnosis; 46-48% macro F1 failure localization |

## Open Problems

- **Evaluation validity**: How can we build benchmarks that accurately predict real-world agent performance without requiring live website evaluation with its safety complexities?
- **Skill generalization boundaries**: When does collective skill evolution break down—when skills are too context-specific, or when environments diverge significantly?
- **World model architectural requirements**: The gap between next-frame prediction and language model pre-training suggests fundamental architectural changes may be needed for ideal world models.
- **Multi-modal agent reliability**: Video tasks remain substantially harder than document/image or code tasks for current agents, with Claude Opus/Sonnet 4.6 achieving only 15.4% consistency on video benchmarks.
- **Code agent debugging**: How to scale failure diagnosis across heterogeneous agent run directories without brittle hardcoded parsers

## Connections

- [[topics/benchmarks]] — Claw-Eval and ClawBench provide evaluation infrastructure for agent systems research
- [[topics/embodied-ai]] — HY-Embodied-0.5 provides embodied foundation models that align with the world model definition
- [[topics/reinforcement-learning]] — Agentic RL training methods like RLSD and RAGEN-2 inform how agent capabilities are developed
- [[topics/code-agents]] — CodeTracer directly addresses debugging and failure localization challenges specific to code agents