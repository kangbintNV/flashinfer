"""Unit tests for the pull-request API and documentation check tooling."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_pr_api_diff import exported_names, extract_public_apis  # noqa: E402
from check_pr_document import load_findings  # noqa: E402
from pr_checks import api_rst_check, ast_utils, config, docstring_checks  # noqa: E402
from pr_checks.registry import API_RST_MISSING, DOCSTRING_COMPLETENESS  # noqa: E402


def test_api_rst_check_reports_new_module_without_rst() -> None:
    results = api_rst_check.run_check({"flashinfer.new_module": {"new_api"}}, {}, {})
    assert results == [
        {
            "module": "flashinfer.new_module",
            "documented": [],
            "api_decorated": ["new_api"],
            "deprecated": [],
            "missing": ["new_api"],
            "stale": [],
        }
    ]


def test_docstring_check_skips_testing_class_members(
    tmp_path: Path, monkeypatch
) -> None:
    package = tmp_path / "flashinfer"
    package.mkdir()
    (package / "testing.py").write_text(
        "class Helper:\n"
        "    @flashinfer_api\n"
        "    def undocumented(self):\n"
        "        pass\n"
    )
    monkeypatch.setattr(docstring_checks, "FLASHINFER_ROOT", tmp_path)
    assert docstring_checks.collect_records(package) == []


def test_relative_alias_from_normal_module(tmp_path: Path) -> None:
    package = tmp_path / "flashinfer"
    package.mkdir()
    (package / "a.py").write_text("@flashinfer_api\ndef original():\n    pass\n")
    (package / "b.py").write_text("from .a import original as public_name\n")
    assert ast_utils.collect_module_alias_exports(package) == {
        "flashinfer.b": {"public_name"}
    }


def test_api_diff_supports_suffix_decorators_and_absolute_exports() -> None:
    source = "@flashinfer.utils.flashinfer_api\ndef public():\n    pass\n"
    assert set(extract_public_apis("flashinfer/example.py", source)) == {"public"}
    assert exported_names("from flashinfer.example import public\n") == {
        "public": "flashinfer.example"
    }
    assert exported_names("from .example import public\n") == {
        "public": "flashinfer.example"
    }


def test_load_findings_uses_registry_slug(tmp_path: Path) -> None:
    (tmp_path / "api_rst_pr-head_1.json").write_text(
        json.dumps(
            {
                "modules": [
                    {"module": "flashinfer.example", "missing": ["public"], "stale": []}
                ]
            }
        )
    )
    (tmp_path / "docstring_checks.json").write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "check": DOCSTRING_COMPLETENESS,
                        "module": "flashinfer.example",
                        "symbol": "public",
                        "file": "flashinfer/example.py",
                        "line": 3,
                        "message": "Missing docstring",
                    }
                ]
            }
        )
    )
    (tmp_path / "flashinfer_cross_source_check.json").write_text(
        json.dumps({"findings": []})
    )
    findings = load_findings(tmp_path)
    assert any(finding.check == API_RST_MISSING for finding in findings)
    assert any(finding.check == DOCSTRING_COMPLETENESS for finding in findings)


def test_config_defaults_to_repository_root() -> None:
    assert config.REPO_ROOT == REPO_ROOT
    assert config.FLASHINFER_ROOT == REPO_ROOT


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def _commit(repo: Path, message: str) -> str:
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def test_pr_document_reports_only_head_delta(tmp_path: Path) -> None:
    repo = tmp_path / "fixture"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    package = repo / "flashinfer"
    package.mkdir()
    (package / "existing.py").write_text("@flashinfer_api\ndef old_api():\n    pass\n")
    base = _commit(repo, "base")
    (package / "new.py").write_text("@flashinfer_api\ndef new_api():\n    pass\n")
    head = _commit(repo, "head")
    report = tmp_path / "report.json"
    env = os.environ | {"PYTHONPATH": str(SCRIPTS_DIR)}
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "check_pr_document.py"),
            "--base",
            base,
            "--head",
            head,
            "--strict",
            "--report-json",
            str(report),
        ],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    findings = json.loads(report.read_text())["findings"]
    messages = [finding["message"] for finding in findings]
    assert "flashinfer.new.new_api is absent from docs/api/*.rst" in messages
    assert "flashinfer.new.new_api: Missing docstring" in messages
    assert not any("old_api" in message for message in messages)
