"""Check registry + unified Finding model for flashinfer_document_check.

This module is the single source of truth for the eight check axes (nine
fail counters — 2.1 splits into MISSING + STALE). Adding a new check is a
matter of:

  1. Append a ``CheckMeta(...)`` entry to ``CHECKS`` below
  2. Emit ``Finding`` instances with ``check=<slug>`` from your checker
  3. Wire up the JSON output (the renderer picks it up automatically)

That's it — generate_doc_check_report.py iterates over ``CHECKS`` to build its
summary table, per-section headers, and HTML cards; no other file needs to
change.

The ``Finding`` schema is intentionally a union: cross-source checks
populate ``location`` (e.g. "CLAUDE.md"); per-symbol checks populate
``module``/``symbol``/``file``/``line``. Empty fields are simply not
rendered. ``schema_version`` lets us migrate without breaking renderers.
"""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION: int = 1


# ---------------------------------------------------------------------------
# Unified Finding model
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single failure record across any check.

    ``check`` is the slug from a ``CheckMeta`` entry. ``message`` is a free
    text description. The other fields are all optional — populate whichever
    apply for your check.
    """

    check: str
    message: str
    location: str = ""  # e.g. "CLAUDE.md" or "docs/index.rst:42"
    module: str = ""  # e.g. "flashinfer.fused_moe"
    symbol: str = ""  # e.g. "trtllm_fused_moe"
    file: str = ""  # e.g. "flashinfer/fused_moe/__init__.py"
    line: int = 0  # 1-based line number; 0 means "not applicable"


# ---------------------------------------------------------------------------
# Check identifiers (machine slugs)
# ---------------------------------------------------------------------------

# §2.1 — two slugs because the check produces both MISSING and STALE counts.
MISSING = "missing"
STALE = "stale"

# §2.2 / §2.3 — produced by doc_check_extended.py
DOCSTRING_COMPLETENESS = "docstring_completeness"
ARGS_CONSISTENCY = "args_consistency"

# §2.4 / §2.5 / §2.6 / §2.7 / §2.8 — produced by cross_source_check.py
ENV_VARS_CONSISTENCY = "env_vars_consistency"
SUPPORTED_ARCH = "supported_arch_consistency"
QUICKREF_PATHS = "quickref_paths_exist"
SKILL_REFS = "skill_refs_exist"
DOCS_INDEX_REFS = "docs_index_refs_exist"


# ---------------------------------------------------------------------------
# Per-check metadata
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckMeta:
    """All renderer-facing metadata for one check axis.

    summary_key tells the renderer which key in the source script's JSON
    ``summary`` dict carries this check's fail count. For §2.1 (missing/
    stale) it points into the doc-gap JSON's ``summary`` sub-object instead
    of the top-level ``summary`` table — see report/extract.py for how
    that's resolved.
    """

    slug: str
    section: str  # "1" .. "8" — section number in the rendered
    # HTML report. MISSING + STALE share "1" and
    # are merged into a single chip section.
    title: str  # human-readable section title
    desc: str  # one-sentence description for headers / docstrings
    source_script: str  # which script produces this check
    summary_key: str  # JSON summary key carrying the fail count


CHECKS: tuple[CheckMeta, ...] = (
    # §1 — MISSING and STALE share a single rendered section in the HTML
    # report (per-module chip blocks). Both stay in CHECKS because the
    # renderer reads counts/findings per-slug; the renderer collapses them
    # into one <div class="section"> at output time.
    CheckMeta(
        slug=MISSING,
        section="1",
        title="API ↔ .rst Coverage (MISSING)",
        desc="Decorated with @flashinfer_api in code but absent from any docs/api/*.rst.",
        source_script="flashinfer_doc_test.py",
        summary_key="total_missing",
    ),
    CheckMeta(
        slug=STALE,
        section="1",
        title="API ↔ .rst Coverage (STALE)",
        desc="Listed in docs/api/*.rst but no longer @flashinfer_api in code.",
        source_script="flashinfer_doc_test.py",
        summary_key="total_stale",
    ),
    CheckMeta(
        slug=DOCSTRING_COMPLETENESS,
        section="2",
        title="Docstring Completeness",
        desc="Every @flashinfer_api function must have a docstring with a Parameters/Args section.",
        source_script="doc_check_extended.py",
        summary_key=DOCSTRING_COMPLETENESS,
    ),
    CheckMeta(
        slug=ARGS_CONSISTENCY,
        section="3",
        title="Args Consistency",
        desc="Function signature args must match the docstring Parameters list.",
        source_script="doc_check_extended.py",
        summary_key=ARGS_CONSISTENCY,
    ),
    CheckMeta(
        slug=ENV_VARS_CONSISTENCY,
        section="4",
        title="Env Vars Consistency",
        desc="Every FLASHINFER_* env var read in code should be mentioned in CLAUDE.md.",
        source_script="cross_source_check.py",
        summary_key=ENV_VARS_CONSISTENCY,
    ),
    CheckMeta(
        slug=SUPPORTED_ARCH,
        section="5",
        title="Supported Architecture Consistency",
        desc="CLAUDE.md supported-arch list ↔ is_sm*_supported() ↔ supported_major_versions[].",
        source_script="cross_source_check.py",
        summary_key=SUPPORTED_ARCH,
    ),
    CheckMeta(
        slug=QUICKREF_PATHS,
        section="6",
        title="CLAUDE.md Quick-Ref Paths Exist",
        desc="Every file path referenced in CLAUDE.md code blocks must exist in the repo.",
        source_script="cross_source_check.py",
        summary_key=QUICKREF_PATHS,
    ),
    CheckMeta(
        slug=SKILL_REFS,
        section="7",
        title="Skill MD References Exist",
        desc="Every file path referenced in .claude/skills/**/SKILL.md must exist.",
        source_script="cross_source_check.py",
        summary_key=SKILL_REFS,
    ),
    CheckMeta(
        slug=DOCS_INDEX_REFS,
        section="8",
        title="Docs Index References Exist",
        desc="Every leaf entry in docs/index.rst toctree blocks must resolve to a .rst file.",
        source_script="cross_source_check.py",
        summary_key=DOCS_INDEX_REFS,
    ),
)


def get_check(slug: str) -> CheckMeta:
    """Lookup CheckMeta by slug; raises KeyError if unknown."""
    for c in CHECKS:
        if c.slug == slug:
            return c
    raise KeyError(f"Unknown check slug: {slug!r}")


# Convenience groupings for callers that want to iterate one source script.
def checks_by_source(script: str) -> tuple[CheckMeta, ...]:
    return tuple(c for c in CHECKS if c.source_script == script)


__all__ = (
    "SCHEMA_VERSION",
    "Finding",
    "CheckMeta",
    "CHECKS",
    "MISSING",
    "STALE",
    "DOCSTRING_COMPLETENESS",
    "ARGS_CONSISTENCY",
    "ENV_VARS_CONSISTENCY",
    "SUPPORTED_ARCH",
    "QUICKREF_PATHS",
    "SKILL_REFS",
    "DOCS_INDEX_REFS",
    "get_check",
    "checks_by_source",
)
