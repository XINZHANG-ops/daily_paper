---
title: "Data-Centric AI"
slug: data-centric-ai
paper_count: 2
last_updated: 2026-04-16
---

# Data-Centric AI

## Overview

Data-centric AI focuses on optimizing training data rather than model architecture. The papers reveal that **data-centric approaches should precede architectural ones**—significant improvements are achievable by improving data selection, weighting, coverage, and annotation quality without any model changes. DataFlex provides the unified engineering infrastructure for data-centric LLM training, while MinerU2.5-Pro provides the definitive case study in document parsing.

## Evolution

Late March 2026 saw DataFlex introduce a unified framework integrating three data-centric paradigms (selection, mixture, weighting) into a single infrastructure. Two weeks later, MinerU2.5-Pro demonstrated that the same philosophy—same architecture, better data—produces state-of-the-art results in document parsing, achieving 95.69 on OmniDocBench by expanding from under 10M to 65.5M training samples.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2603.26164]] DataFlex | 2026-04-06 | Unified framework for data-centric dynamic training |
| [[2604.04771]] MinerU2.5-Pro | 2026-04-07 | Data engine pushes document parsing via data scaling |

## Patterns & Insights

- **Data is the bottleneck**: Architecture is often sufficient; training data is the limiting factor
- **Same architecture, dramatically better results**: Data improvements can outperform architectural changes
- **Three paradigms unified**: DataFlex shows selection, mixture, and weighting share common infrastructure

## Open Problems

- Developing data-centric approaches for domains beyond NLP and document parsing
- Combining data-centric with model-centric approaches optimally
- Automated data quality assessment and improvement

## Connections

- [[topics/llm-training]] — Data-centric training is one approach to LLM optimization
- [[topics/document-parsing]] — Document parsing is a concrete application domain
- [[entities/less]] — Dynamic sample selection algorithm supported by DataFlex
