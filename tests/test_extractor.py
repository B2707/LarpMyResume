from __future__ import annotations

import importlib
import os
from pathlib import Path
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Wave 1 scaffold: extractor.py not yet implemented.
# We conditionally import so the module collects. All tests are marked xfail
# until Wave 2 ships the implementation.
# ---------------------------------------------------------------------------

_extractor_available = importlib.util.find_spec("larpmyresume.extractor") is not None

_WAVE2_XFAIL = pytest.mark.xfail(
    not _extractor_available,
    reason="larpmyresume.extractor not yet implemented (Wave 2)",
    strict=False,
)

if _extractor_available:
    from larpmyresume.extractor import (
        Bullet,
        EmptyPDFError,
        ImageOnlyPDFError,
        ParsedResume,
        _extract_sections_and_bullets,
        extract,
    )
else:
    # Stub names so the module parses without NameError at collection time
    Bullet = None  # type: ignore[assignment,misc]
    EmptyPDFError = Exception  # type: ignore[assignment,misc]
    ImageOnlyPDFError = Exception  # type: ignore[assignment,misc]
    ParsedResume = None  # type: ignore[assignment,misc]
    extract = None  # type: ignore[assignment,misc]
    _extract_sections_and_bullets = None  # type: ignore[assignment,misc]


# ---------------------------------------------------------------------------
# EXTRACT-01: extract() returns a populated ParsedResume
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_extract_real_resume(real_resume_pdf):
    """EXTRACT-01: extract() returns ParsedResume with populated fields from real PDF."""
    result = extract(real_resume_pdf)
    assert isinstance(result, ParsedResume)
    assert len(result.raw_text) > 100
    assert len(result.sections) >= 1
    assert len(result.bullets) >= 1
    assert isinstance(result.chars, list)
    assert result.meta["page_count"] >= 1


# ---------------------------------------------------------------------------
# EXTRACT-02: image-only PDF raises ImageOnlyPDFError
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_image_only_raises(image_only_pdf):
    """EXTRACT-02: extract() raises ImageOnlyPDFError on image-only PDF."""
    with pytest.raises(ImageOnlyPDFError):
        extract(image_only_pdf)


# ---------------------------------------------------------------------------
# EXTRACT-03: ligature normalization — raw_text contains ASCII, not FB-block
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_ligature_normalization(real_resume_pdf):
    """EXTRACT-03: raw_text contains no U+FB00–U+FB06 ligature codepoints."""
    result = extract(real_resume_pdf)
    ligature_codepoints = set(range(0xFB00, 0xFB07))
    for char in result.raw_text:
        assert ord(char) not in ligature_codepoints, (
            f"Ligature codepoint U+{ord(char):04X} found in raw_text after normalization"
        )


# ---------------------------------------------------------------------------
# EXTRACT-04: multi-column detection
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_multicolumn_detected(two_column_pdf):
    """EXTRACT-04: two_column.pdf sets meta['is_multi_column'] = True."""
    result = extract(two_column_pdf)
    assert result.meta["is_multi_column"] is True


@_WAVE2_XFAIL
def test_single_column_not_flagged(real_resume_pdf):
    """EXTRACT-04: real_resume.pdf does NOT set meta['is_multi_column'] = True."""
    result = extract(real_resume_pdf)
    assert result.meta["is_multi_column"] is False


# ---------------------------------------------------------------------------
# EXTRACT-05: section segmentation
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_sections_extracted(real_resume_pdf):
    """EXTRACT-05: sections dict is non-empty with at least one known heading."""
    result = extract(real_resume_pdf)
    assert len(result.sections) >= 1
    # At least one key must be a non-empty string
    for heading in result.sections:
        assert isinstance(heading, str)
        assert len(heading) > 0


# ---------------------------------------------------------------------------
# EXTRACT-06: bullet extraction and continuation merging
# ---------------------------------------------------------------------------

@_WAVE2_XFAIL
def test_bullets_extracted(real_resume_pdf):
    """EXTRACT-06: bullets list is non-empty; each bullet has text and section."""
    result = extract(real_resume_pdf)
    assert len(result.bullets) >= 1
    for b in result.bullets:
        assert isinstance(b, Bullet)
        assert len(b.text) > 0
        assert isinstance(b.section, str)
        assert isinstance(b.line_num, int)


@_WAVE2_XFAIL
def test_bullet_continuation_merge():
    """EXTRACT-06: continuation lines are merged into the preceding Bullet.text."""
    text = "EXPERIENCE\n- Built REST API with Python\n  serving 10k daily users\n"
    _, bullets = _extract_sections_and_bullets(text)
    assert len(bullets) == 1
    assert "serving 10k daily users" in bullets[0].text


@_WAVE2_XFAIL
def test_file_size_limit_enforced(tmp_path):
    """Security: extract() raises ValueError if file exceeds 50MB size limit."""
    # This test validates the guard exists and fires before pdfplumber.open()
    fake_pdf = tmp_path / "huge.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4")  # minimal PDF header

    with patch("os.path.getsize", return_value=51 * 1024 * 1024):
        with pytest.raises(ValueError, match="50"):
            extract(fake_pdf)
