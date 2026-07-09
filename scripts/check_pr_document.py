#!/usr/bin/env python3
"""Report documentation-check findings introduced by one pull request.

This is a PR adapter for the complete static rule set from
``flashinfer_document_check``.  Each rule runs on both commits, then only
findings present at the PR head but absent from its base are reported.  This
avoids turning pre-existing repository debt into contributor-facing warnings.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_DIR = ROOT / "scripts" / "pr_static_checks" / "doc_checks"


@dataclass(frozen=True, order=True)
class Finding:
    check: str
    path: str
    line: int
    message: str


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], stderr=subprocess.PIPE)


def archive_revision(revision: str, destination: Path) -> None:
    data = git("archive", "--format=tar", revision)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(destination, filter="data")


def run_checker(source: Path, output: Path, label: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ | {
        "FLASHINFER_SRC": str(source),
        "DOC_CHECK_OUT": str(output),
        "DOC_CHECK_VERSION": label,
    }
    for script in (
        "flashinfer_doc_test.py",
        "doc_check_extended.py",
        "cross_source_check.py",
    ):
        result = subprocess.run(
            [sys.executable, str(CHECKER_DIR / script)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        # A result of 1 means the checker found drift.  Any other non-zero
        # result is an execution failure and must not be mistaken for a finding.
        if result.returncode not in (0, 1):
            raise RuntimeError(f"{script} failed:\n{result.stdout}\n{result.stderr}")


def location_parts(location: str) -> tuple[str, int]:
    path, separator, line = location.rpartition(":")
    if separator and line.isdigit():
        return path, int(line)
    return location or "docs", 1


def load_findings(output: Path) -> set[Finding]:
    findings: set[Finding] = set()

    for report in output.glob("*doc_gap_*.json"):
        payload = json.loads(report.read_text())
        for module in payload.get("modules", []):
            name = module["module"]
            for symbol in module.get("missing", []):
                findings.add(
                    Finding(
                        "api_rst_missing",
                        "docs/api",
                        1,
                        f"{name}.{symbol} is absent from docs/api/*.rst",
                    )
                )
            for symbol in module.get("stale", []):
                findings.add(
                    Finding(
                        "api_rst_stale",
                        "docs/api",
                        1,
                        f"{name}.{symbol} is documented but no longer public",
                    )
                )

    for filename in (
        "flashinfer_doc_check_extended.json",
        "flashinfer_cross_source_check.json",
    ):
        report = output / filename
        payload = json.loads(report.read_text())
        for item in payload.get("findings", []):
            path = item.get("file", "")
            line = int(item.get("line", 0) or 0)
            if not path:
                path, line = location_parts(item.get("location", ""))
            subject = ".".join(
                part
                for part in (item.get("module", ""), item.get("symbol", ""))
                if part
            )
            message = f"{subject}: {item['message']}" if subject else item["message"]
            findings.add(Finding(item["check"], path, line or 1, message))
    return findings


def emit(finding: Finding, github_actions: bool) -> str:
    text = f"[{finding.check}] {finding.path}:{finding.line} {finding.message}"
    if github_actions:
        escaped = text.replace("%", "%25").replace("\n", " ").replace("\r", "")
        print(f"::warning file={finding.path},line={finding.line}::{escaped}")
    print(text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Base commit SHA")
    parser.add_argument("--head", required=True, help="Head commit SHA")
    parser.add_argument(
        "--github-actions", action="store_true", help="Emit workflow annotations"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Fail when this PR introduces findings"
    )
    parser.add_argument("--report-json", type=Path, help="Write findings as JSON")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="flashinfer-pr-doc-check-") as temp:
        temp_root = Path(temp)
        base_src, head_src = temp_root / "base", temp_root / "head"
        archive_revision(args.base, base_src)
        archive_revision(args.head, head_src)
        base_out, head_out = temp_root / "base-out", temp_root / "head-out"
        run_checker(base_src, base_out, "pr-base")
        run_checker(head_src, head_out, "pr-head")
        new_findings = sorted(load_findings(head_out) - load_findings(base_out))

    print(f"Static documentation checks: {len(new_findings)} new finding(s)")
    for finding in new_findings:
        emit(finding, args.github_actions)
    if not new_findings:
        print("No new static documentation findings introduced by this PR.")
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(
            json.dumps(
                {
                    "check": "static_documentation",
                    "base": args.base,
                    "head": args.head,
                    "findings": [finding.__dict__ for finding in new_findings],
                },
                indent=2,
            )
            + "\n"
        )
    return 1 if args.strict and new_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
