---
title: "StreamForest"
slug: streamforest
type: algorithm
paper_count: 1
last_updated: 2026-04-18
---

# StreamForest

## What It Is

StreamForest is a streaming video understanding method that uses **tree-structured memory**—a hierarchical organization of past video observations where recent frames are stored at fine granularity and older frames are progressively compressed/abstracted. The design goal is to balance memory capacity with retrieval precision: the tree structure allows efficient access to both recent details and historical patterns.

SIMPLESTREAM demonstrates that this complexity is unnecessary for most benchmarks. StreamForest achieves the best recall (benefiting from its rich memory) but pays the highest perception penalty—errors are concentrated in current-scene misclassifications because the VLM's limited context budget gets diluted with historical tokens from the tree-structured memory. The finding reframes the problem: the question isn't how to build better memory, but how to allocate limited context between perception (current scene) and memory (historical context).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.02317]] SIMPLESTREAM | baseline | Tree-structured memory approach; highest perception penalty among compared methods |

## Connections

- [[entities/simplestream]] — SIMPLESTREAM shows a simple sliding window beats StreamForest's tree-structured memory; the perception-memory tradeoff explains why: complex memory crowds out current perception
- [[topics/video-understanding]] — The StreamForest vs SIMPLESTREAM comparison captures the central tension in streaming video: memory complexity vs perception quality