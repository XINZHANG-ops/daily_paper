---
title: "Document Parsing"
slug: document-parsing
paper_count: 1
last_updated: 2026-04-13
---

# Document Parsing

## Overview

Document parsing—the extraction of text, formulas, tables, and their spatial relationships from images of documents—sits at the foundation of virtually every AI-powered workflow that processes PDFs: RAG pipelines, knowledge base construction, financial report analysis, legal document review, and scientific literature ingestion. Despite rapid progress in OCR and layout detection, parsing complex documents (nested tables, multi-column layouts with floating elements, dense mathematical notation, mixed-language content) remains genuinely hard. OmniDocBench v1.6, the standard benchmark, shows that even frontier models drop measurable performance on its Hard subset, and state-of-the-art accuracy on complex documents still lags far behind human transcription quality.

MinerU2.5-Pro (2604.04771) delivers the most striking result in recent document parsing work: a 2.71-point improvement over its same-architecture baseline purely through data engineering—without any architectural change or additional parameters. The paper's core argument is that performance bottlenecks in document parsing stem not from inadequate model capacity but from shared deficiencies in training data. By analyzing failure modes across diverse architectures and parameter scales, the authors find that models exhibit highly consistent errors on the same hard samples. This leads them to a data-centric approach that expands training data from under 10M to 65.5M samples while improving annotation quality through three co-designed components: Diversity-and-Difficulty-Aware Sampling (DDAS), Cross-Model Consistency Verification (CMCV), and a Judge-and-Refine annotation pipeline. The result is 95.69 on OmniDocBench v1.6 Full, 96.12 on Base, and notably 94.08 on the Hard subset—surpassing Gemini 3 Pro and Qwen3-VL-235B despite using far fewer parameters.

The methodological contribution of MinerU2.5-Pro is the three-stage progressive training strategy that sequentially exploits data quality tiers: large-scale pre-training on 65.5M auto-annotated samples, hard-sample fine-tuning on 192K expert-annotated examples with replay, and GRPO format alignment. The Judge-and-Refine pipeline addresses the annotation quality paradox—hard samples are most valuable but least reliably annotatable—by using render-then-verify: compiling LaTeX/HTML to images, feeding original and rendered images to a Judge-Refine model, and iteratively correcting cross-modal mapping gaps. The paper also introduces OmniDocBench v1.6 with corrected element-matching biases and a Hard subset for more discriminative evaluation.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04771]] MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale | 2026-04-05 | Data-engineering-only improvement (+2.71 pts over baseline); 65.5M training samples via DDAS/CMCV/Judge-and-Refine; 95.69 on OmniDocBench v1.6 Full |

## Open Problems

- **Structural understanding beyond content extraction**: Current work focuses on accurate content extraction, but hierarchical heading-body relationships, figure-table bindings, and cross-page continuity are equally critical for retrieval and semantic understanding.
- **Vertical domain evaluation**: OmniDocBench v1.6 covers mainstream scenarios; finance, legal, and medical domains with higher precision requirements lack domain-specific evaluation sets.
- **Element-matching ambiguities**: The same content can have multiple equivalent notations (HTML vs Markdown for tables), and the same visual layout can have different legitimate representations—human annotators themselves disagree.
- **From extraction to semantic understanding**: Advancing from "content extraction" to "structured semantic understanding" of documents remains an open challenge.

## Connections

- [[topics/data-centric-ai]] — MinerU2.5-Pro exemplifies data-centric AI principles: performance bottlenecks stem from training data deficiencies, not model architecture
- [[topics/llm-training]] — The three-stage progressive training strategy (pre-training, hard-sample SFT, GRPO alignment) is directly applicable to other post-training pipelines
- [[topics/vision-language-models]] — Document parsing models like MinerU2.5-Pro operate at the intersection of vision understanding and language extraction