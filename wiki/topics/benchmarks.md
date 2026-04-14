---
title: "Benchmarks"
slug: benchmarks
paper_count: 3
last_updated: 2026-04-10
---

# Benchmarks

## Overview

Benchmark research in this period reflects a maturation of the field, moving from simple task accuracy measurements toward nuanced evaluation frameworks that capture consistency, reliability, and ecological validity. Three papers define the frontier: video understanding with group-based evaluation, agent evaluation with full-trajectory auditing, and real-world web task benchmarks.

Video-MME-v2 introduces a progressive tri-level capability hierarchy (visual information aggregation, temporal dynamics, complex reasoning) paired with a group-based evaluation strategy that enforces consistency across related queries. The key insight is that inflated leaderboard scores mask a widening gap: Gemini-3-Pro achieves 49.4 Non-Lin Score while human experts reach 90.7. More critically, the benchmark reveals that thinking-based reasoning improves performance with subtitles but can degrade it in purely visual settings—exposing models' over-reliance on language priors rather than true visual understanding. The hierarchical bottleneck pattern (errors in lower levels propagate upward) suggests holistic capability enhancement is needed rather than targeted reasoning improvements.

Claw-Eval addresses evaluation opacity by introducing full-trajectory auditing across three independent evidence channels: execution traces, audit logs, and environment snapshots. The framework reveals that trajectory-opaque evaluation (checking only final outputs) misses 44% of safety violations and 13% of robustness failures. The multi-dimensional scoring structure (Completion, Safety, Robustness) with a multiplicative safety gate ensures agents cannot shortcut safety through high completion scores. Error injection experiments show that while Pass@3 (capability ceiling) remains stable, Pass^3 (reliability floor) drops sharply—exposing the capability-reliability divide that simple accuracy metrics hide.

ClawBench extends evaluation into real-world everyday web interactions across 153 tasks on 144 live platforms, introducing a lightweight Chrome extension with CDP-based interception that safely evaluates on production websites by blocking only the final submission request. The five-layer recording infrastructure (session replay, action screenshots, HTTP traffic, agent messages, browser actions) enables both automated evaluation and deep post-hoc failure diagnosis. Most striking is the benchmark saturation effect: models achieving 65-75% on OSWorld and WebArena perform dramatically worse on real-world tasks (Claude Sonnet 4.6 at 33.3%, GPT-5.4 at 6.5%), indicating that existing benchmarks poorly predict real-world capability.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.05015]] Video-MME-v2: Towards the Next Stage in Benchmarks for Comprehensive Video Understanding | 2026-04-05 | Group-based evaluation with Non-Lin scoring revealing 41.3-point gap to human experts; exposes language prior over-reliance |
| [[2604.06132]] Claw-Eval: Toward Trustworthy Evaluation of Autonomous Agents | 2026-04-06 | Full-trajectory auditing with three evidence channels exposing 44% safety violations missed by opaque evaluation |
| [[2604.08523]] ClawBench: Can AI Agents Complete Everyday Online Tasks? | 2026-04-08 | 153 real-world tasks on 144 live platforms with safe interception, revealing 35+ point gap from existing benchmarks |

## Open Problems

- **Benchmark ecological validity**: The large gaps between sandbox benchmarks and real-world performance suggest we need better ways to predict deployment capability without live website risks.
- **Multilingual coverage**: Current benchmarks focus primarily on English; extending to diverse languages remains future work.
- **Robustness beyond error injection**: Error injection patterns (rate limits, server errors, latency spikes) capture only a subset of real-world failure modes.
- **Video understanding ceiling**: Even the best models achieve only 15.4% consistency on video tasks—frame sampling, temporal reasoning, and OCR remain fundamentally challenging.

## Connections

- [[topics/agent-systems]] — Claw-Eval and ClawBench provide evaluation infrastructure for agent systems
- [[topics/video-generation]] — Video understanding benchmarks like Video-MME-v2 drive video generation research
- [[topics/reinforcement-learning]] — Benchmark insights (like the capability-reliability divide) inform RL training strategies