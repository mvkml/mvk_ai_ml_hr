import json
import os

from fastapi import APIRouter, HTTPException
from openai import AsyncAzureOpenAI
from pydantic import BaseModel

from mcp_server import add_two_numbers

router = APIRouter(prefix="/calculate", tags=["Calculation"])

client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://sdn-hr05-openai-cus001.openai.azure.com/"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
)

AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "etna-hr05-openai-cus001-hr05_gpt_4o_mini")

# Tool definition sent to OpenAI — mirrors the MCP tool in mcp_server.py
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "Adds two numbers and returns their sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


class AddRequest(BaseModel):
    a: float
    b: float


@router.post("/add")
async def calculate_add(request: AddRequest):
    """
    Agent endpoint:
      1. Sends the addition question to OpenAI with the MCP tool available.
      2. OpenAI decides to call add_two_numbers.
      3. We execute the MCP tool function and return the result to OpenAI.
      4. OpenAI composes the final answer.

    When this service is split into two, step 3 will call the MCP /sse
    endpoint over HTTP instead of importing directly.
    """
    messages = [
        {
            "role": "user",
            "content": f"What is {request.a} + {request.b}? Use the add_two_numbers tool.",
        }
    ]

    # ── Round 1: ask OpenAI, expect a tool call ─────────────────────────────
    response = await client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if not message.tool_calls:
        # Model answered without using the tool
        return {"answer": message.content, "tool_called": None}

    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    # ── Execute the MCP tool ─────────────────────────────────────────────────
    try:
        tool_result = add_two_numbers(args["a"], args["b"])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"MCP tool error: {exc}")

    # ── Round 2: send tool result back, get final answer ─────────────────────
    messages.append(message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(tool_result),
        }
    )

    final_response = await client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=messages,
    )

    return {
        "a": request.a,
        "b": request.b,
        "tool_called": tool_call.function.name,
        "tool_args": args,
        "tool_result": tool_result,
        "answer": final_response.choices[0].message.content,
    }
