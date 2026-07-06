#!/usr/bin/env python3
"""Check PR public-API changes for accompanying documentation updates.

The checker is deliberately dependency-free.  It reuses the public-API model
used by the release API diff tooling: a public callable is a Python function
decorated with ``@flashinfer_api``.  Unlike a release comparison, this is
scoped to one pull request's base and head commits.

By default findings are GitHub Actions warnings so the check is safe to roll
out without blocking contributors.  ``--strict`` makes findings fail the job.
"""

from __future__ import annotations

import argparse
import ast
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class ApiFunction:
    qualified_name: str
    module: str
    path: str
    line: int
    signature: str
    docstring: str


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    line: int
    message: str


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL)


def git_file(rev: str, path: str) -> str | None:
    try:
        return git("show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return None


def decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        return decorator_name(node.func)
    return ""


def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{prefix} {node.name}({ast.unparse(node.args)}){returns}"


def extract_public_apis(path: str, source: str | None) -> dict[str, ApiFunction]:
    if source is None:
        return {}
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        return {}

    module = str(PurePosixPath(path).with_suffix("")).replace("/", ".")
    result: dict[str, ApiFunction] = {}

    def visit(parent: ast.AST, class_prefix: str = "") -> None:
        for child in ast.iter_child_nodes(parent):
            if isinstance(child, ast.ClassDef):
                visit(child, f"{class_prefix}{child.name}.")
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(
                    decorator_name(dec) == "flashinfer_api"
                    for dec in child.decorator_list
                ):
                    name = f"{class_prefix}{child.name}"
                    result[name] = ApiFunction(
                        qualified_name=name,
                        module=module,
                        path=path,
                        line=child.lineno,
                        signature=signature(child),
                        docstring=ast.get_docstring(child, clean=False) or "",
                    )
                visit(child, class_prefix)

    visit(tree)
    return result


def exported_names(source: str | None) -> set[str]:
    if source is None:
        return set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    exports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level > 0:
            exports.update(
                alias.asname or alias.name for alias in node.names if alias.name != "*"
            )
    return exports


def changed_paths(base: str, head: str) -> set[str]:
    return {p for p in git("diff", "--name-only", f"{base}...{head}").splitlines() if p}


def changed_docs_contain(
    base: str, head: str, paths: set[str], api: ApiFunction
) -> bool:
    """Return whether a relevant documentation source changed in this PR."""
    needles = (api.qualified_name, api.qualified_name.rsplit(".", 1)[-1], api.module)
    for path in paths:
        if not (path.startswith("docs/") or path in {"README.md", "CONTRIBUTING.md"}):
            continue
        content = git_file(head, path)
        if content and any(needle in content for needle in needles):
            return True
    return False


def api_is_listed_in_docs(head: str, api: ApiFunction) -> bool:
    symbol = api.qualified_name.rsplit(".", 1)[-1]
    try:
        paths = git("ls-tree", "-r", "--name-only", head, "docs/api").splitlines()
    except subprocess.CalledProcessError:
        return False
    return any(
        symbol in (git_file(head, path) or "")
        for path in paths
        if path.endswith(".rst")
    )


def check(base: str, head: str) -> list[Finding]:
    paths = changed_paths(base, head)
    findings: list[Finding] = []

    for path in sorted(
        p for p in paths if p.startswith("flashinfer/") and p.endswith(".py")
    ):
        old = extract_public_apis(path, git_file(base, path))
        new = extract_public_apis(path, git_file(head, path))

        for name in sorted(set(new) - set(old)):
            api = new[name]
            if not api.docstring:
                findings.append(
                    Finding(
                        "warning",
                        api.path,
                        api.line,
                        f"New public API `{api.module}.{name}` has no docstring.",
                    )
                )
            if not api_is_listed_in_docs(head, api):
                findings.append(
                    Finding(
                        "warning",
                        api.path,
                        api.line,
                        f"New public API `{api.module}.{name}` is not listed in docs/api/*.rst.",
                    )
                )

        for name in sorted(set(old) - set(new)):
            api = old[name]
            findings.append(
                Finding(
                    "warning",
                    path,
                    api.line,
                    f"Public API `{api.module}.{name}` was removed; update deprecation and API documentation.",
                )
            )

        for name in sorted(set(old) & set(new)):
            before, after = old[name], new[name]
            if before.signature == after.signature:
                continue
            docs_changed = before.docstring != after.docstring or changed_docs_contain(
                base, head, paths, after
            )
            if not docs_changed:
                findings.append(
                    Finding(
                        "warning",
                        after.path,
                        after.line,
                        f"Public API `{after.module}.{name}` signature changed without an updated docstring or relevant documentation file. "
                        f"Before: `{before.signature}`; after: `{after.signature}`.",
                    )
                )

    old_exports = exported_names(git_file(base, "flashinfer/__init__.py"))
    new_exports = exported_names(git_file(head, "flashinfer/__init__.py"))
    for name in sorted(old_exports - new_exports):
        findings.append(
            Finding(
                "error",
                "flashinfer/__init__.py",
                1,
                f"Public top-level export `{name}` was removed.",
            )
        )
    return findings


def emit(finding: Finding, github_actions: bool) -> None:
    if github_actions:
        level = "error" if finding.level == "error" else "warning"
        message = finding.message.replace("\n", " ").replace("%", "%25")
        print(f"::{level} file={finding.path},line={finding.line}::{message}")
    print(f"[{finding.level.upper()}] {finding.path}:{finding.line} {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Base commit SHA")
    parser.add_argument("--head", required=True, help="Head commit SHA")
    parser.add_argument(
        "--github-actions", action="store_true", help="Emit GitHub workflow annotations"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Return non-zero when findings exist"
    )
    args = parser.parse_args()

    findings = check(args.base, args.head)
    print(f"Public API documentation check: {len(findings)} finding(s)")
    for finding in findings:
        emit(finding, args.github_actions)
    if not findings:
        print("No public API/documentation drift introduced by this PR.")
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
