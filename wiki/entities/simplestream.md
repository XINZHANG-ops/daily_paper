---
title: "SIMPLESTREAM"
slug: simplestream
type: model
paper_count: 1
last_updated: 2026-04-16
---

# SIMPLESTREAM

## What It Is

SIMPLESTREAM is a streaming video understanding method that feeds only the last N (2, 4, or 8) frames directly to an off-the-shelf VLM without any memory mechanism. With just 4 frames, it achieves 67.7% on OVO-Bench and 80.59% on StreamingBench—surpassing complex approaches like HERMES and StreamForest. The key finding is a perception-memory tradeoff: adding more historical context improves recall-oriented tasks but degrades current-scene perception.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.02317]] | introduced | SIMPLESTREAM is the paper's main contribution |

## Connections

- [[topics/video-understanding]] — Challenges the assumption that complex memory is needed for streaming
- [[entities/streamforest]] — StreamForest is the complex-memory approach that SIMPLESTREAM beats
