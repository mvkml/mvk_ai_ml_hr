from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

import calculation_api
import mcp_server

app = FastAPI(
    title="UC MCP API",
    description="MCP server + OpenAI agent demo — addition tool",
    version="0.1.0",
)

app.include_router(mcp_server.router)
app.include_router(calculation_api.router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "endpoints": {
            "mcp_sse": "/mcp/sse",
            "mcp_messages": "/mcp/messages",
            "calculate_add": "POST /calculate/add",
        },
    }
