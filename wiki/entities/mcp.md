---
title: "Model Context Protocol"
slug: mcp
type: protocol
paper_count: 1
last_updated: 2026-04-21
---

# Model Context Protocol (MCP)

## What It Is

The Model Context Protocol (MCP) is a standardized interface for connecting LLM agents with scalable real-world services, providing a unified way for agents to invoke tools, query databases, and interact with external stateful environments. MCP serves as the foundational protocol enabling Agent-World to connect with diverse real-world environment ecosystems (1978 environments, 19822 tools).

## Appearances

| Paper | Role | Detail |
|-------|------|--------|
| [[2604.18292]] Agent-World | protocol | MCP provides the unified interface for connecting agents with 1978 real-world environments and 19822 executable tools |

## Connections

- [[entities/agent-world]] — Agent-World uses MCP as the protocol layer for environment connections
- [[topics/agent-systems]] — MCP is foundational infrastructure for general-purpose agent systems
