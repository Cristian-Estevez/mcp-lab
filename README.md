# mcp-lab

A hands-on lab for learning and demonstrating the [Model Context Protocol](https://modelcontextprotocol.io) — from core primitives to advanced patterns like MCP Apps and appsec testing.

Built as a public resource for anyone studying MCP: developers, security researchers, and talk audiences.

## What this covers

| Area | Description |
|------|-------------|
| **Core primitives** | Tools, Resources, and Prompts — what they are, how they differ, when to use each |
| **Transports** | stdio (local) and Streamable HTTP (remote) |
| **MCP Apps** | Interactive HTML UIs rendered inside MCP hosts |
| **Connection methods** | Claude Desktop, VS Code/Cursor, Claude Code CLI, MCP Inspector, MCPJam |
| **AppSec angle** | Using MCP primitives for security testing prompts and tooling |

## Structure

```
mcp-lab/
├── server/
│   ├── tools/          # Tool implementations (dummy → appsec)
│   ├── resources/      # Static and dynamic resource examples
│   ├── prompts/        # Parameterized prompt templates
│   └── apps/           # MCP App UIs (HTML/JS, rendered in hosts)
├── demo-clients/       # Connection guides per client type
└── docs/               # Architecture, plan, and reference notes
```

## Primitives quick reference

| Primitive | Initiated by | Transport | Use when |
|-----------|-------------|-----------|----------|
| **Tool** | Model | Any | You want the LLM to take an action or fetch data |
| **Resource** | Client/User | Any | You want to expose data the client injects into context |
| **Prompt** | User/Client | Any | You want reusable, parameterized prompt templates |
| **MCP App** | Host (via tool) | postMessage | You want an interactive UI inside the conversation |

## Getting started

See [docs/plan.md](docs/plan.md) for the full implementation roadmap.

Requirements: Python 3.10+, Node 18+ (for MCP Apps only)

## License

MIT
