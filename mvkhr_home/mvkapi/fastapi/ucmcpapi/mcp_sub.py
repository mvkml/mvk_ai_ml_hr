from mcp_server import mcp


# registers subtract_two_numbers as an MCP tool on the shared mcp instance
@mcp.tool()
def subtract_two_numbers(a: float, b: float) -> float:
    """Subtracts b from a and returns the result."""
    return a - b
