---
title: "GenEval"
slug: geneval
type: benchmark
paper_count: 1
last_updated: 2026-04-21
---

# GenEval

## What It Is

GenEval is an object-focused benchmark for evaluating text-to-image alignment. It provides precise, attribute-focused evaluation of how well generated images match textual prompts, covering dimensions like single object, two objects, counting, color attribution, and position. GenEval has become a standard benchmark for evaluating few-step and distilled image generation models.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18168]] EMF | evaluation | EMF achieves 0.90 GenEval with only 4 steps, matching the 30-step baseline |

## Connections

- [[entities/blip3o-next]] — BLIP3o-NEXT is the base model for EMF, achieving strong GenEval scores
- [[topics/image-generation]] — GenEval is the primary benchmark for text-to-image generation quality
