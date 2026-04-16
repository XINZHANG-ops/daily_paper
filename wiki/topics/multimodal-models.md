---
title: "Multimodal Models"
slug: multimodal-models
paper_count: 4
last_updated: 2026-04-16
---

# Multimodal Models

## Overview

Unified multimodal models aim to process text, images, and other modalities within a single architecture. The papers reveal a critical issue: **pseudo-unification** where despite shared parameters, text generation shows high-entropy creativity while image synthesis enforces low-entropy fidelity. The root cause is modality-asymmetric encoding and pattern-split responses.

The key insight is that true unification requires consistent information flow, not just shared parameters.

## Evolution

Early April 2026, Think in Strokes used BAGEL as base for process-driven image generation, showing strong capabilities. By mid-April, Pseudo-Unification analyzed 10 unified multimodal models and found that most suffer from pseudo-unification—only Harmon (using contextual prediction for both modalities) achieves genuine unification. Seedance 2.0 then showed that native multi-modal audio-video processing can achieve state-of-the-art across multiple generation tasks.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04746]] Think in Strokes | 2026-04-09 | Process-driven generation on unified multimodal backbone |
| [[2604.10949]] Pseudo-Unification | 2026-04-14 | Entropy probing reveals divergent text/image behaviors |
| [[2604.14148]] Seedance 2.0 | 2026-04-16 | Native audio-video processing for state-of-the-art |

## Patterns & Insights

- **Shared parameters ≠ unified**: Modality-asymmetric encoding causes pseudo-unification
- **Entropy reveals divergence**: Text (high entropy) vs image (low entropy) in same model
- **Contextual prediction helps**: Harmon succeeds because it predicts context for both modalities

## Open Problems

- Detecting pseudo-unification in deployed models
- Architecture modifications to ensure true unification
- Evaluating multimodal synergy beyond individual task performance

## Connections

- [[topics/reasoning]] — Multimodal reasoning requires consistent information flow
- [[entities/bagel]] — Used in process-driven generation, revealed to have pseudo-unification
- [[entities/harmon]] — Only unified multimodal model achieving genuine unification