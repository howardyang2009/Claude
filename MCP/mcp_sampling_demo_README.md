# MCP Sampling Demo

A minimal Python demo of the [Model Context Protocol](https://modelcontextprotocol.io) showing three server→client capabilities in one package:

1. **Sampling** — the server asks the client to run an LLM completion on its behalf (`ctx.session.create_message`).
2. **Logging** — the server pushes log messages to the client (`ctx.info`).
3. **Progress notifications** — the server reports progress on a long-running tool (`ctx.report_progress`).

The package is named `sampling` (see `pyproject.toml`), but in practice it covers all three patterns above.

## Project layout

```
sampling/
├── server.py        # FastMCP server exposing two tools
├── client.py        # MCP client that talks to the server over stdio
├── run_server.py    # Alternative entry point: serves over HTTP via uvicorn
├── pyproject.toml   # uv / setuptools project metadata
├── .env             # ANTHROPIC_API_KEY and CLAUDE_MODEL (not committed)
└── README.md        # Original short README
```

## What the server exposes (`server.py`)

A `FastMCP` instance named `"Demo Server"` with two tools:

- **`summarize(text_to_summarize: str)`** — demonstrates **sampling**. The tool builds a prompt and calls `ctx.session.create_message(...)`, which hands the request back to the *client* to execute against whichever LLM the client chooses. The tool itself never imports an LLM SDK — that responsibility lives on the client side.
- **`add(a: int, b: int)`** — demonstrates **logging** and **progress**. It emits two `ctx.info(...)` log messages and two `ctx.report_progress(...)` updates (20/100 then 80/100), with a `2 s` sleep in between to make the streaming visible.

By default, `server.py`'s `__main__` block runs the **streamable HTTP** transport. A commented-out line shows how to switch to **stdio** instead.

## What the client does (`client.py`)

The client launches the server as a subprocess over stdio (`uv run server.py`) and opens a `ClientSession` with three callbacks wired in:

- **`sampling_callback`** — receives sampling requests from the server, forwards the messages to the **Anthropic API** (`AsyncAnthropic`), and returns the completion as a `CreateMessageResult`. Model defaults to `claude-sonnet-4-6`.
- **`logging_callback`** — prints log messages the server sends via `ctx.info`.
- **`print_progress_callback`** — prints progress as `current/total (pct%)`.

By default `run()` calls the **`add`** tool with `a=1, b=2`, so you'll see progress and log output. A commented-out block calls **`summarize`** instead — uncomment it to exercise the sampling path (which is where the Anthropic API key is actually used).

## Setup

Requires **Python ≥ 3.10** and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create `.env` in the `sampling/` directory:

```env
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-6
```

Both variables are asserted at client startup, even if you only run the `add` tool.

## Running

### Option A — client launches the server over stdio (default)

```bash
uv run client.py
```

> ⚠️ For this to actually use stdio end-to-end, edit `server.py` and switch the bottom from `mcp.run(transport="streamable-http")` to `mcp.run(transport="stdio")`. As shipped, the server's `__main__` uses HTTP, which conflicts with the client's stdio launcher.

### Option B — run the server as a standalone HTTP service

```bash
uv run run_server.py
```

This serves the MCP app on `http://0.0.0.0:3000` via uvicorn. You'd then need an HTTP-based MCP client (not the one in `client.py`, which is stdio-only) to connect to it.

## Dependencies

From `pyproject.toml`:

- `mcp[cli] >= 1.9.3` — Model Context Protocol SDK (server + client)
- `anthropic >= 0.53.0` — used inside the client's sampling callback
- `python-dotenv >= 1.1.0` — loads `.env`
- `aioconsole >= 0.8.1`

## Key takeaway

This repo is a teaching example of **inverted LLM control flow** in MCP: the *tool* asks the *client* to call an LLM, rather than the tool calling one directly. That keeps API keys, model choice, and rate limits with the host application, while still letting tools take advantage of LLM reasoning. The `add` tool rounds out the demo by showing the two ancillary server→client notification channels (logs and progress) that make long-running tools observable.
