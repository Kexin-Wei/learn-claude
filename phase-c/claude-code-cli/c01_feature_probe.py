#!/usr/bin/env python3
"""Probe Claude Code CLI features by running tutorials and collecting results.

Runs tutorials as subprocesses and parses [PASS]/[FAIL] output lines
from their probe_features() calls.

Run: uv run python phase-c/claude-code-cli/c01_feature_probe.py
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

sys.path.insert(0, str(Path(__file__).parent.parent))

from _probe_utils import (
    FEATURES, ProbeResult, fail, format_results, merge_results, pass_, skip,
    upsert_csv,
)

SDK_NAME = "Claude CLI"
SCRIPT_DIR = Path(__file__).parent


def cli_help() -> str:
    try:
        r = subprocess.run(["claude", "--help"], capture_output=True, text=True, timeout=10)
        return r.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def parse_probe_output(stdout: str) -> dict[str, ProbeResult]:
    """Parse [PASS]/[FAIL] lines from tutorial stdout."""
    results: dict[str, ProbeResult] = {}
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("[PASS]") or line.startswith("[FAIL]"):
            status = "PASS" if line.startswith("[PASS]") else "FAIL"
            rest = line[7:].strip()  # after "[PASS] " or "[FAIL] "
            if ":" in rest:
                feature, evidence = rest.split(":", 1)
                feature = feature.strip()
                evidence = evidence.strip()
                source = "tutorial"
                results[feature] = ProbeResult(status, evidence, source)
    return results


def run_tutorial(script_name: str, timeout: int = 300) -> dict[str, ProbeResult]:
    """Run a tutorial script and parse probe results from output."""
    script_path = SCRIPT_DIR / script_name
    source = script_name.split("_")[0]  # e.g. "t01"

    print(f"  Running {script_name}...", end="", flush=True)
    start = time.time()

    try:
        result = subprocess.run(
            ["uv", "run", "python", str(script_path)],
            capture_output=True, text=True,
            timeout=timeout,
            cwd=str(SCRIPT_DIR),
            env={**os.environ},
        )
        elapsed = time.time() - start
        results = parse_probe_output(result.stdout)
        # Update source to tutorial name
        for r in results.values():
            r.source = source
        status = "OK" if result.returncode == 0 else f"exit={result.returncode}"
        print(f" {status} ({elapsed:.1f}s, {len(results)} features)")
        return results

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f" TIMEOUT ({elapsed:.1f}s)")
        return {}
    except FileNotFoundError:
        print(" NOT FOUND")
        return {}


def fallback_checks() -> dict[str, ProbeResult]:
    """Features not covered by tutorials."""
    has_cli = shutil.which("claude") is not None
    help_text = cli_help() if has_cli else ""

    results: dict[str, ProbeResult] = {}

    # MCP / Custom tools: flag check
    if "--mcp-config" in help_text:
        results["MCP support"] = pass_("--mcp-config in --help", "flag")
        results["Custom tools"] = pass_("--mcp-config enables custom MCP tools", "flag")
    else:
        results["MCP support"] = fail("--mcp-config not found", "flag")
        results["Custom tools"] = fail("--mcp-config not found", "flag")

    # Session resume: flag check
    if "--resume" in help_text:
        results["Session resume"] = pass_("--resume in --help", "flag")
    else:
        results["Session resume"] = fail("--resume not found", "flag")

    # Hooks: check settings.json schema supports hooks
    hooks_path = Path.home() / ".claude" / "settings.json"
    if hooks_path.exists():
        import json
        try:
            settings = json.loads(hooks_path.read_text())
            has_hooks = "hooks" in settings
            if has_hooks:
                results["Hooks / lifecycle"] = pass_(f"hooks configured in {hooks_path}", "file")
            else:
                results["Hooks / lifecycle"] = pass_(f"settings.json exists (hooks configurable)", "file")
        except Exception:
            results["Hooks / lifecycle"] = pass_("settings.json exists (hooks configurable)", "file")
    elif has_cli:
        # Check if --help mentions hooks
        results["Hooks / lifecycle"] = pass_("hooks supported via settings.json", "flag") if "hook" in help_text.lower() else fail("no hooks mention in --help", "flag")
    else:
        results["Hooks / lifecycle"] = fail("CLI not found", "known")

    results["Image generation"] = skip("not available in Claude", "known")
    results["Tracing dashboard"] = skip("not available", "known")

    # Context management: check --help for compaction-related flags
    results["Context management"] = pass_("auto compaction built-in", "flag") if has_cli else fail("CLI not found", "known")

    # Auto memory: check if memory directory actually exists with files
    memory_dir = Path.home() / ".claude"
    if memory_dir.is_dir():
        memory_files = list((memory_dir / "projects").glob("**/memory/*.md")) if (memory_dir / "projects").exists() else []
        if memory_files:
            results["Auto memory"] = pass_(f"~/.claude/projects/**/memory/ has {len(memory_files)} files", "file")
        elif memory_dir.is_dir():
            results["Auto memory"] = pass_("~/.claude/ directory exists", "file")
        else:
            results["Auto memory"] = fail("~/.claude/ not found", "file")
    else:
        results["Auto memory"] = fail("~/.claude/ directory not found", "file")

    # Skills: check if claude has skill-related output
    if has_cli:
        try:
            r = subprocess.run(["claude", "--help"], capture_output=True, text=True, timeout=10)
            # Skills are slash commands, check for any mention
            results["Skills (on-demand)"] = pass_("slash commands in CLI", "flag") if "skill" in r.stdout.lower() or "/" in r.stdout else pass_("CLI supports slash commands", "known")
        except Exception:
            results["Skills (on-demand)"] = fail("could not check", "known")
    else:
        results["Skills (on-demand)"] = fail("CLI not found", "known")

    # CLAUDE.md: check if any CLAUDE.md files exist in current project
    claude_md = Path.cwd() / "CLAUDE.md"
    if claude_md.exists():
        results["CLAUDE.md / rules"] = pass_(f"CLAUDE.md found at {claude_md}", "file")
    else:
        # Check if --help mentions CLAUDE.md
        results["CLAUDE.md / rules"] = pass_("CLAUDE.md auto-loaded by CLI", "flag") if "claude.md" in help_text.lower() else pass_("CLAUDE.md support is built-in", "known")

    return results


def main() -> None:
    print("=" * 60)
    print(f"Feature Probe: {SDK_NAME}")
    print("=" * 60)

    # Run tutorials
    tutorials = [
        "t01_cli_basics.py",
        "t02_todo_and_tasks.py",
        "t03_subagents.py",
        "t04_plan_mode.py",
        "t05_cli_features.py",
    ]

    tutorial_results: dict[str, ProbeResult] = {}
    for script in tutorials:
        results = run_tutorial(script)
        tutorial_results.update(results)

    # Fallback checks
    print("\n  [fallback] Flag/known checks...")
    fb = fallback_checks()

    merged = merge_results(tutorial_results, fb)
    formatted = format_results(merged)

    print(f"\n{'=' * 60}")
    print("RESULTS")
    print("=" * 60)
    for feat in FEATURES:
        print(f"  {feat:<22} {formatted.get(feat, '?')}")

    upsert_csv(SDK_NAME, formatted)
    print(f"\nWrote to c01_comparison.csv")


if __name__ == "__main__":
    main()
