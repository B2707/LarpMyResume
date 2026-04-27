"""Keyword matcher test suite — RED in Wave 1, GREEN after Wave 2 implementation.

Covers: KW-01 through KW-08, CLI-02, TEST-04
"""
from __future__ import annotations

import importlib
import importlib.util
import json

import httpx
import pytest
from typer.testing import CliRunner

from larpmyresume.cli import app
from larpmyresume.extractor import Bullet, ParsedResume

# ---------------------------------------------------------------------------
# xfail guards — mirrors test_bullet_scorer.py pattern exactly
# ---------------------------------------------------------------------------

try:
    _kw_available = (
        importlib.util.find_spec("larpmyresume.analyzers.keyword_matcher") is not None
    )
except ModuleNotFoundError:
    _kw_available = False

try:
    _scraper_available = (
        importlib.util.find_spec("larpmyresume.scraper") is not None
    )
except ModuleNotFoundError:
    _scraper_available = False

try:
    _gazetteer_available = (
        importlib.util.find_spec("larpmyresume.analyzers.skills_gazetteer") is not None
    )
except ModuleNotFoundError:
    _gazetteer_available = False

_KW_XFAIL = pytest.mark.xfail(
    not _kw_available,
    reason="larpmyresume.analyzers.keyword_matcher not yet implemented (Wave 2)",
    strict=False,
)

_SCRAPER_XFAIL = pytest.mark.xfail(
    not _scraper_available,
    reason="larpmyresume.scraper not yet implemented (Wave 2)",
    strict=False,
)

if _kw_available:
    from larpmyresume.analyzers.keyword_matcher import (  # type: ignore[import]
        KeywordMatchResult,
        SkillMatch,
        check,
    )
else:
    KeywordMatchResult = None   # type: ignore[assignment,misc]
    SkillMatch = None           # type: ignore[assignment,misc]
    check = None                # type: ignore[assignment,misc]

if _scraper_available:
    from larpmyresume.scraper import (  # type: ignore[import]
        JSRenderedError,
        LinkedInBlockedError,
        ScraperHTTPError,
        fetch_jd_text,
    )
else:
    fetch_jd_text = None        # type: ignore[assignment,misc]
    LinkedInBlockedError = None  # type: ignore[assignment,misc]
    JSRenderedError = None      # type: ignore[assignment,misc]
    ScraperHTTPError = None     # type: ignore[assignment,misc]

if _gazetteer_available:
    from larpmyresume.analyzers.skills_gazetteer import (  # type: ignore[import]
        DISAMBIGUATION_BLOCKLIST,
        GAZETTEER,
        SKILL_PARENTS,
    )
else:
    GAZETTEER = None            # type: ignore[assignment,misc]
    SKILL_PARENTS = None        # type: ignore[assignment,misc]
    DISAMBIGUATION_BLOCKLIST = None  # type: ignore[assignment,misc]

# ---------------------------------------------------------------------------
# HTML fixture constants — ≥200 chars with realistic job description content
# ---------------------------------------------------------------------------

GREENHOUSE_HTML = """\
<!DOCTYPE html>
<html>
  <head><title>Software Engineer - Acme Corp</title></head>
  <body>
    <div id="app_body">
      <h2>About the Role</h2>
      <p>We are looking for a skilled Software Engineer to join our backend team.
      You will be working primarily with Python and Docker to build scalable
      microservices and REST APIs. Experience with PostgreSQL and Redis is required.
      Familiarity with React for frontend integration is a nice to have. Must have
      experience with AWS, Kubernetes, and Terraform for infrastructure work.
      We use GitHub Actions for CI/CD and expect strong Git skills. The ideal
      candidate has experience with FastAPI or Django frameworks and knows how to
      write clean, testable code with pytest. Docker and Linux are must-haves.</p>
    </div>
  </body>
</html>
"""

LEVER_HTML = """\
<!DOCTYPE html>
<html>
  <head><title>Backend Engineer - StartupXYZ</title></head>
  <body>
    <div class="section-wrapper">
      <div data-qa="job-description">
        <h2>What You Will Do</h2>
        <p>Join our growing engineering team and help build the next generation of
        our platform. You will work with TypeScript and Node.js on the backend, with
        Kubernetes for deployment orchestration. Experience with PostgreSQL and MongoDB
        is required. Knowledge of GraphQL and REST API design is essential. We use
        GitHub Actions for CI/CD pipelines. Experience with Redis caching and Kafka
        event streaming is preferred. Terraform for infrastructure-as-code is a plus.
        Linux systems administration experience is mandatory. Docker containerization
        is required for all services.</p>
      </div>
    </div>
  </body>
</html>
"""

