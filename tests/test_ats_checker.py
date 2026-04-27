"""ATS checker test suite — RED in Wave 1, GREEN after Wave 2 implementation."""
from __future__ import annotations

import dataclasses
import importlib
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pytest
from typer.testing import CliRunner

from larpmyresume.cli import app
from larpmyresume.extractor import Bullet, ParsedResume

# ---------------------------------------------------------------------------
# xfail guard — mirrors test_extractor.py pattern
# ---------------------------------------------------------------------------

try:
    _ats_available = importlib.util.find_spec("larpmyresume.analyzers.ats_checker") is not None
except ModuleNotFoundError:
    _ats_available = False

_WAVE2_XFAIL = pytest.mark.xfail(
    not _ats_available,
    reason="larpmyresume.analyzers.ats_checker not yet implemented (Wave 2)",
    strict=False,
)

if _ats_available:
    from larpmyresume.analyzers.ats_checker import ATSFlag, ATSResult, check
else:
    ATSFlag = None       # type: ignore[assignment,misc]
    ATSResult = None     # type: ignore[assignment,misc]
    check = None         # type: ignore[assignment,misc]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

runner = CliRunner()


def _make_parsed(
    sections: dict[str, list[str]] | None = None,
    is_multi_column: bool = False,
    chars: list[dict] | None = None,
    raw_text: str = "sample text",
) -> ParsedResume:
    return ParsedResume(
        raw_text=raw_text,
        sections=sections if sections is not None else {},
        bullets=[],
        chars=chars if chars is not None else [{"text": "x"}],
        meta={"is_multi_column": is_multi_column, "page_count": 1},
        source_path="",
    )


# ---------------------------------------------------------------------------
# ATS-dataclass contracts
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_ats_dataclasses_importable():
    """ATSFlag and ATSResult are importable with exact field names."""
    assert ATSFlag is not None
    assert ATSResult is not None
    assert check is not None
    f = ATSFlag(flag="test", severity="Medium", explanation="test explanation")
    assert f.flag == "test"
    assert f.severity == "Medium"
    assert f.explanation == "test explanation"
    r = ATSResult(flags=[f], section_score=50)
    assert isinstance(r.flags, list)
    assert isinstance(r.section_score, int)


# ---------------------------------------------------------------------------
# ATS-01: non-standard heading detection
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_non_standard_heading_flagged():
    """ATS-01: non-standard headings produce Medium severity flags."""
    parsed = _make_parsed(sections={"Achievements": [], "Hobbies": []})
    result = check(parsed)
    medium_flags = [f for f in result.flags if f.severity == "Medium"]
    assert len(medium_flags) >= 1
    flag_texts = " ".join(f.flag for f in medium_flags)
    assert "Achievements" in flag_texts or "Hobbies" in flag_texts


@_WAVE2_XFAIL
def test_standard_headings_not_flagged():
    """ATS-01 negative: standard headings produce no Medium non-standard-heading flags."""
    parsed = _make_parsed(
        sections={"Experience": [], "Education": [], "Skills": [], "Projects": []}
    )
    result = check(parsed)
    standard = {"experience", "education", "skills", "projects"}
    for f in result.flags:
        if f.severity == "Medium":
            assert not any(s in f.flag.lower() for s in standard), (
                f"Standard heading flagged as non-standard: {f.flag}"
            )


# ---------------------------------------------------------------------------
# ATS-02: multi-column detection
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_multi_column_flagged():
    """ATS-02: multi-column layout produces a High severity flag."""
    parsed = _make_parsed(is_multi_column=True)
    result = check(parsed)
    high_flags = [f for f in result.flags if f.severity == "High"]
    assert len(high_flags) >= 1
    explanations = " ".join(f.explanation.lower() for f in high_flags)
    assert "column" in explanations or "multi" in explanations


@_WAVE2_XFAIL
def test_multi_column_not_flagged_on_single_column():
    """ATS-02 negative: single-column PDF produces no multi-column flag."""
    parsed = _make_parsed(is_multi_column=False)
    result = check(parsed)
    for f in result.flags:
        assert "column" not in f.flag.lower(), (
            f"Single-column PDF should not have column flag: {f.flag}"
        )


# ---------------------------------------------------------------------------
# ATS-04: section scoring
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_section_score_all_four_sections():
    """ATS-04: all four standard sections → score == 100."""
    parsed = _make_parsed(
        sections={"Experience": [], "Education": [], "Skills": [], "Projects": []}
    )
    result = check(parsed)
    assert result.section_score == 100


@_WAVE2_XFAIL
def test_section_score_three_sections():
    """ATS-04: three of four standard sections → score == 75."""
    parsed = _make_parsed(
        sections={"Experience": [], "Education": [], "Skills": []}
    )
    result = check(parsed)
    assert result.section_score == 75


@_WAVE2_XFAIL
def test_section_score_zero_sections():
    """ATS-04: no standard sections → score == 0."""
    parsed = _make_parsed(sections={})
    result = check(parsed)
    assert result.section_score == 0


# ---------------------------------------------------------------------------
# ATS-05: JSON flag list format
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_ats_flags_list_format():
    """ATS-05: flags list items have flag, severity, explanation keys with valid values."""
    parsed = _make_parsed(
        sections={"NonStandard": []},
        is_multi_column=True,
    )
    result = check(parsed)
    result_dict = dataclasses.asdict(result)
    assert isinstance(result_dict["flags"], list)
    for item in result_dict["flags"]:
        assert "flag" in item
        assert "severity" in item
        assert "explanation" in item
        assert item["severity"] in {"High", "Medium", "Low"}


# ---------------------------------------------------------------------------
# Integration: CLI --json and terminal report
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_scan_json_ats_flags_non_null(real_resume_pdf):
    """ATS-05 integration: --json scan output has ats_flags as non-null list."""
    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Unexpected exit {result.exit_code}: {result.output}"
    import json
    data = json.loads(result.stdout)
    assert data["ats_flags"] is not None, "ats_flags must be non-null after Phase 3"
    assert isinstance(data["ats_flags"], list)
    for item in data["ats_flags"]:
        assert "flag" in item
        assert "severity" in item
        assert "explanation" in item


@_WAVE2_XFAIL
def test_scan_terminal_shows_ats_section(real_resume_pdf):
    """CLI-05 integration: terminal scan output contains ATS section."""
    result = runner.invoke(app, ["scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Unexpected exit {result.exit_code}: {result.output}"
    assert "ATS" in result.output, (
        "Terminal report must contain an ATS section — "
        f"got: {result.output[:300]}"
    )
    assert "not yet implemented" not in result.output.lower(), (
        "Phase 2 placeholder must be replaced by Phase 3 ATS report"
    )
