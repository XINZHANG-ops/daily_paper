---
title: "Knowledge Distillation"
slug: knowledge-distillation
paper_count: 1
last_updated: 2026-04-18
---

# Knowledge Distillation

## Overview

Knowledge distillation transfers capabilities from larger (teacher) models to smaller (student) models. Key insight: thinking-pattern consistency between teacher and student is critical for successful transfer.

## Evolution

Mid-April 2026, Rethinking On-Policy Distillation (2604.13016) revealed that OPD fails when teacher-student consistency breaks down—not through random error but through systematic pattern divergence. The paper showed that on-policy constraints create an inherent tension: the more the student improves, the more it diverges from the teacher distribution, degrading the distillation signal. This connects to the broader RLVR theme where multiple independent failure modes (credit assignment, signal quality, pattern consistency) compound during training.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.13016]] Rethinking OPD | 2026-04-15 | On-policy distillation failure conditions and recovery |

## Patterns & Insights

- **Distillation ≠ mere imitation**: Genuine new knowledge transfer requires compatible thinking patterns
- **On-policy constraints**: Teacher-student consistency matters for on-policy settings

## Connections

- [[topics/llm-training]] — Distillation is a post-training approach
- [[topics/reasoning]] — Reasoning pattern transfer is especially challenging