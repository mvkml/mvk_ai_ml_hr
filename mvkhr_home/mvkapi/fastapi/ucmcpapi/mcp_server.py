from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ucmcpapi-mcp", stateless_http=True, streamable_http_path="/")
mcp_app = mcp.streamable_http_app()
