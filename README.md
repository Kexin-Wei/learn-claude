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

## Timeline

**Total Duration:** ~4-6 weeks (at 1-2 hours/day)

### Suggested Schedule

```
Week 1: Foundation
├── Days 1-2: Module 1 - SDK Fundamentals
├── Days 3-4: Module 2 - Pydantic Models
└── Days 5-7: Module 3 - Structured Outputs

Week 2: Core Skills
├── Days 1-3: Module 4 - Tool Use
└── Days 4-7: Module 5 - Pydantic AI Framework

Week 3-4: Agent Development
├── Days 1-5: Module 6 - Building AI Agents
└── Days 6-10: Module 7 - Multi-Agent Systems

Week 5: Advanced & Projects
├── Days 1-3: Module 8 - MCP
└── Days 4-7: Build a project from Project Ideas
```

### Time Estimates per Module

| Module | Estimated Time | Difficulty |
|--------|---------------|------------|
| 1. SDK Fundamentals | 2-3 hours | ⭐ Beginner |
| 2. Pydantic Models | 2-3 hours | ⭐ Beginner |
| 3. Structured Outputs | 3-4 hours | ⭐⭐ Intermediate |
| 4. Tool Use | 4-5 hours | ⭐⭐ Intermediate |
| 5. Pydantic AI | 5-6 hours | ⭐⭐ Intermediate |
| 6. AI Agents | 6-8 hours | ⭐⭐⭐ Advanced |
| 7. Multi-Agent | 8-10 hours | ⭐⭐⭐ Advanced |
| 8. MCP | 4-5 hours | ⭐⭐⭐ Advanced |

**Total:** ~35-45 hours of focused learning

### Milestones

- [ ] **Milestone 1** (End of Week 1): Can make API calls and get structured JSON responses
- [ ] **Milestone 2** (End of Week 2): Can build tools that Claude can call
- [ ] **Milestone 3** (End of Week 4): Can build autonomous agents
- [ ] **Milestone 4** (End of Week 5): Can build production-ready multi-agent systems

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

| Module | Time | Status | Started | Completed |
|--------|------|--------|---------|-----------|
| 1. SDK Fundamentals | 2-3h | ⬜ Not Started | | |
| 2. Pydantic Models | 2-3h | ⬜ Not Started | | |
| 3. Structured Outputs | 3-4h | ⬜ Not Started | | |
| 4. Tool Use | 4-5h | ⬜ Not Started | | |
| 5. Pydantic AI | 5-6h | ⬜ Not Started | | |
| 6. AI Agents | 6-8h | ⬜ Not Started | | |
| 7. Multi-Agent | 8-10h | ⬜ Not Started | | |
| 8. MCP | 4-5h | ⬜ Not Started | | |

**Status Legend:** ⬜ Not Started | 🔄 In Progress | ✅ Completed | ⏸️ Paused

---

## License

MIT
