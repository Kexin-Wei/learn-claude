"""Shared utilities for c01_feature_probe.py scripts.

Each tutorial exposes a `probe_features()` function returning dict[str, ProbeResult].
The c01 scripts import and call these directly — no subprocess, no markers.
"""
import csv
from dataclasses import dataclass
from pathlib import Path

CSV_PATH = Path(__file__).parent / "c01_comparison.csv"

FEATURES = [
    "Agent loop", "Custom tools", "Web search", "File tools", "Code execution",
    "Structured output", "Multi-agent", "Guardrails", "Hooks / lifecycle",
    "Tracing dashboard", "Permission system", "Plan mode", "TodoWrite / tasks",
    "MCP support", "Streaming", "Session resume",
    "Shell", "File read", "File write", "File edit", "Image generation",
    "Tool search", "Agent nesting", "Context management", "Auto memory",
    "Skills (on-demand)", "CLAUDE.md / rules",
]


@dataclass
class ProbeResult:
    status: str  # PASS, FAIL, SKIP
    evidence: str
    source: str  # e.g. "t01", "import", "flag", "known"


def pass_(evidence: str, source: str) -> ProbeResult:
    return ProbeResult("PASS", evidence, source)


def fail(evidence: str, source: str) -> ProbeResult:
    return ProbeResult("FAIL", evidence, source)


def skip(evidence: str, source: str) -> ProbeResult:
    return ProbeResult("SKIP", evidence, source)


def merge_results(
    *result_dicts: dict[str, ProbeResult],
) -> dict[str, ProbeResult]:
    """Merge multiple probe result dicts. PASS wins over FAIL; earlier dicts have priority."""
    collected: dict[str, ProbeResult] = {}
    for d in result_dicts:
        for feature, result in d.items():
            if feature not in collected or (
                collected[feature].status != "PASS" and result.status == "PASS"
            ):
                collected[feature] = result
    return collected


def format_results(results: dict[str, ProbeResult]) -> dict[str, str]:
    """Convert ProbeResults to display strings for CSV."""
    output: dict[str, str] = {}
    for feature in FEATURES:
        if feature in results:
            r = results[feature]
            if r.status == "PASS":
                output[feature] = f"Yes ({r.source}: {r.evidence})"
            elif r.status == "FAIL":
                output[feature] = f"No ({r.source}: {r.evidence})"
            elif r.status == "SKIP":
                output[feature] = f"N/A ({r.source}: {r.evidence})"
        else:
            output[feature] = "? (not checked)"
    return output


def upsert_csv(sdk_name: str, row: dict[str, str]) -> None:
    """Read existing CSV, update this SDK's column, write back."""
    data: dict[str, dict[str, str]] = {f: {} for f in FEATURES}
    sdks: list[str] = []
    if CSV_PATH.exists():
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            sdks = [c for c in (reader.fieldnames or []) if c != "Feature"]
            for r in reader:
                feat = r.get("Feature", "")
                if feat in data:
                    for s in sdks:
                        if s in r:
                            data[feat][s] = r[s]
    if sdk_name not in sdks:
        sdks.append(sdk_name)
    for feat, val in row.items():
        if feat in data:
            data[feat][sdk_name] = val
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Feature"] + sdks)
        writer.writeheader()
        for feat in FEATURES:
            writer.writerow({"Feature": feat, **data[feat]})
