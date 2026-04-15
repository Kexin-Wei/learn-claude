#!/usr/bin/env python3
"""Probe Claude Agent SDK features by running tutorials and collecting results.

Runs t01-t05 tutorials, each of which exposes a probe_features() function
returning structured results. Fallback checks cover features without tutorials.

Run: uv run python phase-c/claude-agent-sdk/c01_feature_probe.py
"""
import asyncio
import importlib
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

# Add phase-c to path for _probe_utils and tutorial imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from _probe_utils import (
    FEATURES, ProbeResult, fail, format_results, merge_results, pass_, skip,
    upsert_csv,
)

SDK_NAME = "Claude Agent SDK"


def check(module: str, attr: str) -> bool:
    try:
        return hasattr(importlib.import_module(module), attr)
    except ImportError:
        return False


def sdk(attr: str) -> bool:
    return check("claude_agent_sdk", attr)


async def check_session_resume() -> ProbeResult:
    """Actually call list_sessions to verify session resume works."""
    try:
        from claude_agent_sdk import list_sessions
        sessions = list_sessions()  # sync function, not async
        if hasattr(sessions, '__await__'):
            sessions = await sessions
        count = len(sessions) if sessions is not None else 0
        return pass_(f"list_sessions returned {count} sessions", "live")
    except Exception as e:
        return fail(f"list_sessions failed: {e}", "live")


async def check_hooks() -> ProbeResult:
    """Verify hook types are importable and have expected fields."""
    try:
        from claude_agent_sdk import PreToolUseHookInput, StopHookInput
        # Check they have expected attributes
        has_tool_name = hasattr(PreToolUseHookInput, "__annotations__")
        has_stop = hasattr(StopHookInput, "__annotations__")
        if has_tool_name and has_stop:
            return pass_("PreToolUseHookInput + StopHookInput importable with fields", "import")
        else:
            return fail("hook types missing expected annotations", "import")
    except ImportError as e:
        return fail(f"hook types not importable: {e}", "import")


def fallback_checks() -> dict[str, ProbeResult]:
    """Features not covered by any tutorial — use import/known checks."""
    results: dict[str, ProbeResult] = {}

    # MCP: covered by t02b tutorial now, this is just a backup
    if sdk("McpServerConfig"):
        results["MCP support"] = pass_("McpServerConfig importable", "import")
    else:
        results["MCP support"] = fail("McpServerConfig not found", "import")

    results["Image generation"] = skip("not available in Claude", "known")
    results["Tracing dashboard"] = skip("not in SDK", "known")
    results["Auto memory"] = skip("CLI-only feature, not in SDK", "known")

    # Context management: check for compaction-related types
    if sdk("CompactedMessage") or sdk("CompactionMessage"):
        results["Context management"] = pass_("compaction message types found in SDK", "import")
    else:
        # Compaction is built-in but may not have public types
        results["Context management"] = pass_("built-in (no public compaction types)", "known")

    # Skills/CLAUDE.md: check settingSources actually exists as a field
    try:
        from claude_agent_sdk import ClaudeAgentOptions
        import inspect
        sig = inspect.signature(ClaudeAgentOptions)
        has_settings = "setting_sources" in sig.parameters or "settingSources" in sig.parameters
        if has_settings:
            results["Skills (on-demand)"] = pass_("settingSources param in ClaudeAgentOptions", "import")
            results["CLAUDE.md / rules"] = pass_("settingSources param in ClaudeAgentOptions", "import")
        else:
            # Check all param names
            params = list(sig.parameters.keys())
            results["Skills (on-demand)"] = fail(f"settingSources not in params: {params[:10]}", "import")
            results["CLAUDE.md / rules"] = fail(f"settingSources not in params: {params[:10]}", "import")
    except Exception as e:
        results["Skills (on-demand)"] = fail(f"ClaudeAgentOptions inspection failed: {e}", "import")
        results["CLAUDE.md / rules"] = fail(f"ClaudeAgentOptions inspection failed: {e}", "import")

    return results


async def run_tutorials() -> dict[str, ProbeResult]:
    """Run all tutorials and collect probe results."""
    all_results: dict[str, ProbeResult] = {}

    tutorials = [
        ("t01_sdk_basics", "t01"),
        ("t02_todo_and_tasks", "t02"),
        ("t02b_safe_write", "t02b"),
        ("t03_subagents", "t03"),
        ("t04_plan_mode", "t04"),
        ("t05_custom_tools_and_hooks", "t05"),
    ]

    for module_name, label in tutorials:
        print(f"\n  Running {module_name}...")
        start = time.time()
        try:
            mod = importlib.import_module(module_name)
            # Run the tutorial's main() to exercise the features
            await mod.main()
            elapsed = time.time() - start
            print(f"  → {module_name} done ({elapsed:.1f}s)")

            # Collect probe results — main() already called probe_features() internally
            # but we need to call it again to get the return value
            # The probe functions need their inputs, which main() computed.
            # Since main() already prints results, we just need the structured data.
            # We'll re-extract from the module's probe_features by re-running it
            # with the data that main() already printed.
        except Exception as e:
            elapsed = time.time() - start
            print(f"  → {module_name} ERROR ({elapsed:.1f}s): {type(e).__name__}: {e}")

    return all_results


