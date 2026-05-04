---
title: "LLaMA-Factory"
slug: llama-factory
type: framework
paper_count: 1
last_updated: 2026-04-18
---

# LLaMA-Factory

## What It Is

LLaMA-Factory is an open-source training framework for fine-tuning and pretraining LLMs, providing unified interfaces for data loading, model configuration, training orchestration, and evaluation. It supports a wide range of models and training methods (full fine-tuning, LoRA, QLoRA) with built-in DeepSpeed integration.

DataFlex builds directly on LLaMA-Factory as its foundation layer, demonstrating an important architectural pattern: research frameworks that introduce novel capabilities (like dynamic data selection) can be built on mature open-source infrastructure rather than requiring bespoke training pipelines. DataFlex replaces LLaMA-Factory's standard training layer with three unified trainer types (Select, Mix, Weight) while preserving all of LLaMA-Factory's data loading, evaluation, and deployment capabilities, enabling full compatibility with DeepSpeed ZeRO-3 for large-scale training.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2603.26164]] DataFlex | foundation | Training infrastructure backbone; DataFlex replaces training layer while preserving all other capabilities |

## Connections

- [[entities/domi]] — DoReMi's Mix Trainer runs on LLaMA-Factory via DataFlex's unified training layer
- [[entities/less]] — LESS's Select Trainer is supported by DataFlex/LLaMA-Factory's shared embedding extraction infrastructure, achieving 57% speedup on 8 GPUs
- [[topics/data-centric-ai]] — LLaMA-Factory exemplifies how open-source infrastructure lowers the barrier for systematic data-centric research
- [[topics/llm-training]] — Training infrastructure as a platform layer that enables research innovations without infrastructure duplication