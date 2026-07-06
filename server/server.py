"""
mcp-lab server — Phase 1: core server over stdio transport.

Protocol flow on startup:
  client → initialize (sends client capabilities)
  server → initialize response (sends server capabilities: tools, resources, prompts)
  client → initialized notification
  ... normal operation (tools/list, tools/call, etc.)

Run:
  .venv/bin/python server/server.py
  or: .venv/bin/fastmcp run server/server.py

Logs: mcp-server.log (project root) — full JSON-RPC message trace at DEBUG level.
"""
import logging
import os

from fastmcp import FastMCP

from tools.dummy import register_tools


def _setup_logging() -> None:
    # Log to a file — stdout/stdin are reserved for the MCP stdio transport,
    # and stderr output can confuse some clients.
    log_path = os.path.join(os.path.dirname(__file__), "..", "mcp-server.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        handlers=[logging.FileHandler(os.path.normpath(log_path), mode="a")],
    )


_setup_logging()

mcp = FastMCP("mcp-lab")

# Register all tool groups onto the server instance.
# Each module exposes a register(mcp) function so tools stay in their own file
# without importing the server instance (avoids circular imports).
register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")