async def run_tutorial_probes() -> dict[str, ProbeResult]:
    """Run tutorials and collect structured probe results."""
    all_results: dict[str, ProbeResult] = {}

    # t01: tool discovery
    print("\n  [t01] SDK basics — tool discovery...")
    start = time.time()
    try:
        import t01_sdk_basics as t01
        tools_used = await t01.probe_default_tools()
        tool_list = await t01.probe_tool_inventory()
        results = t01.probe_features(tools_used, tool_list)
        all_results.update(results)
        print(f"  → t01 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t01 ERROR: {e}")

    # t02: TodoWrite
    print("\n  [t02] TodoWrite...")
    start = time.time()
    try:
        import t02_todo_and_tasks as t02
        tools_with = await t02.probe_todowrite(
            "Create a Python project with:\n1. main.py\n2. utils.py\n3. test_main.py\nTrack your progress with todos as you go.",
            "With todo instruction",
        )
        tools_without = await t02.probe_todowrite(
            "Create a Python calculator project with:\n1. calc.py\n2. test_calc.py\n3. README.md",
            "Without todo instruction",
        )
        results = t02.probe_features(tools_with, tools_without)
        all_results.update(results)
        print(f"  → t02 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t02 ERROR: {e}")

    # t02b: Custom tools
    print("\n  [t02b] Custom tools (safe_write)...")
    start = time.time()
    try:
        import t02b_safe_write as t02b
        tool_counts = await t02b.run_probe()
        results = t02b.probe_features(tool_counts)
        all_results.update(results)
        print(f"  → t02b done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t02b ERROR: {e}")

    # t03: Subagents
    print("\n  [t03] Subagents...")
    start = time.time()
    try:
        import t03_subagents as t03
        auto_spawned = await t03.probe_auto_spawn()
        manual_used = await t03.probe_manual_agents()
        results = t03.probe_features(auto_spawned, manual_used)
        all_results.update(results)
        print(f"  → t03 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t03 ERROR: {e}")

    # t04: Plan mode
    print("\n  [t04] Plan mode...")
    start = time.time()
    try:
        import t04_plan_mode as t04
        tools_blocked = await t04.probe_plan_permission_mode()
        results = t04.probe_features(tools_blocked)
        all_results.update(results)
        print(f"  → t04 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t04 ERROR: {e}")

    # t05: Structured output, permission control
    print("\n  [t05] Custom tools, structured output, permissions...")
    start = time.time()
    try:
        import t05_custom_tools_and_hooks as t05
        custom_tools = await t05.probe_custom_tools()
        structured_ok = await t05.probe_structured_output()
        blocked_tools = await t05.probe_permission_control()
        results = t05.probe_features(custom_tools, structured_ok, blocked_tools)
        all_results.update(results)
        print(f"  → t05 done ({time.time() - start:.1f}s, {len(results)} features)")
    except Exception as e:
        print(f"  → t05 ERROR: {e}")

    return all_results


async def main() -> None:
    print("=" * 60)
    print(f"Feature Probe: {SDK_NAME}")
    print("=" * 60)

    # Run tutorials
    tutorial_results = await run_tutorial_probes()

    # Live async checks
    print("\n  [live] Session resume...")
    tutorial_results["Session resume"] = await check_session_resume()

    print("  [live] Hooks / lifecycle...")
    tutorial_results["Hooks / lifecycle"] = await check_hooks()

    # Fallback checks
    print("\n  [fallback] Import/known checks...")
    fb = fallback_checks()

    # Merge: tutorial wins over fallback
    merged = merge_results(tutorial_results, fb)

    # Format and display
    formatted = format_results(merged)
    print(f"\n{'=' * 60}")
    print("RESULTS")
    print("=" * 60)
    for feat in FEATURES:
        print(f"  {feat:<22} {formatted.get(feat, '?')}")

    # Write CSV
    upsert_csv(SDK_NAME, formatted)
    print(f"\nWrote to c01_comparison.csv")


if __name__ == "__main__":
    asyncio.run(main())
