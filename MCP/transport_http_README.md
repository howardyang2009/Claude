# transport-http

A minimal **MCP (Model Context Protocol) server** demonstrating the
**streamable-HTTP** transport, bundled with an interactive browser-based
protocol inspector.

The server exposes a single `add` tool that emits progress notifications,
and the included HTML page walks through every step of the MCP HTTP
handshake live against the running server — making this a useful
reference for understanding what actually goes over the wire.

---

## What's in this project

| File             | Purpose                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `main.py`        | The FastMCP server. Defines the `add` tool and serves `index.html` at `/`. |
| `index.html`     | Browser-based MCP protocol inspector — issues real requests to the server. |
| `pyproject.toml` | Python project definition. Requires Python ≥ 3.10 and `mcp[cli] >= 1.9.3`. |

---

## How it works

### The server (`main.py`)

```python
mcp = FastMCP("mcp-server")

@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await asyncio.sleep(2)
    await ctx.report_progress(80, 100)
    return a + b

@mcp.custom_route("/", methods=["GET"])
async def get(request: Request) -> Response:
    with open("index.html", "r") as f:
        return Response(content=f.read(), media_type="text/html")

mcp.run(transport="streamable-http")
```

A few things worth noticing:

- **The `Context` parameter is injected automatically by FastMCP.** It
  gives the tool a channel back to the client for logs (`ctx.info`) and
  progress (`ctx.report_progress`), which the client receives as
  server-sent events while the tool is still running.
- **The 2-second sleep is deliberate.** It gives the demo UI enough
  time to show the SSE stream filling in before the final result lands.
- **`custom_route`** lets the same FastMCP process serve the inspector
  page so you can open the demo at `http://localhost:8000/` without a
  separate static file server.

Two commented-out flags in the `FastMCP(...)` constructor are worth
knowing about:

- `stateless_http=True` — disables session tracking. Each request is
  independent; no `mcp-session-id` is issued.
- `json_response=True` — forces plain JSON responses instead of SSE.
  Faster for simple request/response, but you lose progress streaming.

### The inspector (`index.html`)

A self-contained dark-themed page (HTML + CSS + vanilla JS, no build
step) that walks through the MCP HTTP handshake one step at a time
against the live server at `/mcp/`:

1. **`initialize`** — opens a session. The server returns an
   `mcp-session-id` header that the page captures and reuses for every
   subsequent request.
2. **`notifications/initialized`** — the post-handshake "ready" signal.
3. **`tools/list`** — lists available tools (just `add` here).
4. **`tools/call`** for `add(2, 3)` — the interesting one. Because the
   response is an SSE stream, you watch the `notifications/message`
   (info log) and `notifications/progress` events arrive in real time
   before the final result.
5. **Start GET SSE** — opens a long-lived `GET /mcp/` SSE stream for
   server-initiated messages, separate from the request/response streams.

Every panel shows the raw request headers
(`Accept: application/json, text/event-stream`, `mcp-session-id: …`),
the response headers, and the body or stream — so you can see exactly
what a streamable-HTTP MCP client has to send.

---

## Setup

Requires Python 3.10+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Running

```bash
uv run main.py
```

The server starts on `http://localhost:8000` by default. The MCP
endpoint lives at `/mcp/` and the demo inspector at `/`.

Open <http://localhost:8000/> in a browser and click through the
panels in order, top to bottom.

---

## Why streamable HTTP?

The streamable-HTTP transport is the newer MCP transport that
replaces the older HTTP+SSE split (which used two separate endpoints
for sending and receiving). Streamable HTTP uses a **single endpoint**
that can return either a plain JSON response or an SSE stream
depending on what the operation needs — which is why every request
in this demo carries `Accept: application/json, text/event-stream`.

That single-endpoint design is what makes `tools/call` interesting to
watch here: the same POST that invokes the tool also carries the
progress notifications back as they happen, and only closes when the
tool returns its final value.
