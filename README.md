# Claude Agent SDK & Pydantic AI Learning Path

Python 3.11+ | async/await | type hints | `uv sync` to install

## The Path

```
Step 0  learn-claude-code          Agent loops, tools, subagents, multi-agent
   ↓
Step 1  Pydantic + Structured Out  Type-safe validated responses from Claude
   ↓
Step 2  Pydantic AI Framework      Agents with DI, typed tools, test harness
   ↓
Step 3  MCP                        Connect agents to external services
   ↓
Step 4  Capstone                   Build a real project combining it all
```

## Progress

- [ ] **Step 0** — [learn-claude-code](learn-claude-code/) (submodule, prerequisite)
  - [ ] s01 — The Agent Loop: one tool + one `while True` loop = a working agent
  - [ ] s02 — Tool Use: add tools via a dispatch map, the loop never changes
  - [ ] s03 — TodoWrite: list steps first, track with TodoManager, doubles completion
  - [ ] s04 — Subagents: spawn child agents with fresh context for subtasks
  - [ ] s05 — Skills: load domain knowledge on-demand via `tool_result`, not system prompt
  - [ ] s06 — Context Compact: three-layer compression for infinite sessions
  - [ ] s07 — Task System: file-based task graph with dependencies, persisted to disk
  - [ ] s08 — Background Tasks: daemon threads for slow ops, agent keeps thinking
  - [ ] s09 — Agent Teams: delegate to persistent teammates via JSONL mailboxes
  - [ ] s10 — Team Protocols: request-response pattern, shutdown + plan approval FSMs
  - [ ] s11 — Autonomous Agents: agents scan a shared board and auto-claim tasks
  - [ ] s12 — Worktree Isolation: each agent works in its own git worktree, no interference
- [ ] **Step 1** — [Pydantic + Structured Outputs](docs/modules/01-pydantic-structured-outputs.md) ~3-4h
  - BaseModel, validators, `model_json_schema()`, enforce typed Claude responses
- [ ] **Step 2** — [Pydantic AI Framework](docs/modules/02-pydantic-ai.md) ~5-6h
  - `Agent`, `result_type`, `@agent.tool`, `RunContext`, `TestModel`
- [ ] **Step 3** — [MCP](docs/modules/03-mcp.md) ~3-4h
  - Connect to MCP servers, build your own, integrate with Agent SDK & Pydantic AI
- [ ] **Step 4** — [Capstone Project](docs/modules/04-capstone.md) ~4-6h
  - Code reviewer, research assistant, data pipeline, or CLI task manager

> [Quick Reference](docs/QUICKSTART.md) — setup + code snippets for each step

## Two SDKs, One Path

| SDK | What it gives you |
|-----|-------------------|
| `claude-agent-sdk` | Claude Code-style automation (Read, Edit, Bash, etc.) |
| `pydantic-ai` | Type-safe agents with dependency injection and structured results |

Both support MCP. The capstone combines them.

## License

MIT
