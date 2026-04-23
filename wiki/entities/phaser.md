---
title: "Phaser"
slug: phaser
type: framework
paper_count: 1
last_updated: 2026-04-21
---

# Phaser

## What It Is

Phaser is a popular open-source HTML5 game framework for creating 2D web games. It provides a programmatic API for game loops, physics systems, scene management, and asset handling—all expressible in JavaScript/TypeScript. OpenGame targets Phaser as its primary game development framework because its fully text-based architecture makes it amenable to LLM code generation.

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18394]] OpenGame | target framework | OpenGame's template library and debugging protocol are organized around Phaser's architecture; all generated games are valid Phaser projects |

## Connections

- [[2604.18394]] — Phaser is the target framework; OpenGame's template families (platformer, top-down, grid_logic, etc.) map directly to Phaser's physics and scene systems
- [[topics/code-agents]] — Phaser's text-based API makes it an ideal testbed for code agents; unlike Unity/Unreal which rely on binary assets, Phaser games can be fully expressed in code
