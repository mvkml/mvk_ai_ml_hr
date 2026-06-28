from mcp_server import mcp

_ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen"]
_tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _number_to_words(n: int) -> str:
    if n < 0:
        return "negative " + _number_to_words(-n)
    if n < 20:
        return _ones[n]
    if n < 100:
        return _tens[n // 10] + ("" if n % 10 == 0 else "-" + _ones[n % 10])
    if n < 1000:
        return _ones[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _number_to_words(n % 100))
    return str(n)


@mcp.tool()
def add_two_numbers(a: float, b: float) -> str:
    """Adds two numbers and returns their sum with result in words."""
    result = a + b
    result_int = int(result)
    result_words = _number_to_words(result_int) if result == result_int else str(result)
    return (
        f"[MVK MCP Server | ucmcpapi]\n"
        f"  add_two_numbers({a} + {b}) = {result}\n"
        f"  Result in words: {result_words}\n"
        f"  ★ Vishnu Kiran M — Maths Coaching Center ★"
    )
