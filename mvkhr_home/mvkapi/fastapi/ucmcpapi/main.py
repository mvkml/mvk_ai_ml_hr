from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

import mcp_server
import mpc_add   # noqa: F401  # pyright: ignore[reportUnusedImport]
import mcp_sub   # noqa: F401  # pyright: ignore[reportUnusedImport]
import mcp_mul   # noqa: F401  # pyright: ignore[reportUnusedImport]
import mcp_div   # noqa: F401  # pyright: ignore[reportUnusedImport]


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with mcp_server.mcp.session_manager.run():
        yield


app = FastAPI(
    title="UC MCP API",
    description="MCP server — Streamable HTTP transport",
    version="0.2.0",
    lifespan=lifespan,
)

app.mount("/mcp", mcp_server.mcp_app)
