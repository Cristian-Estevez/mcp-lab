"""
mcp-lab server — Phase 1: core server over stdio transport.

Protocol flow on startup:
  client → initialize (sends client capabilities)
  server → initialize response (sends server capabilities: tools, resources, prompts)
  client → initialized notification
  ... normal operation (list_tools, call_tool, etc.)

Run:
  python server/server.py          (from project root)
  .venv/bin/python server/server.py

Logs: mcp-server.log (project root) — full JSON-RPC message trace at DEBUG level.
"""
import asyncio
import logging
import sys
import os

# Allow imports from the server/ package when run as a script.
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from tools.dummy import list_tools, call_tool


def _setup_logging() -> None:
    # Log to a file — stdout/stdin are reserved for the MCP stdio transport,
    # and stderr output can confuse some clients. The log file sits at the
    # project root so it's easy to tail during development.
    log_path = os.path.join(os.path.dirname(__file__), "..", "mcp-server.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        handlers=[logging.FileHandler(os.path.normpath(log_path), mode="a")],
    )


_setup_logging()

# The server name is sent to the client during the initialize handshake.
server = Server("mcp-lab")


# list_tools is called by the client after initialization to discover what
# tools this server exposes. The model then reads the tool descriptions to
# decide when/how to call them.
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return await list_tools()


# call_tool is invoked by the host when the model decides to use a tool.
# 'name' matches a tool declared in list_tools; 'arguments' are validated
# against the tool's inputSchema before this handler is called.
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    return await call_tool(name, arguments)


async def main() -> None:
    # stdio_server() wires stdin/stdout as the MCP transport.
    # All JSON-RPC messages flow over these streams — the process IS the server.
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
