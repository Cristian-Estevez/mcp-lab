from mcp import types


# Each tool is declared with a name, description, and a JSON Schema for its inputs.
# The description is what the model reads to decide whether to call the tool —
# it's also the main attack surface for tool poisoning (Phase 5).
TOOLS: list[types.Tool] = [
    types.Tool(
        name="echo",
        description="Returns the input message unchanged. Use this to verify the tool call pipeline is working end-to-end.",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back.",
                }
            },
            "required": ["message"],
        },
        # annotations are hints to the host/client about tool behaviour.
        # readOnlyHint: true signals this tool has no side effects — safe to
        # call freely. title is the human-readable label shown in host UIs.
        annotations=types.ToolAnnotations(
            title="Echo",
            readOnlyHint=True,    # no side effects
            destructiveHint=False, # irrelevant when readOnlyHint=True, but explicit for clarity
            idempotentHint=True,   # same — irrelevant when readOnly, but true: same input → same output always
            openWorldHint=False,   # pure computation, no external systems touched
        ),
    ),
    types.Tool(
        name="add",
        description="Adds two integers and returns the result.",
        inputSchema={
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "First operand."},
                "b": {"type": "integer", "description": "Second operand."},
            },
            "required": ["a", "b"],
        },
        annotations=types.ToolAnnotations(
            title="Add",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        ),
    ),
]


async def list_tools() -> list[types.Tool]:
    return TOOLS


async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "echo":
        return [types.TextContent(type="text", text=arguments["message"])]

    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [types.TextContent(type="text", text=str(result))]

    raise ValueError(f"Unknown tool: {name}")
