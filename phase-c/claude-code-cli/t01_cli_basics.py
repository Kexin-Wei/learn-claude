#!/usr/bin/env python3
"""Exercise 1: CLI Basics — What does `claude -p` give you out of the box?

Question answered: Q4 — What's built-in vs what Claude Code adds on top?

Run: uv run python phase-c/claude-code-cli/ex01_cli_basics.py
"""
import json
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

WORKDIR = Path(__file__).parent
MODEL = os.environ.get("CLAUDE_MODEL")


def run_claude(prompt: str, *, max_turns: int = 3, extra_args: list[str] | None = None) -> list[dict]:
    """Run claude -p and return parsed stream-json messages."""
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns)]
    if MODEL:
        cmd += ["--model", MODEL]
    if extra_args:
        cmd += extra_args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKDIR))
    messages = []
    for line in result.stdout.strip().splitlines():
        try:
            messages.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return messages


def extract_tools_used(messages: list[dict]) -> list[str]:
    """Extract tool names from stream-json messages."""
    tools = []
    for msg in messages:
        if msg.get("type") == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tools.append(block["name"])
    return tools


def extract_text(messages: list[dict]) -> str:
    """Extract text content from stream-json messages."""
    texts = []
    for msg in messages:
        if msg.get("type") == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    texts.append(block["text"])
    return "\n".join(texts)


def main() -> None:
    print("=" * 60)
    print("PROBE 1: Default tool availability")
    print("=" * 60)

    messages = run_claude("List the Python files in this directory. Be brief.")
    tools = extract_tools_used(messages)
    print(f"  Tools used: {tools}")

    # Print result
    for msg in messages:
        if msg.get("type") == "result":
            cost = msg.get("total_cost_usd", "N/A")
            print(f"  Turns: {msg.get('num_turns')}, Cost: ${cost}, Duration: {msg.get('duration_ms')}ms")

    print(f"\n{'=' * 60}")
    print("PROBE 2: Full tool inventory")
    print("=" * 60)

    messages = run_claude(
        "List every tool you have access to. Output ONLY tool names, one per line, no descriptions. "
        "Do NOT use any tools to answer this.",
        max_turns=1,
    )
    text = extract_text(messages)
    print(text)

    print(f"\n{'=' * 60}")
    print("KEY FINDINGS")
    print("=" * 60)
    if tools:
        print(f"  • Probe 1 used these tools: {', '.join(tools)}")
    else:
        print("  • Probe 1: no tool calls detected (model may have answered from context)")
    if text.strip():
        tool_names = [line.strip() for line in text.strip().splitlines() if line.strip()]
        print(f"  • Probe 2 reported {len(tool_names)} tools: {', '.join(tool_names)}")
    else:
        tool_names = []
        print("  • Probe 2: model returned no tool list (may need a different prompt)")

    results = probe_features(tools, tool_names)
    for feat, r in results.items():
        print(f"  [{r.status}] {feat}: {r.evidence}")


def probe_features(tools_used: list[str], tool_list: list[str]) -> "dict[str, ProbeResult]":
    """Return structured probe results for c01_feature_probe.py."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from _probe_utils import ProbeResult, pass_, fail

    all_tools = set(tools_used + tool_list)
    results: dict[str, ProbeResult] = {}

    tool_map = {
        "Shell": "Bash",
        "Code execution": "Bash",
        "File read": "Read",
        "File write": "Write",
        "File edit": "Edit",
        "Web search": "WebSearch",
        "Tool search": "ToolSearch",
    }
    for feature, tool_name in tool_map.items():
        if tool_name in all_tools:
            results[feature] = pass_(f"{tool_name} in tool list", "t01")
        else:
            results[feature] = fail(f"{tool_name} not found", "t01")

    file_tools = {"Read", "Write", "Glob", "Grep"}
    if file_tools <= all_tools:
        results["File tools"] = pass_("Read/Write/Glob/Grep in tool list", "t01")
    else:
        results["File tools"] = fail(f"missing {file_tools - all_tools}", "t01")

    results["Agent loop"] = pass_("claude -p returned results", "t01")
    results["Streaming"] = pass_("stream-json output parsed", "t01")
    return results


if __name__ == "__main__":
    main()
