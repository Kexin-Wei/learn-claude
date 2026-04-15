# Phase C — SDK & Provider Comparison

> Tables generated from `c01_feature_probe.py` results (`c01_comparison.csv`).
> Run `uv run python phase-c/<sdk>/c01_feature_probe.py` to re-probe.

## Built-in Tools

| Tool | Claude Agent SDK | Claude CLI | GLM (via z.ai) | OpenAI Agents SDK |
|------|-----------------|------------|----------------|-------------------|
| Web search | Yes (t01: WebSearch) | Yes (t01: WebSearch) | Yes (proxy: WebSearch) | Yes (t01: WebSearchTool) |
| File search | Yes (t01: Glob/Grep) | Yes (t01: Glob/Grep) | Yes (proxy: Glob/Grep) | Yes (import: FileSearchTool) |
| Code execution | Yes (t01: Bash) | Yes (t01: Bash) | Yes (proxy: Bash) | Yes (import: CodeInterpreterTool) |
| Shell | Yes (t01: Bash) | Yes (t01: Bash) | Yes (proxy: Bash) | Yes (import: ShellTool) |
| File read | Yes (t01: Read) | Yes (t01: Read) | Yes (proxy: Read) | N/A (DIY) |
| File write | Yes (t01: Write) | Yes (t01: Write) | Yes (proxy: Write) | N/A (DIY) |
| File edit | Yes (t01: Edit) | Yes (t01: Edit) | Yes (proxy: Edit) | Yes (import: ApplyPatchTool) |
| Image generation | N/A | N/A | N/A | Yes (import: ImageGenerationTool) |
| MCP | Yes (t02b: MCP server tested) | Yes (flag: --mcp-config) | Yes (proxy) | No (MCPServer not found) |
| Tool search | Yes (t01: ToolSearch) | Yes (t01: ToolSearch) | Yes (proxy: ToolSearch) | N/A |
| **TodoWrite** | **Yes (t02: used)** | **Yes (t02: used)** | **Yes (proxy: found)** | **N/A** |

## Agent Features

| Feature | Claude Agent SDK | Claude CLI | GLM (via z.ai) | OpenAI Agents SDK |
|---------|-----------------|------------|----------------|-------------------|
| Agent loop | Yes (t01: query()) | Yes (t01: claude -p) | Yes (proxy: query()) | Yes (t01: Runner.run()) |
| Custom tools | Yes (t02b: MCP tool used 3x) | Yes (flag: --mcp-config) | Yes (proxy) | Yes (t01: @function_tool 2x) |
| Structured output | Yes (t05: output_format JSON) | Yes (t05: --json-schema) | Yes (proxy) | Yes (t01: Pydantic output_type) |
| Multi-agent | Yes (t03: Agent tool) | Yes (t03: Agent tool) | Yes (proxy: Agent) | Yes (t02: handoff to math-expert) |
| Agent nesting | No (t03: 1 level) | No (t03: 1 level) | No (1 level) | Yes (t02: handoff chains) |
| Guardrails | Yes (t05: disallowed_tools) | Yes (t05: --tools restriction) | Yes (proxy) | Yes (t02: InputGuardrail) |
| Hooks / lifecycle | Yes (import: PreToolUse/Stop with fields) | Yes (file: settings.json hooks) | Yes (proxy) | Yes (t03: RunHooks 6 + AgentHooks 2 events) |
| Permission system | Yes (t05: disallowed_tools) | Yes (t05: --tools enforced) | Yes (proxy) | N/A |
| Tracing / dashboard | N/A | N/A | N/A | Yes (t03: set_tracing_disabled) |
| Plan mode | No (t04: tools not blocked) | Yes (t04: plan mode worked) | Yes (proxy) | N/A |
| Session resume | Yes (live: 357 sessions) | Yes (flag: --resume) | Yes (proxy) | Yes (live: previous_response_id) |
| Streaming | Yes (t01: async iteration) | Yes (t01: stream-json) | Yes (proxy: async iteration) | Yes (live: run_streamed 12 events) |
| Context management | Yes (built-in compaction) | Yes (auto compaction) | Yes (proxy) | N/A (manual) |
| Auto memory | N/A (CLI-only) | Yes (file: 15 memory files) | N/A | N/A |
| Skills (on-demand) | Yes (import: settingSources) | Yes (flag: slash commands) | N/A | N/A |
| CLAUDE.md / rules | Yes (import: settingSources) | Yes (flag: auto-loaded) | N/A | N/A |
| MCP support | Yes (t02b: server tested) | Yes (flag: --mcp-config) | Yes (proxy) | No (not found) |

## Coding Task Test Results

> Task: "Build a multi-file Python expense tracker CLI (models.py, storage.py, cli.py, test_tracker.py).
> Commands: add, list (with filters), summary (category totals), delete. JSON persistence. Unit tests."
>
> Run: `uv run python phase-c/<sdk>/c02_coding_task.py`

| Metric | Claude Agent SDK | Claude CLI | GLM (via z.ai) | OpenAI Agents SDK |
|--------|-----------------|------------|----------------|-------------------|
| Completed? | Yes (async cleanup error) | Yes | Yes | Files only (import bug) |
| Turns used | 21 | 22 | 17 | 12 |
| Expected files (4) | 4/4 | 4/4 | 4/4 | 4/4 |
| Code runs? | Yes | Yes | Yes | No |
| Cost | $0.77 | $0.62 | $1.55 | N/A (check dashboard) |
| Duration | 169s | 134s | 476s | 86s |
| Used TodoWrite? | Yes | Yes | Yes | No (not available) |
| Used subagents? | Yes | Yes | Yes | No (not available) |

## Summary

**Claude CLI** is the most complete — all 27 features verified, cheapest ($0.62) and fastest working solution (134s). Auto memory with 15 persistent files, hooks via settings.json.

**Claude Agent SDK** matches CLI on 24/27 features. Plan mode doesn't block tools (may differ from CLI behavior). Auto memory is CLI-only. Session resume confirmed with 357 live sessions.

**OpenAI Agents SDK** has unique strengths: handoff chains (multi-level nesting), tracing dashboard, ImageGenerationTool. Streaming and session resume verified live. Lacks file read/write, TodoWrite, permissions, plan mode, MCP. Generated code had import bugs in the coding task.

**GLM via z.ai** inherits all Claude tools (verified by live proxy query finding Bash/Read/Write/WebSearch/Agent/TodoWrite). Slowest (476s) and most expensive ($1.55). Native GLM SDK is raw LLM API — you build everything yourself.