SHORT_HTML = "<html><body>too short</body></html>"

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


class _URLMatchingTransport(httpx.BaseTransport):
    """Routes requests by URL substring match. Returns 404 for unmatched URLs."""

    def __init__(self, responses: dict[str, httpx.Response]) -> None:
        self._responses = responses

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        for pattern, response in self._responses.items():
            if pattern in url:
                return response
        return httpx.Response(404, text="Not Found")


def make_transport(responses: dict[str, httpx.Response]) -> httpx.BaseTransport:
    """Build a mock transport that routes by URL substring."""
    return _URLMatchingTransport(responses)


def minimal_parsed(
    skills: str = "Python, PostgreSQL, Docker",
    sections: dict[str, list[str]] | None = None,
    raw_text: str | None = None,
) -> ParsedResume:
    """Build a minimal ParsedResume for unit tests.

    Args:
        skills: Comma-separated skills string placed in the 'skills' section.
        sections: Override the default sections dict entirely.
        raw_text: Override the auto-derived raw_text.
    """
    if sections is None:
        sections = {"skills": [skills]}
    derived_raw = raw_text if raw_text is not None else " ".join(
        line for lines in sections.values() for line in lines
    )
    bullets = [
        Bullet(text=line, section=sec, line_num=i)
        for sec, lines in sections.items()
        for i, line in enumerate(lines)
        if line.strip()
    ]
    return ParsedResume(
        raw_text=derived_raw,
        sections=sections,
        bullets=bullets,
        chars=[{"text": "x"}],
        meta={"is_multi_column": False, "page_count": 1},
        source_path="",
    )


runner = CliRunner()

# ---------------------------------------------------------------------------
# SECTION 3: Gazetteer integrity tests (KW-01)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_gazetteer_loads() -> None:
    """GAZETTEER has at least 60 entries (KW-01)."""
    assert GAZETTEER is not None
    assert len(GAZETTEER) >= 60


@_KW_XFAIL
def test_skill_parents_children_in_gazetteer() -> None:
    """Every child and parent in SKILL_PARENTS is a key in GAZETTEER (KW-01)."""
    assert SKILL_PARENTS is not None
    assert GAZETTEER is not None
    for child, parent in SKILL_PARENTS.items():
        assert child in GAZETTEER, f"Child skill {child!r} not found in GAZETTEER"
        assert parent in GAZETTEER, f"Parent skill {parent!r} not found in GAZETTEER"


@_KW_XFAIL
def test_disambiguation_blocklist_entries_in_gazetteer() -> None:
    """All DISAMBIGUATION_BLOCKLIST entries exist as keys in GAZETTEER (KW-01, KW-07)."""
    assert DISAMBIGUATION_BLOCKLIST is not None
    assert GAZETTEER is not None
    for term in DISAMBIGUATION_BLOCKLIST:
        assert term in GAZETTEER, f"Blocklist term {term!r} not found in GAZETTEER"


@_KW_XFAIL
def test_gazetteer_canonical_has_alias() -> None:
    """Each GAZETTEER entry has at least one alias, and canonical appears as alias or substring (KW-01)."""
    assert GAZETTEER is not None
    for canonical, aliases in GAZETTEER.items():
        assert len(aliases) >= 1, f"GAZETTEER[{canonical!r}] has no aliases"
        # The canonical name should appear in its own alias list or as a substring
        has_self_reference = canonical in aliases or any(canonical in a for a in aliases)
        assert has_self_reference, (
            f"GAZETTEER[{canonical!r}] has no self-referencing alias: {aliases}"
        )


# ---------------------------------------------------------------------------
# SECTION 4: HIT / WEAK / MISS classification tests (KW-04, KW-05, KW-06)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_hit_exact_match() -> None:
    """Exact match in JD -> skill appears in result.hits (KW-04)."""
    parsed = minimal_parsed(skills="Python")
    jd_text = "We need Python. Python is required."
    result = check(parsed, jd_text)
    assert any(m.skill.lower() == "python" for m in result.hits), (
        f"Expected 'python' in hits; got hits={[m.skill for m in result.hits]}"
    )


@_KW_XFAIL
def test_hit_via_alias() -> None:
    """Alias in resume matches canonical in JD -> appears in result.hits (KW-04)."""
    parsed = minimal_parsed(skills="postgres")
    jd_text = "postgresql required"
    result = check(parsed, jd_text)
    hit_skills = [m.skill.lower() for m in result.hits]
    assert any(s in ("postgresql", "postgres") for s in hit_skills), (
        f"Expected postgres/postgresql in hits; got {hit_skills}"
    )


