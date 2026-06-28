from mcp_server import mcp


# registers multiply_two_numbers as an MCP tool on the shared mcp instance
@mcp.tool()
def multiply_two_numbers(a: float, b: float) -> float:
    """Multiplies two numbers and returns the result."""
    return a * b
