import asyncio
import os
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
    LoggingMessageNotificationParams,
)


load_dotenv()

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)

anthropic_client = AsyncAnthropic()
model = "claude-sonnet-4-6"

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text


async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)


async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=sampling_callback, logging_callback=logging_callback
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                 name="summarize",
                 arguments={"text_to_summarize": "Verdict: your server's sampling implementation is correct end-to-end — request construction, stream routing, correlation of the response, and final tool result all behave properly. The only failure is environmental: Claude Code doesn't implement the sampling/createMessage client capability, so the tool can't be used through this particular connection. To exercise it for real, use a client with sampling support — e.g. the MCP Inspector (npx @modelcontextprotocol/inspector), which lets you approve and fulfill sampling requests interactively, or a custom client built on an MCP SDK with a sampling_callback wired to an LLM.One small observation from the earlier tools/list: both tools have empty description fields — worth adding docstrings to the tool functions so clients know when to use them."},
            )

            #result = await session.call_tool(
            #    name = "add",
            #    arguments={"a":1, "b":2},
            #    progress_callback=print_progress_callback,
            #)
            print(result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
