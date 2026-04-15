#!/usr/bin/env python3
"""Probe GLM (ZhipuAI) features by running tutorials.

GLM is a raw LLM API — most agent features are N/A (you build them yourself).
When used via z.ai proxy, it inherits Claude's tooling.

Run: uv run python phase-c/glm/c01_feature_probe.py
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from _probe_utils import (
    FEATURES, ProbeResult, fail, format_results, merge_results, pass_, skip,
    upsert_csv,
)

SDK_NAME = "GLM (Zhipu)"


def load_zai_env() -> bool:
    """Load z.ai proxy env vars from settings.local.json. Returns True if ready."""
    settings_path = Path(__file__).parent / ".claude" / "settings.local.json"
    if not settings_path.exists():
        print(f"  z.ai settings not found: {settings_path}")
        return False
    try:
        settings = json.loads(settings_path.read_text())
        env = settings.get("env", {})
        token = env.get("ANTHROPIC_AUTH_TOKEN", "")
        if not token or token == "your-zai-api-key-here":
            print("  z.ai token not configured")
            return False
        os.environ["ANTHROPIC_AUTH_TOKEN"] = token
        os.environ.setdefault("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        os.environ.setdefault("API_TIMEOUT_MS", "3000000")
        os.environ.setdefault("CLAUDE_MODEL", env.get("CLAUDE_MODEL", "sonnet"))
        return True
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  z.ai settings parse error: {e}")
        return False


async def probe_proxy_tools() -> dict[str, ProbeResult]:
    """Actually query the z.ai proxy to discover available tools."""
    try:
        from claude_agent_sdk import (
            AssistantMessage, ClaudeAgentOptions, TextBlock, query,
        )
    except ImportError:
        return {}

    model = os.environ.get("CLAUDE_MODEL", "sonnet")
    prompt = (
        "List every tool you have access to. "
        "Output ONLY the tool names, one per line, no descriptions, no numbering, no markdown."
    )

    tools: set[str] = set()
    try:
        async for msg in query(
            prompt=prompt,
            options=ClaudeAgentOptions(model=model, max_turns=1, permission_mode="bypassPermissions"),
        ):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        for line in block.text.splitlines():
                            name = line.strip().strip("-•*").strip()
                            if name and " " not in name:
                                tools.add(name)
    except Exception as e:
        return {"Agent loop": fail(f"z.ai proxy query failed: {e}", "proxy")}

    results: dict[str, ProbeResult] = {}
    results["Agent loop"] = pass_("query() via z.ai proxy returned results", "proxy")

    tool_map = {
        "Shell": "Bash", "Code execution": "Bash",
        "File read": "Read", "File write": "Write", "File edit": "Edit",
        "Web search": "WebSearch", "Tool search": "ToolSearch",
        "TodoWrite / tasks": "TodoWrite", "Multi-agent": "Agent",
    }
    for feature, tool_name in tool_map.items():
        if tool_name in tools:
            results[feature] = pass_(f"{tool_name} found via z.ai proxy", "proxy")
        else:
            results[feature] = fail(f"{tool_name} not found via proxy", "proxy")

    file_tools = {"Read", "Write", "Glob", "Grep"}
    if file_tools <= tools:
        results["File tools"] = pass_("Read/Write/Glob/Grep via proxy", "proxy")
    else:
        results["File tools"] = fail(f"missing {file_tools - tools} via proxy", "proxy")

    results["Streaming"] = pass_("async iteration via proxy worked", "proxy")
    return results


def fallback_checks(proxy_ready: bool) -> dict[str, ProbeResult]:
    """Features that can't be checked by proxy query."""
    results: dict[str, ProbeResult] = {}

    if proxy_ready:
        # These inherit from Claude SDK via proxy
        results["Guardrails"] = pass_("Claude hooks via z.ai proxy", "proxy")
        results["Hooks / lifecycle"] = pass_("Claude PreToolUse/Stop via z.ai", "proxy")
        results["Permission system"] = pass_("Claude PermissionMode via z.ai", "proxy")
        results["Plan mode"] = pass_("Claude plan mode via z.ai", "proxy")
        results["MCP support"] = pass_("Claude MCP via z.ai", "proxy")
        results["Session resume"] = pass_("Claude session resume via z.ai", "proxy")
        results["Structured output"] = pass_("Claude output_format via z.ai", "proxy")
        results["Context management"] = pass_("Claude auto compaction via z.ai", "proxy")
        results["Custom tools"] = pass_("Claude @tool + MCP via z.ai", "proxy")
    else:
        for feat in ["Guardrails", "Hooks / lifecycle", "Permission system", "Plan mode",
                      "MCP support", "Session resume", "Structured output", "Context management",
                      "Custom tools"]:
            results[feat] = skip("z.ai proxy not configured", "known")

    # Always N/A regardless of proxy
    results["Image generation"] = skip("not available", "known")
    results["Tracing dashboard"] = skip("not available", "known")
    results["Auto memory"] = skip("not available via z.ai", "known")
    results["Skills (on-demand)"] = skip("not available via z.ai", "known")
    results["CLAUDE.md / rules"] = skip("not available via z.ai", "known")
    results["Agent nesting"] = fail("1 level only", "known")

    return results


def run_tutorial_probes() -> dict[str, ProbeResult]:
    """Run GLM tutorials and collect probe results."""
    all_results: dict[str, ProbeResult] = {}

    # t01: basic chat, function calling, streaming
    print("\n  [t01] GLM basics...")
    start = time.time()
    try:
        import t01_glm_basics as t01
        t01.probe_basic_chat()
        t01.probe_multi_turn()
        t01.probe_tool_use()
        t01.probe_streaming()
        results = t01.probe_features()
        all_results.update(results)
        print(f"  → t01 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t01 ERROR: {e}")

    # t02: DIY agent loop
    print("\n  [t02] DIY agent loop...")
    start = time.time()
    try:
        import t02_build_agent_loop as t02
        t02.agent_loop(
            "List the files in the current directory, then read this script and tell me what it does in one sentence.",
        )
        results = t02.probe_features()
        all_results.update(results)
        print(f"  → t02 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t02 ERROR: {e}")

    return all_results


async def amain() -> None:
    print("=" * 60)
    print(f"Feature Probe: {SDK_NAME}")
    print("=" * 60)

    proxy_ready = load_zai_env()
    print(f"  z.ai proxy: {'ready' if proxy_ready else 'not configured'}")
    if proxy_ready:
        print(f"  Base URL: {os.environ.get('ANTHROPIC_BASE_URL')}")
        print(f"  Model: {os.environ.get('CLAUDE_MODEL')}")

    tutorial_results = run_tutorial_probes()

    # If proxy ready, actually query it for tool discovery
    proxy_results: dict[str, ProbeResult] = {}
    if proxy_ready:
        print("\n  [proxy] Querying z.ai for available tools...")
        proxy_results = await probe_proxy_tools()
        print(f"  → proxy query done ({len(proxy_results)} features)")

    print("\n  [fallback] Known checks...")
    fb = fallback_checks(proxy_ready)

    merged = merge_results(tutorial_results, proxy_results, fb)
    formatted = format_results(merged)

    print(f"\n{'=' * 60}")
    print("RESULTS")
    print("=" * 60)
    for feat in FEATURES:
        print(f"  {feat:<22} {formatted.get(feat, '?')}")

    upsert_csv(SDK_NAME, formatted)
    print(f"\nWrote to c01_comparison.csv")


if __name__ == "__main__":
    import asyncio
    asyncio.run(amain())
