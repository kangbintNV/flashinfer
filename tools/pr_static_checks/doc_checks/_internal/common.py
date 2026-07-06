"""Shared path constants for the flashinfer_document_check tooling.

All four checker scripts (flashinfer_doc_test.py, doc_check_extended.py,
cross_source_check.py, generate_doc_check_report.py) import these instead of
declaring their own copies — change one place to retarget the whole pipeline.

Env overrides (defaults shown in parentheses):
  FLASHINFER_SRC  (${HERE}/flashinfer_src)   — checked-out flashinfer repo
  DOC_CHECK_OUT   (${HERE}/doc_check_results) — JSON / per-check MD output dir
  HTML_OUT_DIR    (${HERE}/html_out)          — rendered HTML output dir

``HERE`` is the directory containing this _common.py (i.e. the repo root for
this tooling project).
"""

from __future__ import annotations

import os
from pathlib import Path

HERE: Path = Path(__file__).resolve().parent.parent

FLASHINFER_ROOT: Path = Path(os.environ.get("FLASHINFER_SRC", HERE / "flashinfer_src"))
FLASHINFER_PKG: Path = FLASHINFER_ROOT / "flashinfer"
DOCS_DIR: Path = FLASHINFER_ROOT / "docs"
DOCS_API_DIR: Path = DOCS_DIR / "api"
CSRC_DIR: Path = FLASHINFER_ROOT / "csrc"
CLAUDE_MD: Path = FLASHINFER_ROOT / "CLAUDE.md"
SKILLS_DIR: Path = FLASHINFER_ROOT / ".claude" / "skills"

OUTPUT_DIR: Path = Path(os.environ.get("DOC_CHECK_OUT", HERE / "doc_check_results"))
HTML_OUT_DIR: Path = Path(os.environ.get("HTML_OUT_DIR", HERE / "html_out"))

__all__ = (
    "HERE",
    "FLASHINFER_ROOT",
    "FLASHINFER_PKG",
    "DOCS_DIR",
    "DOCS_API_DIR",
    "CSRC_DIR",
    "CLAUDE_MD",
    "SKILLS_DIR",
    "OUTPUT_DIR",
    "HTML_OUT_DIR",
)
