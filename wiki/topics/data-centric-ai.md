---
title: "Data-Centric AI"
slug: data-centric-ai
paper_count: 2
last_updated: 2026-04-13
---

# Data-Centric AI

## Overview

The two papers in this topic provide complementary evidence that systematic data engineering—not architectural innovation—is the primary lever for advancing AI performance. **DataFlex** addresses the fragmentation problem in data-centric AI research by providing a unified framework built on LLaMA-Factory that treats data as a first-class optimization variable. Its modular trainer abstractions (Select Trainer for dynamic sample selection, Mix Trainer for domain mixture optimization, Weight Trainer for per-sample reweighting) integrate algorithms that previously required separate implementations (LESS, NICE, DoReMi, ODM). The key insight is that data-centric operations are complementary and can be composed: gradient-based data selection, online/offline mixture optimization, and dynamic reweighting each address different aspects of data quality and can be used together. DataFlex demonstrates this by achieving consistent MMLU improvements (LESS gains 5.8pp on Mistral-7B) and 3-7% runtime reductions compared to original implementations, with 57% speedup on 8 GPUs through distributed gradient collection.

**MinerU2.5-Pro** provides the most direct evidence for data-centric principles in document parsing—a domain where architectural choices are well-explored and performance plateaus have been observed. By analyzing state-of-the-art models across diverse architectures and parameter scales, the authors identify that models exhibit highly consistent failure modes on the same hard samples, revealing that performance bottlenecks stem from shared deficiencies in training data rather than model architecture. The Data Engine expands training data from under 10M to 65.5M samples through three co-designed components: Diversity-and-Difficulty-Aware Sampling (DDAS) for coverage, Cross-Model Consistency Verification (CMCV) for informativeness assessment, and Judge-and-Refine annotation for accuracy on hard samples. The three-stage progressive training strategy (large-scale pre-training, hard sample SFT, GRPO alignment) sequentially exploits these data quality tiers. Without any architectural modification, MinerU2.5-Pro achieves 95.69 on OmniDocBench v1.6, improving 2.71 points over the same-architecture baseline and surpassing models with over 200x more parameters.

The two papers converge on a central theme: data quality is not merely one input among many but the primary constraint that architectural innovations cannot bypass. DataFlex shows this through algorithmic data selection and mixture optimization; MinerU2.5-Pro shows this through systematic data engine construction. Both demonstrate that once the data problem is solved properly, architectural differences become secondary.

## Key Papers

| Paper | Date | Contribution |
|-------|------|-------------|
| [[2603.26164]] DataFlex: A Unified Framework for Data-Centric Dynamic Training | 2026-03-27 | Unified Select/Mix/Weight trainer architecture for dynamic data selection, mixture optimization, and reweighting; 7 selection algorithms, 2 mixture methods; 57% speedup for LESS on 8 GPUs |
| [[2604.04771]] MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale | 2026-04-05 | Data Engine expands data from <10M to 65.5M with DDAS/CMCV/Judge-and-Refine; 95.69 on OmniDocBench (surges models with 200x more parameters); three-stage progressive training |

## Open Problems

- **Algorithmic scope**: DataFlex focuses on instruction tuning and pretraining; extension to RLHF and other training paradigms requires additional abstraction.
- **Coverage gaps**: MinerU2.5-Pro covers mainstream document parsing scenarios; vertical domains (finance, legal, medical) with higher precision requirements need domain-specific evaluation sets.
- **From content extraction to structural understanding**: Both papers focus on content accuracy; structural relationships (hierarchical heading-body, figure-table bindings, cross-page continuity) are equally critical for retrieval and semantic understanding.
- **Data quality paradox for hard samples**: MinerU2.5-Pro's Judge-and-Refine addresses the paradox where hard samples are most valuable but least reliably annotatable; extending this to other domains is non-trivial.

## Connections

- [[topics/llm-training]] — DataFlex is a core tool for data-centric LLM training; MinerU2.5-Pro's three-stage training strategy (pre-training, hard SFT, GRPO) is directly relevant
- [[topics/document_parsing]] — MinerU2.5-Pro is the landmark paper for document parsing at scale
- [[topics/computer-vision]] — WildDet3D's massive data engineering (1M images, 13.5K categories) exemplifies data-centric principles in vision