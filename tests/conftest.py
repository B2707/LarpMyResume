from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def real_resume_pdf() -> Path:
    p = FIXTURES_DIR / "real_resume.pdf"
    if not p.exists():
        from tests.fixtures.generate_fixtures import make_single_column_pdf
        make_single_column_pdf(p)
    return p


@pytest.fixture(scope="session")
def two_column_pdf() -> Path:
    p = FIXTURES_DIR / "two_column.pdf"
    assert p.exists(), (
        f"Missing fixture: {p}. Run: python tests/fixtures/generate_fixtures.py"
    )
    return p


@pytest.fixture(scope="session")
def image_only_pdf() -> Path:
    p = FIXTURES_DIR / "image_only.pdf"
    assert p.exists(), (
        f"Missing fixture: {p}. Run: python tests/fixtures/generate_fixtures.py"
    )
    return p
