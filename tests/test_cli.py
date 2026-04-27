from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from larpmyresume.cli import app  # ImportError until Plan 02 creates cli.py — RED gate

runner = CliRunner()  # stdout/stderr are separate streams via result.stdout / result.stderr


# ---------------------------------------------------------------------------
# CLI-06: --version
# ---------------------------------------------------------------------------

def test_version():
    """CLI-06: --version prints version string and exits 0."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


# ---------------------------------------------------------------------------
# SCHEMA-01/02/03/04, D-01/02/03: JSON schema shape
# ---------------------------------------------------------------------------

def test_scan_json_schema(real_resume_pdf):
    """SCHEMA-01/02/03/04: --json produces valid JSON with all required fields."""
    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Expected exit 0, got {result.exit_code}. Output: {result.output}"
    data = json.loads(result.stdout)  # stdout only — Pitfall 4: never result.output
    # SCHEMA-01
    assert data["schema_version"] == "1.0"
    # SCHEMA-03
    assert "generated_at" in data
    assert data["generated_at"]  # not empty
    # SCHEMA-02
    assert "resume_file" in data
    assert "job_url" in data
    assert "overall_score" in data
    assert "sections" in data
    assert "ats_flags" in data
    assert "bullets" in data
    assert "score_breakdown" in data
    # Phase 6: overall_score and score_breakdown now populated by scan (D-01/D-04)
    assert isinstance(data["overall_score"], int)
    assert 0 <= data["overall_score"] <= 100
    assert isinstance(data["ats_flags"], list)  # Phase 3: populated by ats_checker
    assert isinstance(data["bullets"], list)  # Phase 4: populated by bullet_scorer
    assert isinstance(data["score_breakdown"], dict)
    assert set(data["score_breakdown"].keys()) == {"ats_score", "bullet_score", "keyword_score", "overall_score"}
    assert data["score_breakdown"]["keyword_score"] is None  # scan-only: no JD
    # SCHEMA-04 + D-02: keyword_match is null BUT the KEY must exist
    assert "keyword_match" in data
    assert data["keyword_match"] is None


def test_scan_keyword_match_key_exists(real_resume_pdf):
    """SCHEMA-04: keyword_match key must EXIST (not absent) in scan-only JSON output.

    Separate from test_scan_json_schema to make the requirement explicit — a missing
    key would cause Ruby KeyError in the downstream report generator.
    """
    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    # Key existence check — data.get("keyword_match") would pass even if absent
    assert "keyword_match" in data, (
        "keyword_match key must be present in JSON output even when null "
        "(absent key causes Ruby KeyError in report generator)"
    )


# ---------------------------------------------------------------------------
# CLI-03: stdout purity
# ---------------------------------------------------------------------------

def test_scan_stdout_clean_on_json(real_resume_pdf):
    """CLI-03: --json stdout is pure JSON; no diagnostic contamination."""
    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0
    # If stdout is contaminated by any non-JSON text, json.loads raises — test fails clearly
    json.loads(result.stdout)


# ---------------------------------------------------------------------------
# CLI-04: exit codes
# ---------------------------------------------------------------------------

def test_scan_nonexistent_file_exit_1():
    """CLI-04: nonexistent file path exits with code 1."""
    result = runner.invoke(app, ["scan", "/nonexistent/does_not_exist_99.pdf"])
    assert result.exit_code == 1


def test_scan_image_only_pdf_exit_1(image_only_pdf):
    """CLI-04 + D-08: image-only PDF exits with code 1 (ImageOnlyPDFError caught)."""
    result = runner.invoke(app, ["scan", str(image_only_pdf)])
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# CLI-01: scan terminal mode
# ---------------------------------------------------------------------------

def test_scan_terminal_report_no_crash(real_resume_pdf):
    """CLI-01: scan without --json completes without error; prints placeholder panel (D-09)."""
    result = runner.invoke(app, ["scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Expected exit 0, got {result.exit_code}. Output: {result.output}"


# ---------------------------------------------------------------------------
# CLI-02: match command (fully wired — Phase 5)
# ---------------------------------------------------------------------------

def test_match_no_jd_source_exits_1(real_resume_pdf):
    """CLI-02: match command with neither --job-url nor --job-text exits 1."""
    result = runner.invoke(app, ["match", str(real_resume_pdf)])
    assert result.exit_code == 1, (
        f"Expected exit 1 when no JD source provided; got {result.exit_code}"
    )


def test_match_job_text_exits_0(real_resume_pdf):
    """CLI-02: match command with --job-text (no HTTP) completes exit 0."""
    result = runner.invoke(
        app,
        ["match", str(real_resume_pdf), "--job-text", "Python required. Docker preferred."],
    )
    assert result.exit_code == 0, (
        f"Expected exit 0 with --job-text; got {result.exit_code}. Output: {result.output}"
    )


def test_match_json_output(real_resume_pdf):
    """CLI-02/03/SCHEMA-01: match --json --job-text produces valid JSON with schema_version and keyword_match."""
    result = runner.invoke(
        app,
        ["--json", "match", str(real_resume_pdf), "--job-text", "Python required."],
    )
    assert result.exit_code == 0, (
        f"Expected exit 0; got {result.exit_code}. Output: {result.output}"
    )
    data = json.loads(result.stdout)
    assert data["schema_version"] == "1.0"
    assert "keyword_match" in data
    assert data["keyword_match"] is not None


# ---------------------------------------------------------------------------
# D-12: no_args_is_help
# ---------------------------------------------------------------------------

def test_no_args_shows_help():
    """D-12: invoking with no args shows help text mentioning both subcommands."""
    result = runner.invoke(app, [])
    # Help text should describe available commands
    assert "scan" in result.output
    assert "match" in result.output


# ---------------------------------------------------------------------------
# Phase 6: ats_section_score top-level key
# ---------------------------------------------------------------------------

def test_scan_json_has_ats_section_score(real_resume_pdf):
    """Phase 6: ats_section_score is a top-level int in scan JSON (D-02)."""
    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert "ats_section_score" in data
    assert isinstance(data["ats_section_score"], int)
    assert data["ats_section_score"] in (0, 25, 50, 75, 100)