@_KW_XFAIL
def test_weak_child_satisfies_parent() -> None:
    """Child skill in resume weakly satisfies parent skill in JD -> appears in weak (KW-06)."""
    parsed = minimal_parsed(skills="postgresql")
    jd_text = "SQL experience required"
    result = check(parsed, jd_text)
    weak_skills = [m.skill.lower() for m in result.weak]
    assert any(s == "sql" for s in weak_skills), (
        f"Expected 'sql' in weak; got weak={weak_skills}"
    )


@_KW_XFAIL
def test_weak_is_one_directional() -> None:
    """JD child does NOT satisfy resume parent — React missing if only JavaScript present (KW-06)."""
    parsed = minimal_parsed(skills="javascript")
    jd_text = "React required"
    result = check(parsed, jd_text)
    hit_skills = [m.skill.lower() for m in result.hits]
    weak_skills = [m.skill.lower() for m in result.weak]
    missing_skills = [m.skill.lower() for m in result.missing]
    assert "react" not in hit_skills, "React must not appear as a hit when only JS present"
    assert "react" not in weak_skills, "React must not appear as weak when only JS present"
    assert "react" in missing_skills, (
        f"Expected 'react' in missing; got {missing_skills}"
    )


@_KW_XFAIL
def test_miss_not_found() -> None:
    """Skill required in JD but absent from resume -> appears in result.missing (KW-05)."""
    parsed = minimal_parsed(skills="Python")
    jd_text = "Kubernetes required"
    result = check(parsed, jd_text)
    missing_skills = [m.skill.lower() for m in result.missing]
    assert "kubernetes" in missing_skills, (
        f"Expected 'kubernetes' in missing; got {missing_skills}"
    )


@_KW_XFAIL
def test_miss_found_in_is_empty_string() -> None:
    """Missing skill must have found_in='' (not in any section) (KW-04)."""
    parsed = minimal_parsed(skills="Python")
    jd_text = "Kubernetes required"
    result = check(parsed, jd_text)
    miss = next((m for m in result.missing if m.skill.lower() == "kubernetes"), None)
    assert miss is not None, "Expected 'kubernetes' in missing"
    assert miss.found_in == "", (
        f"Missing skill found_in must be empty string; got {miss.found_in!r}"
    )


@_KW_XFAIL
def test_hit_found_in_is_section_name() -> None:
    """HIT skill's found_in is the section name (lowercase, no colon) (KW-04)."""
    parsed = minimal_parsed(skills="Python, Docker", sections={"skills": ["Python, Docker"]})
    result = check(parsed, "Python required.")
    hit = next((m for m in result.hits if m.skill.lower() == "python"), None)
    assert hit is not None, "Expected 'python' in hits"
    assert hit.found_in == "skills", (
        f"Expected found_in='skills'; got {hit.found_in!r}"
    )


# ---------------------------------------------------------------------------
# SECTION 5: Importance classification tests (KW-03)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_importance_required() -> None:
    """Skill with 'required'/'must' signal in JD -> importance='required' (KW-03)."""
    parsed = minimal_parsed(skills="Python Docker")
    jd_text = "Python is required. Must have Docker."
    result = check(parsed, jd_text)
    python_hit = next(
        (m for m in result.hits if m.skill.lower() == "python"), None
    )
    assert python_hit is not None, "Expected python in hits"
    assert python_hit.importance == "required", (
        f"Expected importance='required'; got {python_hit.importance!r}"
    )


@_KW_XFAIL
def test_importance_preferred() -> None:
    """Skill with 'nice to have'/'preferred' signal -> importance='preferred' (KW-03)."""
    parsed = minimal_parsed(skills="Python")
    jd_text = "React is nice to have. Preferred: Vue."
    result = check(parsed, jd_text)
    preferred_misses = [
        m for m in result.missing if m.skill.lower() in ("react", "vue")
    ]
    assert len(preferred_misses) >= 1, "Expected react or vue in missing"
    for m in preferred_misses:
        assert m.importance == "preferred", (
            f"Expected importance='preferred' for {m.skill!r}; got {m.importance!r}"
        )


@_KW_XFAIL
def test_importance_negated_not_required() -> None:
    """'Not required' negation -> skill treated as preferred, not required (KW-03)."""
    parsed = minimal_parsed(skills="")
    jd_text = "Docker is preferred but not required."
    result = check(parsed, jd_text)
    docker_entry = next(
        (m for m in result.missing if m.skill.lower() == "docker"), None
    )
    if docker_entry is not None:
        assert docker_entry.importance == "preferred", (
            f"Negated required signal should yield preferred; got {docker_entry.importance!r}"
        )


