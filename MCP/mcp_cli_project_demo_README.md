# MCP CLI Project Demo

A Claude-powered command-line chat application that demonstrates how to build a **full MCP host**: it connects to one or more MCP servers, surfaces their **tools**, **resources**, and **prompts** to the user, and lets Claude call those tools inside a normal chat loop.

It ships with a bundled MCP server (`mcp_server.py`, name `"DocumentMCP"`) that holds a small in-memory document store and an `ffmpeg`-based video converter. The whole thing runs from one entry point: `python main.py <root_paths...>`.

## What it demonstrates

A working example of the three main MCP primitives plus the **roots** capability:

- **Tools** — Claude can call MCP tools mid-conversation (list dirs, convert video, read/edit docs).
- **Resources** — the in-memory document corpus is exposed as `docs://documents` and `docs://documents/{doc_id}`, used to power `@doc_id` mentions.
- **Prompts** — server-defined prompts (e.g. `/format <doc_id>`) are surfaced as slash-commands in the CLI with tab completion.
- **Roots** — the client advertises filesystem roots back to the server (via `list_roots_callback`), and the server enforces that `read_dir` / `convert_video` only touch paths inside those roots.

## Project layout

```
cli_project/
├── main.py              # Entry point: wires Claude + MCP clients + CLI together
├── mcp_client.py        # Thin wrapper around mcp.ClientSession (stdio transport)
├── mcp_server.py        # FastMCP server "DocumentMCP" (tools + resources + prompts)
├── pyproject.toml       # deps: anthropic, mcp[cli], prompt-toolkit, python-dotenv
├── .env                 # ANTHROPIC_API_KEY, CLAUDE_MODEL  (not committed)
├── README.md            # Original README
└── core/
    ├── claude.py          # Anthropic SDK wrapper (chat, tools, thinking)
    ├── chat.py            # Base Chat: agentic loop until stop_reason != "tool_use"
    ├── cli_chat.py        # CliChat: adds @-mention + /-command handling
    ├── cli.py             # prompt-toolkit UI (completer, key bindings, suggester)
    ├── tools.py           # ToolManager: aggregates tools across MCP clients, routes calls
    ├── video_converter.py # ffmpeg wrapper used by the convert_video tool
    └── utils.py           # file:// URL → Path helper
```

## How the pieces fit together

```
              ┌────────────────────────────────────────────────────┐
              │                       main.py                      │
              │  loads .env, builds Claude(), opens MCPClient(s),  │
              │  hands them to CliChat → CliApp → run loop         │
              └────────────────────────────────────────────────────┘
                                   │
                ┌──────────────────┼──────────────────────┐
                ▼                  ▼                      ▼
        ┌──────────────┐   ┌───────────────┐   ┌──────────────────┐
        │ Claude       │   │ MCPClient(s)  │   │ CliApp           │
        │ (Anthropic)  │   │ stdio → server│   │ prompt-toolkit UI│
        └──────────────┘   └───────┬───────┘   └─────────┬────────┘
                                   │                     │
                                   ▼                     ▼
                         ┌──────────────────┐    ┌───────────────┐
                         │ mcp_server.py    │    │ CliChat       │
                         │  • tools         │◄───┤  @mentions →  │
                         │  • resources     │    │  resources    │
                         │  • prompts       │    │  /commands →  │
                         │  • list_roots()  │    │  prompts      │
                         └──────────────────┘    └───────────────┘
```

The agentic loop lives in `core/chat.py`: send messages + tool definitions to Claude → if `stop_reason == "tool_use"`, dispatch each tool call through `ToolManager` to the right MCP client, append the results as a user message, and loop. When Claude stops asking for tools, the final text is returned to the CLI.

## The bundled MCP server (`mcp_server.py`)

A `FastMCP` instance named `"DocumentMCP"` with an in-memory `docs` dict (6 fake docs: `deposition.md`, `report.pdf`, `financials.docx`, …) and the following capabilities:

| Kind | Name | Purpose |
|---|---|---|
| tool | `list_roots` | Lists the roots advertised by the client |
| tool | `read_dir` | Lists a directory, sandboxed to a root |
| tool | `convert_video` | MP4 → avi / mov / webm / mkv / gif via ffmpeg, sandboxed to a root |
| tool | `read_doc_contents` | Returns the contents of a doc by id |
| tool | `edit_document` | String-replace inside a doc |
| resource | `docs://documents` | JSON list of all doc ids |
| resource | `docs://documents/{doc_id}` | Plain-text contents of one doc |
| prompt | `format` | Returns a user-message prompt asking Claude to reformat a doc in Markdown |

Roots are enforced via `is_path_allowed()`, which calls `ctx.session.list_roots()` and checks containment with `Path.relative_to`.

## The CLI (`core/cli.py` + `core/cli_chat.py`)

Built on `prompt-toolkit` with custom completion and key bindings:

- **`@<doc_id>`** — mention a document. The CLI completes against `docs://documents`; mentioned docs are fetched via `read_resource` and injected into the prompt as `<document id="...">...</document>` blocks before sending to Claude. Triggered by typing `@`.
- **`/<command> <doc_id>`** — invoke an MCP **prompt** by name. The CLI completes the command name against the server's `list_prompts()` and then the doc id against `docs://documents`. The resolved prompt messages are prepended to the chat history.
- **Free-form text** — sent straight to Claude, with all MCP tools available.

## Setup

Requires **Python ≥ 3.10**, an Anthropic API key, and **ffmpeg** on `$PATH` if you want `convert_video` to work (`brew install ffmpeg` on macOS).

```bash
# inside cli_project/
uv venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
uv pip install -e .
```

Configure `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-6
```

Both variables are asserted at startup.

## Running

`main.py` takes one or more **root directories** as positional arguments. These define the filesystem sandbox the server is allowed to read.

```bash
uv run main.py /path/to/videos /another/path
# or, without uv:
python main.py /path/to/videos
```

Inside the prompt:

```
> what files are in /path/to/videos ?            # triggers list_roots + read_dir
> convert /path/to/videos/clip.mp4 to gif        # triggers convert_video
> tell me about @deposition.md                   # @-mention → injects doc content
> /format report.pdf                             # invokes the 'format' MCP prompt
```

Tab completes commands and resource ids; `Ctrl-C` exits.

## Things worth knowing if you actually run this

A few rough edges that are visible in the code as shipped:

- **Typos in `mcp_server.py`** — `read_doc_contents`, `edit_document`, and `fetch_doc` reference `ValueEoor` (sic) instead of `ValueError`. These only fire on the error path (`doc_id not in docs`), so the happy path works, but a bad id will produce a `NameError` rather than the intended `ValueError`.
- **`edit_document` returns nothing** — it mutates `docs[doc_id]` in place but doesn't return the new value or a confirmation, so Claude sees an empty tool result.
- **Extra-server loading is disabled** — `main.py` contains `#server_scripts = sys.argv[1:]` commented out and `server_scripts = []` hard-coded right below it. `sys.argv` is used only for root paths; the loop that would spawn additional MCP servers from CLI args never runs.
- **Server transport is stdio only** — `mcp_server.py`'s `__main__` calls `mcp.run(transport="stdio")`, which is what `MCPClient` expects. Don't change it without also changing the client.
- **`pyproject.toml` vs README** — the README says Python 3.9+, but `pyproject.toml` requires `>=3.10`. Go with 3.10.

## Dependencies

From `pyproject.toml`:

- `anthropic >= 0.51.0` — Claude API client
- `mcp[cli] >= 1.8.0` — MCP server + client SDK
- `prompt-toolkit >= 3.0.51` — the CLI UI, completion, key bindings
- `python-dotenv >= 1.1.0` — loads `.env`

## Key takeaway

This is a compact reference implementation of an **MCP host**: it shows the full surface area (tools, resources, prompts, roots) wired into a real agentic chat loop, with a UI layer that makes resources and prompts feel first-class to the user via `@` and `/`. The split between `Chat` (model-agnostic agentic loop) and `CliChat` (MCP-aware sugar on top) is a clean pattern to copy when bolting MCP onto an existing chat app.
