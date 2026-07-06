from fastmcp import FastMCP
from mcp.types import ToolAnnotations

dummy = FastMCP("dummy")


@dummy.tool(
    title="Echo",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def echo(message: str) -> str:
    """Returns the input message unchanged.

    Use this to verify the tool call pipeline is working end-to-end.
    The description is what the model reads to decide whether to call
    the tool — also the main attack surface for tool poisoning (Phase 5).
    """
    return message


@dummy.tool(
    title="Add",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def add(a: int, b: int) -> int:
    """Adds two integers and returns the result."""
    return a + b
