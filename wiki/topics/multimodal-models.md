---
title: "Multimodal Models"
slug: multimodal-models
paper_count: 13
last_updated: 2026-04-21
---

# Multimodal Models

## Overview

Unified multimodal models aim to process text, images, and other modalities within a single architecture. The papers reveal a critical issue: **pseudo-unification** where despite shared parameters, text generation shows high-entropy creativity while image synthesis enforces low-entropy fidelity. The root cause is modality-asymmetric encoding and pattern-split responses.

The key insight is that true unification requires consistent information flow, not just shared parameters.

## Evolution

Early April 2026, Think in Strokes used BAGEL as base for process-driven image generation. By mid-April, Pseudo-Unification analyzed 10 unified multimodal models and found that most suffer from pseudo-unification—only Harmon achieves genuine unification. Seedance 2.0 showed native multi-modal audio-video processing. On April 21, EMF (Extending MeanFlow to T2I) demonstrated that bridging text representations with visual generation requires text encoders with high discriminability and disentanglement—new properties beyond those needed for language-only tasks.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04746]] Think in Strokes | 2026-04-09 | Process-driven generation on unified multimodal backbone |
| [[2604.03128]] Self-Distilled RLVR | 2026-04-08 | Multimodal reasoning via token-level credit assignment |
| [[2604.07430]] HY-Embodied-0.5 | 2026-04-10 | Mixture-of-Transformers for embodied multimodal |
| [[2604.02327]] SteerViT | 2026-04-06 | Steerable frozen ViT via gated cross-attention |
| [[2604.07823]] LPM 1.0 | 2026-04-13 | Character animation with interleaved audio-video |
| [[2604.02317]] SIMPLESTREAM | 2026-04-06 | Simple sliding window for streaming multimodal |
| [[2604.08546]] NUMINA | 2026-04-10 | Counting alignment in text-to-video models |
| [[2604.10949]] Pseudo-Unification | 2026-04-14 | Entropy probing reveals divergent text/image behaviors |
| [[2604.14148]] Seedance 2.0 | 2026-04-16 | Native audio-video processing for state-of-the-art |
| [[2604.05015]] Video-MME-v2 | 2026-04-08 | Video understanding benchmark with multimodal consistency |
| [[2604.11626]] RationalRewards | 2026-04-17 | Reasoning rewards scale both training and test time |
| [[2604.11804]] OmniShow | 2026-04-14 | Human-object interaction video generation |
| [[2604.18168]] EMF | 2026-04-21 | Text-conditioned MeanFlow generation with discriminative text representations |

## Patterns & Insights

- **Shared parameters ≠ unified**: Modality-asymmetric encoding causes pseudo-unification
- **Entropy reveals divergence**: Text (high entropy) vs image (low entropy) in same model
- **Contextual prediction helps**: Harmon succeeds because it predicts context for both modalities
- **Text representations need discriminability**: For text-to-image generation, text encoders must have high discriminability and disentanglement

## Open Problems

- Detecting pseudo-unification in deployed models
- Architecture modifications to ensure true unification
- Evaluating multimodal synergy beyond individual task performance

## Connections

- [[topics/reasoning]] — Multimodal reasoning requires consistent information flow
- [[entities/bagel]] — Used in process-driven generation, revealed to have pseudo-unification
- [[entities/harmon]] — Only unified multimodal model achieving genuine unification