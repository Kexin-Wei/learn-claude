# Claude SDK & Pydantic AI Learning Path

A structured learning repository for mastering the Anthropic Claude SDK and Pydantic AI framework.

## Learning Objectives

By completing this learning path, you will:
- Understand how to interact with Claude models via the official SDK
- Build type-safe AI applications using Pydantic models
- Create AI agents with structured outputs
- Implement tool use (function calling) patterns
- Design multi-agent systems

---

## Prerequisites

- [ ] Python 3.11+
- [ ] Basic understanding of async/await
- [ ] Familiarity with type hints
- [ ] Anthropic API key ([Get one here](https://console.anthropic.com/))

---

## Learning Modules

### Module 1: Anthropic SDK Fundamentals
**Goal:** Understand the basics of interacting with Claude

- [ ] Install SDK: `pip install anthropic`
- [ ] Create first message request
- [ ] Explore sync vs async clients
- [ ] Handle streaming responses
- [ ] Understand token counting and costs

**Resources:**
- [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)
- [Official SDK Docs](https://docs.anthropic.com/en/api/client-sdks)

**Practice:** `exercises/01_sdk_basics/`

---

### Module 2: Pydantic Models for AI
**Goal:** Use Pydantic for structured data validation

- [ ] Define Pydantic BaseModel classes
- [ ] Use Field() for validation constraints
- [ ] Implement custom validators
- [ ] Serialize/deserialize JSON
- [ ] Handle nested models

**Resources:**
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Practice:** `exercises/02_pydantic_basics/`

---

### Module 3: Structured Outputs with Claude
**Goal:** Get guaranteed JSON responses from Claude

- [ ] Use `response_format` with JSON schema
- [ ] Define Pydantic models as output schemas
- [ ] Handle partial/streaming structured outputs
- [ ] Validate and retry on schema errors

**Resources:**
- [Claude Structured Outputs Guide](https://thomas-wiegold.com/blog/claude-api-structured-output/)
- [Instructor Library](https://python.useinstructor.com/integrations/anthropic/)

**Practice:** `exercises/03_structured_outputs/`

---

### Module 4: Tool Use (Function Calling)
**Goal:** Enable Claude to call your functions

- [ ] Define tools with JSON schema
- [ ] Handle tool_use response blocks
- [ ] Implement tool result handling
- [ ] Chain multiple tool calls
- [ ] Error handling for tools

**Resources:**
- [Claude Tool Use Docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [claudetools library](https://github.com/vatsalsaglani/claudetools)

**Practice:** `exercises/04_tool_use/`

---

### Module 5: Pydantic AI Framework
**Goal:** Build agents the "FastAPI way"

- [ ] Install: `pip install pydantic-ai`
- [ ] Create a basic Agent
- [ ] Use system prompts and dependencies
- [ ] Implement typed tool functions
- [ ] Handle conversation context

**Resources:**
- [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
- [Pydantic AI Docs](https://ai.pydantic.dev/)
- [daveebbelaar/pydantic-ai-tutorial](https://github.com/daveebbelaar/pydantic-ai-tutorial)

**Practice:** `exercises/05_pydantic_ai/`

---

### Module 6: Building AI Agents
**Goal:** Create autonomous agents that can reason and act

- [ ] Design agent architecture
- [ ] Implement ReAct pattern (Reason + Act)
- [ ] Add memory/context management
- [ ] Handle multi-turn conversations
- [ ] Implement agent loops with exit conditions

**Resources:**
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
- [anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)

**Practice:** `exercises/06_agents/`

---

### Module 7: Multi-Agent Systems
**Goal:** Coordinate multiple specialized agents

- [ ] Design agent communication patterns
- [ ] Implement supervisor/worker architecture
- [ ] Handle agent handoffs
- [ ] Build a research agent system

**Resources:**
- [coleam00/PydanticAI-Research-Agent](https://github.com/coleam00/PydanticAI-Research-Agent)
- [Martin Fowler: Building CLI Coding Agent](https://martinfowler.com/articles/build-own-coding-agent.html)

**Practice:** `exercises/07_multi_agent/`

---

### Module 8: MCP (Model Context Protocol)
**Goal:** Connect agents to external tools via MCP

- [ ] Understand MCP architecture
- [ ] Connect to MCP servers
- [ ] Build custom MCP tools
- [ ] Integrate MCP with Pydantic AI

**Resources:**
- [Pydantic AI MCP Support](https://pydantic.dev/articles/mcp-launch)

**Practice:** `exercises/08_mcp/`

---

## Project Ideas

After completing the modules, try building:

1. **CLI Assistant** - A command-line tool that helps with file operations
2. **Code Reviewer** - An agent that reviews code and suggests improvements
3. **Research Bot** - Multi-agent system that searches and summarizes information
4. **Data Extractor** - Extract structured data from unstructured text

---

## Quick Reference

### Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install anthropic pydantic pydantic-ai

# Set API key
export ANTHROPIC_API_KEY="your-key-here"
```

### Basic Claude Request

```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)
```

### Basic Pydantic AI Agent

```python
from pydantic_ai import Agent

agent = Agent(
    'anthropic:claude-sonnet-4-20250514',
    system_prompt='Be concise and helpful.'
)

result = agent.run_sync('What is 2 + 2?')
print(result.data)
```

---

## Progress Tracker

| Module | Status | Notes |
|--------|--------|-------|
| 1. SDK Fundamentals | ⬜ Not Started | |
| 2. Pydantic Models | ⬜ Not Started | |
| 3. Structured Outputs | ⬜ Not Started | |
| 4. Tool Use | ⬜ Not Started | |
| 5. Pydantic AI | ⬜ Not Started | |
| 6. AI Agents | ⬜ Not Started | |
| 7. Multi-Agent | ⬜ Not Started | |
| 8. MCP | ⬜ Not Started | |

---

## License

MIT
