from fastapi import APIRouter, Request
from mcp.server import Server
from mcp.server.sse import SseServerTransport
import mcp.types as types

# MCP server instance
mcp = Server("ucmcpapi-mcp")

# SSE transport — messages will be posted to /mcp/messages
sse_transport = SseServerTransport("/mcp/messages")

router = APIRouter(prefix="/mcp", tags=["MCP"])


# ── Core tool logic (pure function — reusable outside MCP too) ──────────────

def add_two_numbers(a: float, b: float) -> float:
    return a + b


# ── MCP tool declarations ───────────────────────────────────────────────────

@mcp.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add_two_numbers",
            description="Adds two numbers and returns their sum.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        )
    ]


@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "add_two_numbers":
        result = add_two_numbers(arguments["a"], arguments["b"])
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")


# ── FastAPI endpoints (SSE transport) ───────────────────────────────────────

@router.get("/sse")
async def handle_sse(request: Request):
    """MCP SSE endpoint — MCP clients connect here."""
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options(),
        )


@router.post("/messages")
async def handle_messages(request: Request):
    """MCP message handler — SSE transport posts tool calls here."""
    await sse_transport.handle_post_message(
        request.scope, request.receive, request._send
    )