@_KW_XFAIL
def test_importance_default_required() -> None:
    """Skill with no importance signal defaults to 'required' (KW-03)."""
    parsed = minimal_parsed(skills="")
    jd_text = "Experience with Terraform."
    result = check(parsed, jd_text)
    tf_entry = next(
        (m for m in result.missing if m.skill.lower() == "terraform"), None
    )
    if tf_entry is not None:
        assert tf_entry.importance == "required", (
            f"No-signal importance must default to 'required'; got {tf_entry.importance!r}"
        )


# ---------------------------------------------------------------------------
# SECTION 6: Disambiguation tests (KW-07)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_go_does_not_match_english_go() -> None:
    """'go' and 'C' as English verbs/pronouns must not be classified as skills (KW-07)."""
    jd_text = "You will go to the office daily. C suite preferred."
    parsed = minimal_parsed(skills="Python")
    result = check(parsed, jd_text)
    all_skills = [m.skill.lower() for m in result.hits + result.weak + result.missing]
    assert "go" not in all_skills, (
        f"'go' (English verb) must not appear as a skill; got all_skills={all_skills}"
    )
    assert "c" not in all_skills, (
        f"'c' (English letter) must not appear as a skill; got all_skills={all_skills}"
    )


@_KW_XFAIL
def test_go_matches_golang_alias() -> None:
    """'golang' in JD -> Go skill is detected (KW-07)."""
    jd_text = "Expert in golang required."
    parsed = minimal_parsed(skills="")
    result = check(parsed, jd_text)
    missing_skills = [m.skill.lower() for m in result.missing]
    assert any(s in ("go", "golang") for s in missing_skills), (
        f"Expected 'go'/'golang' in missing when JD says 'golang'; got {missing_skills}"
    )


@_KW_XFAIL
def test_go_matches_comma_list() -> None:
    """'Go' in a comma-separated skills list in JD -> Go skill detected (KW-07)."""
    jd_text = "Skills: Go, Python, JavaScript"
    parsed = minimal_parsed(skills="")
    result = check(parsed, jd_text)
    missing_skills = [m.skill.lower() for m in result.missing]
    assert any(s in ("go", "golang") for s in missing_skills), (
        f"Expected 'go'/'golang' in missing from comma list; got {missing_skills}"
    )


@_KW_XFAIL
def test_rust_does_not_match_rusty_english() -> None:
    """'rusty' in English prose must not trigger Rust skill detection (KW-07)."""
    jd_text = "Our legacy code is rusty and needs refactoring."
    parsed = minimal_parsed(skills="Python")
    result = check(parsed, jd_text)
    all_skills = [m.skill.lower() for m in result.hits + result.weak + result.missing]
    assert "rust" not in all_skills, (
        f"'rusty' must not match Rust skill; got all_skills={all_skills}"
    )


# ---------------------------------------------------------------------------
# SECTION 7: KeywordMatchResult structure tests (KW-08)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_result_has_three_lists() -> None:
    """KeywordMatchResult has hits, weak, missing as lists (KW-08)."""
    result = check(minimal_parsed(skills="Python"), "Python required. Kubernetes required.")
    assert hasattr(result, "hits"), "result must have 'hits' attribute"
    assert hasattr(result, "weak"), "result must have 'weak' attribute"
    assert hasattr(result, "missing"), "result must have 'missing' attribute"
    assert isinstance(result.hits, list), "result.hits must be a list"
    assert isinstance(result.weak, list), "result.weak must be a list"
    assert isinstance(result.missing, list), "result.missing must be a list"


@_KW_XFAIL
def test_skill_match_fields() -> None:
    """SkillMatch has skill, importance, found_in fields with correct types (KW-08)."""
    result = check(minimal_parsed(skills="Python"), "Python required.")
    assert len(result.hits) >= 1, "Expected at least one hit for Python"
    m = result.hits[0]
    assert hasattr(m, "skill"), "SkillMatch must have 'skill' field"
    assert hasattr(m, "importance"), "SkillMatch must have 'importance' field"
    assert hasattr(m, "found_in"), "SkillMatch must have 'found_in' field"
    assert m.importance in ("required", "preferred"), (
        f"importance must be 'required' or 'preferred'; got {m.importance!r}"
    )
    assert isinstance(m.skill, str), "skill must be str"
    assert isinstance(m.found_in, str), "found_in must be str"


# ---------------------------------------------------------------------------
# SECTION 8: HTTP scraper tests (KW-02)
# ---------------------------------------------------------------------------


