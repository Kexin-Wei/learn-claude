# Quick Reference

## Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk pydantic pydantic-ai mcp
```

## Claude Agent SDK — Basic Query (you know this)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage

async def main():
    async for message in query(
        prompt="Hello, Claude!",
        options=ClaudeAgentOptions(max_turns=1),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)

asyncio.run(main())
```

## Structured Output with Pydantic (Module 1)

```python
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    year: int
    genre: list[str]

# Use model_json_schema() to enforce typed responses
# via Agent SDK's query() or Pydantic AI's result_type
```

## Pydantic AI Agent (Module 2)

```python
from pydantic_ai import Agent

agent = Agent(
    'anthropic:claude-sonnet-4-20250514',
    system_prompt='Be concise and helpful.',
    result_type=str,
)

result = agent.run_sync('What is 2 + 2?')
print(result.data)
```

## Agent SDK with MCP (Module 3)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="List files in /tmp",
        options=ClaudeAgentOptions(
            allowed_tools=["mcp__filesystem__list_directory"],
            mcp_servers={"filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]}},
        ),
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
```

## Pydantic AI with MCP (Module 3)

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

server = MCPServerStdio('npx', ['-y', '@modelcontextprotocol/server-filesystem', '/tmp'])

agent = Agent('anthropic:claude-sonnet-4-20250514', mcp_servers=[server])

async with agent.run_mcp_servers():
    result = await agent.run('List files in /tmp')
```
