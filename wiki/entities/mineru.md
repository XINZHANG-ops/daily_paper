---
title: "MinerU"
slug: mineru
type: framework
paper_count: 1
last_updated: 2026-04-16
---

# MinerU

## What It Is

MinerU is a document parsing framework that converts unstructured PDFs into structured markdown. MinerU2.5-Pro demonstrates that the 1.2B parameter architecture was already capable—the bottleneck was always training data, not architecture. By expanding from under 10M to 65.5M training samples via a co-designed Data Engine, MinerU2.5-Pro achieves 95.69 on OmniDocBench v1.6 (2.71 points above the baseline).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.04771]] | base framework | MinerU2.5-Pro uses the same 1.2B architecture as MinerU2.5 but with improved data |

## Connections

- [[topics/document-parsing]] — MinerU is the document parsing family this paper builds upon
- [[topics/data-centric-ai]] — The paper demonstrates that data improvements outperform architectural ones