@_SCRAPER_XFAIL
def test_greenhouse_scrape() -> None:
    """Greenhouse URL returns extracted text ≥200 chars with expected content (KW-02)."""
    transport = make_transport({
        "greenhouse.io": httpx.Response(200, text=GREENHOUSE_HTML),
    })
    text = fetch_jd_text("https://boards.greenhouse.io/co/jobs/1", transport=transport)
    assert len(text) >= 200, f"Extracted text too short: {len(text)} chars"
    assert "python" in text.lower(), "Expected 'python' in extracted greenhouse JD text"


@_SCRAPER_XFAIL
def test_lever_scrape() -> None:
    """Lever URL returns extracted text ≥200 chars (KW-02)."""
    transport = make_transport({
        "lever.co": httpx.Response(200, text=LEVER_HTML),
    })
    text = fetch_jd_text("https://jobs.lever.co/co/abc123", transport=transport)
    assert len(text) >= 200, f"Extracted text too short: {len(text)} chars"


@_SCRAPER_XFAIL
def test_linkedin_raises() -> None:
    """LinkedIn URL raises LinkedInBlockedError without making HTTP call (KW-02)."""
    assert LinkedInBlockedError is not None
    with pytest.raises(LinkedInBlockedError):
        fetch_jd_text("https://www.linkedin.com/jobs/view/123456")


@_SCRAPER_XFAIL
def test_js_rendered_raises() -> None:
    """Short content (<SHORT_CONTENT_THRESHOLD chars) raises JSRenderedError (KW-02)."""
    assert JSRenderedError is not None
    short_transport = httpx.MockTransport(lambda req: httpx.Response(200, text=SHORT_HTML))
    with pytest.raises(JSRenderedError):
        fetch_jd_text("https://example.com/job", transport=short_transport)


@_SCRAPER_XFAIL
def test_timeout_raises() -> None:
    """Timeout during fetch raises httpx.TimeoutException (KW-02)."""
    def timeout_handler(req: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("Simulated timeout", request=req)

    transport = httpx.MockTransport(timeout_handler)
    with pytest.raises(httpx.TimeoutException):
        fetch_jd_text("https://example.com/job", transport=transport)


@_SCRAPER_XFAIL
def test_http_403_raises() -> None:
    """HTTP 403 response raises ScraperHTTPError (KW-02)."""
    assert ScraperHTTPError is not None
    transport = httpx.MockTransport(lambda req: httpx.Response(403, text="Forbidden"))
    with pytest.raises(ScraperHTTPError):
        fetch_jd_text("https://example.com/job", transport=transport)


# ---------------------------------------------------------------------------
# SECTION 8 (CLI): match --job-text bypasses HTTP (CLI-02)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_job_text_bypasses_http() -> None:
    """match command with --job-text succeeds without any HTTP call (CLI-02)."""
    result = runner.invoke(app, [
        "match", "tests/fixtures/real_resume.pdf",
        "--job-text", "Python required. Docker preferred.",
    ])
    assert result.exit_code == 0, (
        f"Expected exit_code=0; got {result.exit_code}. Output: {result.output}"
    )


# ---------------------------------------------------------------------------
# SECTION 9: JSON schema shape test (CLI-02, KW-08)
# ---------------------------------------------------------------------------


@_KW_XFAIL
def test_match_json_schema() -> None:
    """match --json output has keyword_match key with hits/weak/missing lists (KW-08, CLI-02)."""
    result = runner.invoke(app, [
        "--json", "match", "tests/fixtures/real_resume.pdf",
        "--job-text", "Python required. Kubernetes preferred.",
    ])
    assert result.exit_code == 0, (
        f"Expected exit_code=0; got {result.exit_code}. Output: {result.output}"
    )
    data = json.loads(result.output)
    assert "keyword_match" in data, f"'keyword_match' key missing from JSON output"
    assert data["keyword_match"] is not None, "'keyword_match' must be non-null"
    kw = data["keyword_match"]
    assert "hits" in kw, "'hits' key missing from keyword_match"
    assert "weak" in kw, "'weak' key missing from keyword_match"
    assert "missing" in kw, "'missing' key missing from keyword_match"
    for tier in ("hits", "weak", "missing"):
        assert isinstance(kw[tier], list), f"keyword_match['{tier}'] must be a list"
        for item in kw[tier]:
            assert "skill" in item, f"Item in {tier!r} missing 'skill' key: {item}"
            assert "importance" in item, f"Item in {tier!r} missing 'importance' key: {item}"
            assert "found_in" in item, f"Item in {tier!r} missing 'found_in' key: {item}"
            assert item["importance"] in ("required", "preferred"), (
                f"importance must be 'required' or 'preferred'; got {item['importance']!r}"
            )
