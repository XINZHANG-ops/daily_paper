---
title: "SWE-bench"
slug: swe-bench
type: benchmark
paper_count: 2
last_updated: 2026-04-20
---

# SWE-bench

## What It Is

SWE-bench is a benchmark for evaluating software engineering agents on resolving real GitHub issues. It tests an agent's ability to understand a bug report, navigate a codebase, implement a fix, and verify the fix passes the relevant tests. In the April 2026 literature, SWE-bench serves as the canonical code-agent benchmark alongside web-task and general-agent evaluations.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.06132]] | baseline | One of the benchmarks in Claw-Eval's 300-task evaluation; measures code-agent capability within the broader agent evaluation framework |
| [[2604.10866]] | baseline | Referenced as part of the agent evaluation landscape; OCCUBENCH extends benchmark coverage from public code repositories to professional workplace scenarios across 10 industries |

## Connections

- [[entities/claw-eval]] — Claw-Eval includes SWE-bench tasks in its 300-task cross-modal evaluation, revealing that no single model dominates all modalities—each domain (Video, Doc & Image, Code) has a different leader
- [[topics/code-agents]] — SWE-bench is the canonical evaluation for code agents, testing bug resolution across real codebases; CodeTracer's evidence-to-action gap diagnosis complements SWE-bench's task-completion metric
- [[topics/agent-evaluation]] — SWE-bench represents the "public repository" evaluation paradigm that OCCUBENCH argues is insufficient: professional software engineering requires access to enterprise systems with no public APIs
- [[topics/agent-systems]] — SWE-bench tasks require long-horizon planning, tool use (git, test runners, editors), and error recovery—core general-agent capabilities
