---
title: "Document Parsing"
slug: document-parsing
paper_count: 1
last_updated: 2026-04-16
---

# Document Parsing

## Overview

Document parsing converts unstructured PDFs into structured machine-readable formats. The papers reveal that **the bottleneck in document parsing is training data, not model architecture**. MinerU2.5-Pro achieves state-of-the-art using the same 1.2B architecture as MinerU2.5, improving 2.71 points on OmniDocBench by expanding training data from under 10M to 65.5M samples through a co-designed Data Engine.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2604.04771]] MinerU2.5-Pro | 2026-04-07 | Data engine pushes document parsing to 95.69 via data scaling |

## Patterns & Insights

- **Same architecture, dramatically better results**: Data improvements outperform architectural changes
- **Annotation quality paradox**: The hardest samples (most valuable for model quality) are least reliably annotatable
- **Cross-model consistency verification**: Using agreement among diverse models to assess annotation quality

## Open Problems

- Extending the data-centric approach to other document types beyond technical papers
- Scaling annotation quality for long-tail document layouts
- Reducing the computational cost of multi-model consistency verification

## Connections

- [[topics/data-centric-ai]] — Document parsing is a concrete application of data-centric principles
- [[topics/computer-vision]] — Document parsing requires layout understanding, text recognition, and figure detection
