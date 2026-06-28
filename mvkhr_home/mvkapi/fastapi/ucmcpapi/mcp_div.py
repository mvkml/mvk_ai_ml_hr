from mcp_server import mcp


@mcp.tool()
def divide_two_numbers(a: float, b: float) -> float:
    """Divides a by b and returns the result. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b
