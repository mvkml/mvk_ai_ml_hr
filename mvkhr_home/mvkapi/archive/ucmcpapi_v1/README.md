# ucmcpapi — Version 1 (Archive)

## What This Is
This is the **first iteration** of the UC MCP API, implemented on 2026-05-14 as a
learning baseline to understand the relationship between an MCP server and an AI agent.

---

## Purpose of This Archive
This version is preserved as a **learning reference** and **git history checkpoint**.
It was archived after an architect review identified that the agent was not using the
MCP protocol at runtime. v2 (true MCP implementation) replaces this in `mvkapi/fastapi/ucmcpapi/`.

---

## What Was Built

### Files
| File | Role |
|------|------|
| `mcp_server.py` | MCP server — SSE transport, exposes `add_two_numbers` tool |
| `calculation_api.py` | Agent endpoint — Azure OpenAI function calling |
| `main.py` | Single FastAPI app wiring both routers |
| `requirements.txt` | Python dependencies |
| `.env.example` | Config template (API key, endpoint, deployment) |

### Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/mcp/sse` | GET | MCP SSE connection point |
| `/mcp/messages` | POST | MCP message handler |
| `/calculate/add` | POST | Agent endpoint — takes `{a, b}`, returns sum via OpenAI |

### Flow (as implemented)
```
POST /calculate/add  {a: 3, b: 5}
  → Azure OpenAI receives question with tool definition
      → model decides to call add_two_numbers
  → calculation_api.py calls add_two_numbers() directly (Python import)
  → result returned to OpenAI
  → OpenAI composes final answer
← "The result of 3 + 5 is 8"
```

---

## Why It Was Archived — Architect Decision

> **The MCP server was correctly built. The agent side was not.**

| Aspect | v1 (This Archive) | v2 (Correct Implementation) |
|--------|-------------------|------------------------------|
| Tool definition | Hardcoded in `calculation_api.py` | Fetched dynamically from MCP server |
| Tool execution | Direct Python import | Via `mcp.ClientSession` over SSE |
| Coupling | Tightly coupled (same process) | Fully decoupled (separate services) |
| MCP protocol used at runtime | No | Yes |

In v1, the MCP server's SSE endpoint (`/mcp/sse`) was never called by the agent.
The agent imported `add_two_numbers` as a plain Python function. This is equivalent
to calling a function in another class — not MCP.

---

## Tech Stack
- Python 3.14
- FastAPI 0.111
- MCP SDK 1.27.1
- Azure OpenAI (`AsyncAzureOpenAI`) — gpt-4o-mini
- Uvicorn 0.46

## Azure Config Used
| Key | Value |
|-----|-------|
| Endpoint | `https://sdn-hr05-openai-cus001.openai.azure.com/` |
| Deployment | `etna-hr05-openai-cus001-hr05_gpt_4o_mini` |
| Model | `gpt-4o-mini` |
| API Version | `2024-12-01-preview` |

---

## Issues Logged During This Session
See: `agile/worklogs/dev_fastapi/20260514_000100_mcp_implementation.md`

1. Azure OpenAI vs regular OpenAI client mismatch
2. API key placed in `.env.example` (security risk — corrected)
3. Port 8000 conflict (previous server still running)
4. VS Code `launch.json` not at workspace root
5. Missing `.gitignore` at project root

---

## Authored By
- **Architect Agent** — archive description and technical review
- **Dev FastAPI Agent** — implementation
- **Dev DevOps Agent** — archiving and git preparation
- **Scrum Master Agent** — session tracking

---

*This archive is read-only. Do not modify. For v2, see `mvkapi/fastapi/ucmcpapi/`.*
