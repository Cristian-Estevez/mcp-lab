# Implementation Plan

## Goals

1. Deep understanding of MCP primitives (tools, resources, prompts, MCP Apps)
2. Working server demonstrating all primitives — stdio and HTTP transports
3. Connection demos across multiple client types
4. Foundation for an appsec testing toolkit built on MCP
5. Presentation-ready material

---

## Phase 1 — Core server (stdio, Python)

**Deliverables:**
- `server/server.py` — bare MCP server, stdio transport
- One dummy tool (`echo`, `add`, or similar)
- One static resource (`text://hello`)
- One parameterized prompt (`summarize` with a `topic` arg)

**Goal:** get connected to Claude Desktop and MCP Inspector. Understand the handshake, capability negotiation, and message flow at the protocol level.

**Key concepts to internalize:**
- `initialize` / `initialized` lifecycle
- Capability declaration (`tools`, `resources`, `prompts`)
- How the host lists and calls each primitive

---

## Phase 2 — Resources and Prompts in depth

**Deliverables:**
- Dynamic resource (content changes per call — e.g., current timestamp, live data)
- Resource with URI template (`data://{id}`)
- `notifications/resources/updated` — push updates to client
- Multiple prompts with different argument shapes
- Prompt that returns multi-turn message arrays (not just a single string)

**Goal:** correct mental model of resources vs tools vs prompts.

**Key distinctions:**
- Resources are client-fetched, not model-called. The model doesn't invoke them — the client includes their content in context.
- Prompts are user/client-initiated templates. They take args and return a `messages` array (full conversation structure), not just text.
- Tools are model-initiated. The LLM decides when to call them.

---

## Phase 3 — HTTP transport + remote connections

**Deliverables:**
- `server/server.py` updated to support Streamable HTTP alongside stdio
- Connection guide for MCPJam (`demo-clients/mcpjam.md`)
- Connection guide for remote Claude Desktop config

**Goal:** understand transport differences. stdio is process-local; HTTP enables remote and multi-client scenarios.

---

## Phase 4 — MCP Apps

**Deliverables:**
- `server/apps/dashboard/index.html` — minimal interactive MCP App (pre-built)
- Tool that declares `_meta.ui.resourceUri` pointing to `ui://dashboard`
- Server returns `ui://dashboard` resource with the HTML payload
- Bidirectional communication demo (app calls a tool, host proxies it)

**Goal:** understand the MCP Apps extension — `ui://` resources, `_meta.ui`, the postMessage JSON-RPC dialect, sandboxed iframe security model.

**Tech split:**
- Server: Python (serves the `ui://` resource and handles tool calls)
- App UI: vanilla JS (runs inside host's sandboxed iframe)
- Build step: Node.js — required to inline the `@modelcontextprotocol/ext-apps` bundle into the widget HTML before the Python server can serve it

**Why a Node build step is mandatory:**
The host's iframe sandbox blocks all external script fetches (strict CSP). The
`ext-apps` browser bundle that powers `App.connect()` / `sendMessage()` / etc.
must be inlined directly into the HTML at build time — it cannot be loaded from
a CDN at runtime. The Python server then serves the already-bundled HTML as a
static string.

**Critical implementation details:**
- The `ui://` resource MUST return MIME type `text/html;profile=mcp-app` — this
  is how the host distinguishes a widget resource from plain HTML to display.
  Any other MIME type causes the host to render raw source instead of an iframe.
- Tool declaration in Python: `meta={"ui": {"resourceUri": "ui://dashboard"}}` —
  the Python SDK's `types.Tool` supports `_meta` natively via the `meta` kwarg.
- `annotations=types.ToolAnnotations(readOnlyHint=True)` should be set on any
  tool that only displays data (no side effects).

**Supported hosts:** Claude Desktop, Claude.ai, VS Code Copilot, MCPJam

---

## Phase 5 — AppSec toolkit

**Deliverables:**
- Tools for common appsec test scenarios (prompt injection, tool poisoning, resource exfiltration patterns)
- Prompts designed as security testing templates
- Resources exposing scan/test results
- MCP App UI for displaying findings interactively

**Goal:** demonstrate MCP as a platform for security tooling, and surface the protocol's own attack surface (prompt injection via resource content, `_meta.ui` CSP bypass patterns, tool call proxying abuse).

---

## Connection matrix

| Client | Transport | MCP Apps | Notes |
|--------|-----------|----------|-------|
| Claude Desktop | stdio | Yes | Config via `claude_desktop_config.json` |
| Claude.ai (web) | HTTP | Yes | Remote server required |
| VS Code Copilot | stdio / HTTP | Yes | `.vscode/mcp.json` |
| Cursor | stdio / HTTP | No | `~/.cursor/mcp.json` |
| Claude Code CLI | stdio / HTTP | No | `~/.claude/mcp.json` |
| MCP Inspector | stdio / HTTP | No | Dev/debug tool |
| MCPJam | HTTP | Yes | Good for MCP Apps demos |

---

## Directory structure (target)

```
mcp-lab/
├── server/
│   ├── server.py               # main entrypoint, registers all primitives
│   ├── tools/
│   │   ├── dummy.py            # echo, add, reverse — baseline
│   │   └── appsec.py           # security testing tools (Phase 5)
│   ├── resources/
│   │   ├── static.py           # static text resources
│   │   ├── dynamic.py          # live/computed resources
│   │   └── ui_dashboard.py     # ui:// resource for MCP App
│   ├── prompts/
│   │   └── templates.py        # parameterized prompts
│   └── apps/
│       └── dashboard/
│           └── index.html      # MCP App UI
├── demo-clients/
│   ├── claude-desktop.md
│   ├── vscode.md
│   ├── claude-code-cli.md
│   ├── inspector.md
│   └── mcpjam.md
├── docs/
│   ├── plan.md                 # this file
│   ├── primitives.md           # deep dive: tools vs resources vs prompts vs apps
│   └── appsec-notes.md        # attack surface and testing patterns
├── README.md
└── requirements.txt
```
