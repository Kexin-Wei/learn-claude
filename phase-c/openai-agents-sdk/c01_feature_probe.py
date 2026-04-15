#!/usr/bin/env python3
"""Probe OpenAI Agents SDK features by running tutorials and import checks.

Run: uv run python phase-c/openai-agents-sdk/c01_feature_probe.py
"""
import asyncio
import importlib
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

SDK_NAME = "OpenAI Agents SDK"


def check(module: str, attr: str) -> bool:
    try:
        return hasattr(importlib.import_module(module), attr)
    except ImportError:
        return False


def ag(attr: str) -> bool:
    return check("agents", attr)


def fallback_checks() -> dict[str, ProbeResult]:
    """Features checked by import (hosted tools) or known values."""
    results: dict[str, ProbeResult] = {}

    # Hosted tools — check by import
    if ag("ShellTool"):
        results["Shell"] = pass_("ShellTool importable", "import")
    else:
        results["Shell"] = fail("ShellTool not found", "import")

    if ag("ImageGenerationTool"):
        results["Image generation"] = pass_("ImageGenerationTool importable", "import")
    else:
        results["Image generation"] = fail("ImageGenerationTool not found", "import")

    if ag("ApplyPatchTool"):
        results["File edit"] = pass_("ApplyPatchTool importable", "import")
    else:
        results["File edit"] = fail("ApplyPatchTool not found", "import")

    if ag("FileSearchTool"):
        results["File tools"] = pass_("FileSearchTool importable", "import")
    else:
        results["File tools"] = fail("FileSearchTool not found", "import")

    if ag("CodeInterpreterTool"):
        results["Code execution"] = pass_("CodeInterpreterTool importable", "import")
    else:
        results["Code execution"] = fail("CodeInterpreterTool not found", "import")

    if ag("MCPServerStdio") or ag("MCPServerSse"):
        results["MCP support"] = pass_("MCPServer* importable", "import")
    else:
        results["MCP support"] = fail("MCPServer not found", "import")

    # Streaming and Session resume: checked by live tests in run_extra_probes()

    # Known values
    results["File read"] = skip("DIY via @function_tool", "known")
    results["File write"] = skip("DIY via @function_tool", "known")
    results["Tool search"] = skip("not in SDK", "known")
    results["Permission system"] = skip("not in SDK", "known")
    results["Plan mode"] = skip("not in SDK", "known")
    results["TodoWrite / tasks"] = skip("not in SDK", "known")
    results["Context management"] = skip("manual", "known")
    results["Auto memory"] = skip("not in SDK", "known")
    results["Skills (on-demand)"] = skip("not in SDK", "known")
    results["CLAUDE.md / rules"] = skip("not in SDK", "known")

    return results


async def run_tutorial_probes() -> dict[str, ProbeResult]:
    """Run tutorials and collect probe results."""
    all_results: dict[str, ProbeResult] = {}

    # t01: basic agent, custom tools, web search, structured output
    print("\n  [t01] SDK basics...")
    start = time.time()
    try:
        import t01_sdk_basics as t01
        basic = await t01.probe_basic_agent()
        tools = await t01.probe_custom_tools()
        web = await t01.probe_web_search()
        structured = await t01.probe_structured_output()
        results = t01.probe_features(basic, tools, web, structured)
        all_results.update(results)
        print(f"  → t01 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t01 ERROR: {e}")

    # t02: handoffs, guardrails
    print("\n  [t02] Handoffs & guardrails...")
    start = time.time()
    try:
        import t02_handoffs_and_guardrails as t02
        handoff_results = await t02.probe_handoffs()
        guardrail_results = await t02.probe_guardrails()
        results = t02.probe_features(handoff_results, guardrail_results)
        all_results.update(results)
        print(f"  → t02 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t02 ERROR: {e}")

    # t03: hooks, tracing
    print("\n  [t03] Hooks & tracing...")
    start = time.time()
    try:
        import t03_hooks_and_tracing as t03
        run = await t03.probe_run_hooks()
        agent = await t03.probe_agent_hooks()
        tracing = await t03.probe_tracing()
        results = t03.probe_features(run, agent, tracing)
        all_results.update(results)
        print(f"  → t03 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t03 ERROR: {e}")

    return all_results


async def run_extra_probes() -> dict[str, ProbeResult]:
    """Live tests for streaming and session resume."""
    from agents import Agent, Runner
    import os

    results: dict[str, ProbeResult] = {}
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    # Streaming: actually call run_streamed
    print("\n  [live] Streaming (run_streamed)...")
    try:
        agent = Agent(name="streamer", instructions="Be concise.", model=model)
        result = Runner.run_streamed(agent, input="Say hi in one word.")
        chunks = 0
        async for event in result.stream_events():
            chunks += 1
        # Access final output from the completed result
        final = result.final_output
        if final and chunks > 0:
            results["Streaming"] = pass_(f"run_streamed produced {chunks} events", "live")
        else:
            results["Streaming"] = fail(f"no events from run_streamed", "live")
    except Exception as e:
        results["Streaming"] = fail(f"run_streamed failed: {e}", "live")

    # Session resume: run once, then resume with previous_response_id
    print("  [live] Session resume (previous_response_id)...")
    try:
        agent = Agent(name="memory-test", instructions="Be concise.", model=model)
        result1 = await Runner.run(agent, input="Remember the number 42.")
        # Find the response ID from raw_responses
        prev_id = None
        if hasattr(result1, "raw_responses") and result1.raw_responses:
            last_resp = result1.raw_responses[-1]
            # Try common attribute names for response ID
            prev_id = getattr(last_resp, "id", None) or getattr(last_resp, "response_id", None)
        if prev_id:
            result2 = await Runner.run(agent, input="What number did I tell you?", previous_response_id=prev_id)
            results["Session resume"] = pass_(f"previous_response_id={prev_id[:20]}... accepted", "live")
        else:
            # Can't find response ID — check if the API supports it at all
            resp_attrs = [a for a in dir(result1.raw_responses[-1]) if not a.startswith("_")] if result1.raw_responses else []
            results["Session resume"] = fail(f"no response ID found in attrs: {resp_attrs[:10]}", "live")
    except Exception as e:
        results["Session resume"] = fail(f"previous_response_id failed: {e}", "live")

    return results


async def main() -> None:
    print("=" * 60)
    print(f"Feature Probe: {SDK_NAME}")
    print("=" * 60)

    tutorial_results = await run_tutorial_probes()

    extra_results = await run_extra_probes()

    print("\n  [fallback] Import/known checks...")
    fb = fallback_checks()

    merged = merge_results(tutorial_results, extra_results, fb)
    formatted = format_results(merged)

    print(f"\n{'=' * 60}")
    print("RESULTS")
    print("=" * 60)
    for feat in FEATURES:
        print(f"  {feat:<22} {formatted.get(feat, '?')}")

    upsert_csv(SDK_NAME, formatted)
    print(f"\nWrote to c01_comparison.csv")


if __name__ == "__main__":
    asyncio.run(main())
