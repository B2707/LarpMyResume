"""Bullet scorer test suite — RED in Wave 1, GREEN after Wave 2 implementation."""
from __future__ import annotations

import dataclasses
import importlib
import importlib.util

import pytest
from typer.testing import CliRunner

from larpmyresume.cli import app
from larpmyresume.extractor import Bullet, ParsedResume

# ---------------------------------------------------------------------------
# xfail guard — mirrors test_ats_checker.py pattern
# ---------------------------------------------------------------------------

try:
    _bullet_scorer_available = (
        importlib.util.find_spec("larpmyresume.analyzers.bullet_scorer") is not None
    )
except ModuleNotFoundError:
    _bullet_scorer_available = False

_WAVE2_XFAIL = pytest.mark.xfail(
    not _bullet_scorer_available,
    reason="larpmyresume.analyzers.bullet_scorer not yet implemented (Wave 2)",
    strict=False,
)

if _bullet_scorer_available:
    from larpmyresume.analyzers.bullet_scorer import BulletResult, BulletScorerResult, check
else:
    BulletResult = None       # type: ignore[assignment,misc]
    BulletScorerResult = None  # type: ignore[assignment,misc]
    check = None              # type: ignore[assignment,misc]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

runner = CliRunner()


def _make_bullets(
    items: list[tuple[str, str]] | None = None,
) -> list[Bullet]:
    if items is None:
        return []
    return [
        Bullet(text=text, section=section, line_num=i)
        for i, (text, section) in enumerate(items)
    ]


def _make_parsed_with_bullets(bullets: list[Bullet]) -> ParsedResume:
    return ParsedResume(
        raw_text="",
        sections={},
        bullets=bullets,
        chars=[{"text": "x"}],
        meta={"is_multi_column": False, "page_count": 1},
        source_path="",
    )


# ---------------------------------------------------------------------------
# Group 1 — Dataclass contract (BULLET-05, BULLET-07)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_bullet_result_dataclass():
    """BulletResult and BulletScorerResult importable with exact field names."""
    assert BulletResult is not None
    assert BulletScorerResult is not None
    assert check is not None

    br = BulletResult(
        score=100,
        text="Built authentication service using JWT",
        flags=[],
        has_action_verb=True,
        has_metric=False,
        section="Experience",
    )
    assert br.score == 100
    assert br.text == "Built authentication service using JWT"
    assert br.flags == []
    assert br.has_action_verb is True
    assert br.has_metric is False
    assert br.section == "Experience"

    bullets = _make_bullets([("Built authentication service", "Experience")])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert isinstance(result, BulletScorerResult)
    assert hasattr(result, "results")
    assert hasattr(result, "anti_ai_score")
    assert hasattr(result, "anti_ai_flags")
    assert isinstance(result.results, list)
    assert isinstance(result.anti_ai_score, int)
    assert isinstance(result.anti_ai_flags, list)


@_WAVE2_XFAIL
def test_bullet_result_asdict():
    """dataclasses.asdict(BulletResult(...)) produces dict with exact keys."""
    br = BulletResult(
        score=80,
        text="Deployed services using Terraform",
        flags=["passive_voice"],
        has_action_verb=True,
        has_metric=False,
        section="Experience",
    )
    d = dataclasses.asdict(br)
    assert set(d.keys()) == {"score", "text", "flags", "has_action_verb", "has_metric", "section"}
    assert d["score"] == 80
    assert d["text"] == "Deployed services using Terraform"
    assert d["flags"] == ["passive_voice"]
    assert d["has_action_verb"] is True
    assert d["has_metric"] is False
    assert d["section"] == "Experience"


# ---------------------------------------------------------------------------
# Group 2 — Penalty scoring (BULLET-01 through BULLET-05, D-01 through D-05)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_score_perfect_bullet():
    """Perfect bullet: strong verb + metric + active voice + short → score==100, flags==[]."""
    bullets = _make_bullets([
        ("Reduced API response time by 40% by implementing Redis caching layer", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 100
    assert br.flags == []
    assert br.has_action_verb is True
    assert br.has_metric is True


@_WAVE2_XFAIL
def test_score_weak_verb_only():
    """Bullet starting with weak phrase but with metric → score==65 (100-35), weak_verb only."""
    bullets = _make_bullets([
        ("Helped design the auth service reducing latency by 40%", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 65
    assert "weak_verb" in br.flags
    assert br.has_action_verb is False


@_WAVE2_XFAIL
def test_score_no_outcome_only():
    """Strong verb but no metric/outcome → score==70 (100-30), no_outcome flag set."""
    bullets = _make_bullets([
        ("Built the API endpoint using Flask and PostgreSQL for user authentication", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 70
    assert "no_outcome" in br.flags
    assert br.has_action_verb is True


@_WAVE2_XFAIL
def test_score_passive_voice_only():
    """Bullet with strong verb but passive clause → score==80 (100-20), passive_voice flag."""
    bullets = _make_bullets([
        ("Deployed the pipeline; errors were caught by automated tests", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 80
    assert "passive_voice" in br.flags
    assert br.has_action_verb is True


@_WAVE2_XFAIL
def test_score_too_long_only():
    """Bullet >200 chars with strong verb, metric, active voice → score==85 (100-15), too_long."""
    # This bullet exceeds 200 characters; starts with strong verb, has metric, active voice
    text = (
        "Built and deployed a microservices authentication platform using Spring Boot, "
        "PostgreSQL, Redis, and AWS Lambda, reducing login latency by 50% across 3 environments "
        "and serving over 10000 concurrent users in production"
    )
    assert len(text) > 200, f"Text must exceed 200 chars; got {len(text)}"
    bullets = _make_bullets([(text, "Experience")])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 85
    assert "too_long" in br.flags
    assert br.has_action_verb is True
    assert br.has_metric is True


@_WAVE2_XFAIL
def test_score_all_flags_floor():
    """Bullet triggering all 4 flags → score==0 (floor, not negative)."""
    # weak verb + no metric/outcome + passive voice + long (>160 chars)
    # Uses a weak phrase start so weak_verb triggers
    text = (
        "Worked on and was responsible for the deployment of various authentication services "
        "and infrastructure components using Jenkins, Terraform, and various cloud platforms "
        "that were managed by the DevOps team across multiple regions"
    )
    assert len(text) > 160, f"Text must exceed 160 chars; got {len(text)}"
    bullets = _make_bullets([(text, "Experience")])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 0
    assert "weak_verb" in br.flags
    assert "passive_voice" in br.flags
    assert "too_long" in br.flags


@_WAVE2_XFAIL
def test_score_weak_and_no_outcome():
    """Two flags (weak_verb + no_outcome) → score==35 (100-35-30)."""
    bullets = _make_bullets([
        ("Helped build the database schema for the project", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert len(result.results) == 1
    br = result.results[0]
    assert br.score == 35
    assert "weak_verb" in br.flags
    assert "no_outcome" in br.flags


# ---------------------------------------------------------------------------
# Group 3 — Action verb detection (BULLET-01, D-06 through D-09)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_strong_verb_detection():
    """Bullets starting with known strong verbs → has_action_verb=True, no weak_verb flag."""
    strong_starts = [
        "Built a distributed caching layer using Redis and Memcached",
        "Deployed microservices to AWS EKS using Helm and Terraform",
        "Optimized SQL query performance reducing execution time by 60%",
        "Led a team of 5 engineers delivering the payments platform",
        "Engineered a real-time data pipeline using Apache Kafka",
        "Reduced API response latency by 40% through connection pooling",
        "Designed the authentication service architecture using OAuth2",
        "Automated CI/CD pipelines using GitHub Actions and ArgoCD",
        "Migrated legacy monolith to microservices on AWS ECS",
        "Refactored the codebase reducing technical debt by 30%",
        "Shipped the billing feature enabling $2M in new revenue",
        "Implemented JWT-based authentication for 50k users",
        "Developed REST APIs consumed by 3 mobile applications",
        "Analyzed production logs identifying root cause of 99% of outages",
        "Increased test coverage from 45% to 92% using pytest",
        "Generated weekly performance reports for executive stakeholders",
        "Presented architecture proposals to 20+ senior engineers",
        "Debugged race condition in the distributed lock manager",
        "Architected event-driven system processing 1M events per day",
    ]
    for text in strong_starts:
        bullets = _make_bullets([(text, "Experience")])
        parsed = _make_parsed_with_bullets(bullets)
        result = check(parsed)
        br = result.results[0]
        assert br.has_action_verb is True, f"Expected has_action_verb=True for: {text!r}"
        assert "weak_verb" not in br.flags, f"Expected no weak_verb flag for: {text!r}"


@_WAVE2_XFAIL
def test_weak_phrase_detection():
    """Bullets starting with forbidden weak phrases → has_action_verb=False, weak_verb flag."""
    weak_starts = [
        ("Worked on the authentication module for the backend API", "Experience"),
        ("Helped with the deployment pipeline configuration on AWS", "Experience"),
        ("Assisted in designing the database schema for the project", "Experience"),
        ("Responsible for maintaining the CI/CD infrastructure", "Experience"),
        ("Involved in the migration of legacy services to Kubernetes", "Experience"),
        ("Participated in code reviews improving team code quality", "Experience"),
        ("Contributed to the open-source project adding 3 features", "Experience"),
        ("Supported the team in resolving critical production incidents", "Experience"),
        ("Handled requests from 10+ stakeholders for analytics reports", "Experience"),
    ]
    for text, section in weak_starts:
        bullets = _make_bullets([(text, section)])
        parsed = _make_parsed_with_bullets(bullets)
        result = check(parsed)
        br = result.results[0]
        assert br.has_action_verb is False, f"Expected has_action_verb=False for: {text!r}"
        assert "weak_verb" in br.flags, f"Expected weak_verb flag for: {text!r}"


@_WAVE2_XFAIL
def test_non_verb_start_article():
    """Bullet starting with article → weak_verb=True, has_action_verb=False."""
    bullets = _make_bullets([
        ("The authentication service was refactored to support OAuth2 and JWT", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    br = result.results[0]
    assert br.has_action_verb is False
    assert "weak_verb" in br.flags


@_WAVE2_XFAIL
def test_non_verb_start_pronoun():
    """Bullet starting with pronoun 'I' → weak_verb=True, has_action_verb=False."""
    bullets = _make_bullets([
        ("I built a data pipeline processing 10M records per day", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    br = result.results[0]
    assert br.has_action_verb is False
    assert "weak_verb" in br.flags


@_WAVE2_XFAIL
def test_non_verb_start_number():
    """Bullet starting with number → weak_verb=True, has_action_verb=False."""
    bullets = _make_bullets([
        ("3 services were redesigned and deployed to production using Docker", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    br = result.results[0]
    assert br.has_action_verb is False
    assert "weak_verb" in br.flags


@_WAVE2_XFAIL
def test_verb_check_first_8_tokens_only():
    """Strong verb only at token[9+] → weak_verb=True (verb outside 8-token window ignored)."""
    # Tokens: "The", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "Built" (token index 8)
    # First 8 tokens contain no strong verb; "Built" is at position 8 (0-indexed)
    text = "The quick brown fox jumped over the lazy Built a caching layer"
    tokens = text.split()
    assert len(tokens) >= 9, f"Need at least 9 tokens; got {len(tokens)}"
    assert tokens[8] == "Built", f"Token[8] should be 'Built'; got {tokens[8]}"
    bullets = _make_bullets([(text, "Experience")])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    br = result.results[0]
    assert br.has_action_verb is False
    assert "weak_verb" in br.flags


# ---------------------------------------------------------------------------
# Group 4 — Metric detection (BULLET-02, D-20)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_has_metric_percentage():
    """Bullet containing percentage pattern → has_metric=True."""
    bullets = _make_bullets([
        ("Reduced API latency by 40% using Redis connection pooling", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.results[0].has_metric is True


@_WAVE2_XFAIL
def test_has_metric_dollar():
    """Bullet containing dollar amount → has_metric=True."""
    bullets = _make_bullets([
        ("Generated $5k in monthly recurring revenue by launching the billing feature", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.results[0].has_metric is True


@_WAVE2_XFAIL
def test_has_metric_multiplier():
    """Bullet containing multiplier pattern → has_metric=True."""
    bullets = _make_bullets([
        ("Optimized the search indexer making it 3x faster through parallel processing", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.results[0].has_metric is True


@_WAVE2_XFAIL
def test_has_metric_users():
    """Bullet containing count + users pattern → has_metric=True."""
    bullets = _make_bullets([
        ("Scaled the auth service to support 500 users across 3 geographic regions", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.results[0].has_metric is True


@_WAVE2_XFAIL
def test_has_metric_false():
    """Bullet with no quantifiable metric → has_metric=False."""
    bullets = _make_bullets([
        ("Built authentication service using JWT and Redis for session management", "Experience"),
    ])
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.results[0].has_metric is False


# ---------------------------------------------------------------------------
# Group 5 — Anti-AI rubric (BULLET-06, D-10, D-11)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_anti_ai_condition_1_verb_repetition():
    """Condition 1: ≥30% of bullets share top-2 verbs → verb_repetition flagged."""
    # 4 "Developed", 3 "Implemented", 3 "Built" — top 2 verbs = 7/10 = 70%
    items = [
        ("Developed the API endpoint for user registration using Django", "Experience"),
        ("Developed authentication module with JWT and Redis caching", "Experience"),
        ("Developed database migration scripts for PostgreSQL upgrade", "Experience"),
        ("Developed CI/CD pipeline configuration for the team", "Experience"),
        ("Implemented authentication using OAuth2 and PKCE flow", "Experience"),
        ("Implemented rate limiting middleware reducing abuse by 80%", "Experience"),
        ("Implemented batch processing job for nightly analytics", "Experience"),
        ("Built caching layer using Redis reducing DB load by 40%", "Experience"),
        ("Built REST API consumed by 3 mobile applications", "Experience"),
        ("Built monitoring dashboard using Grafana and Prometheus", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "verb_repetition" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_2_vague_improvement():
    """Condition 2: 3+ bullets with vague verbs and no mechanism noun → vague_improvement flagged."""
    items = [
        ("Optimized performance across the entire platform significantly", "Experience"),
        ("Improved the system to be more efficient and reliable", "Experience"),
        ("Enhanced efficiency through careful process improvements", "Experience"),
        ("Reduced costs by making operations more streamlined", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "vague_improvement" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_4_ungrounded_metric():
    """Condition 4: metric appears without mechanism noun → ungrounded_metric flagged."""
    items = [
        ("Reduced latency by 70% across all services in production", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "ungrounded_metric" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_5_collaboration_no_artifact():
    """Condition 5: collaboration term with no named artifact → collaboration_no_artifact flagged."""
    items = [
        ("Led cross-functional collaboration to align stakeholders on priorities", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "collaboration_no_artifact" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_6_buzzword_density():
    """Condition 6: 3+ buzzwords in one bullet → buzzword_density flagged."""
    items = [
        (
            "Leveraged scalable cloud-native microservices to drive innovation and synergy",
            "Experience",
        ),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "buzzword_density" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_8_fuzzy_duplicate():
    """Condition 8: two bullets share >60% non-stopword tokens → fuzzy_duplicate flagged."""
    items = [
        ("Built authentication service using JWT for user login", "Experience"),
        ("Built authentication module using JWT tokens for user login", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "fuzzy_duplicate" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_9_tense_inconsistency():
    """Condition 9: mix of past and present tense verbs in same section → tense_inconsistency."""
    items = [
        ("Built authentication service using JWT and Redis", "Experience"),
        ("Deployed pipeline to AWS using Terraform and CloudFormation", "Experience"),
        ("Manages CI/CD workflows for the team on a daily basis", "Experience"),
        ("Refactored database schema reducing redundant queries by 30%", "Experience"),
        ("Operates on-call rotation and responds to production incidents", "Experience"),
        ("Migrated legacy monolith to microservices architecture on ECS", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "tense_inconsistency" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_condition_10_marketing_tone():
    """Condition 10: adj/adverb density >35% AND technical noun count <2 → marketing_tone."""
    items = [
        (
            "Highly innovative, exceptionally passionate, remarkably dynamic professional",
            "Experience",
        ),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score >= 1
    assert "marketing_tone" in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_score_clean_bullets():
    """Clean, varied bullets with no AI signals → anti_ai_score==0, anti_ai_flags==[]."""
    items = [
        ("Reduced API response time by 40% by implementing Redis caching", "Experience"),
        ("Deployed authentication service to AWS EKS using Helm charts", "Experience"),
        ("Migrated PostgreSQL schema reducing query time by 35%", "Experience"),
        ("Architected event-driven pipeline processing 1M Kafka events daily", "Experience"),
        ("Debugged race condition in distributed lock manager fixing 3 production outages", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert result.anti_ai_score == 0
    assert result.anti_ai_flags == []


@_WAVE2_XFAIL
def test_anti_ai_conditions_3_and_7_skipped():
    """Conditions 3 and 7 are skipped; their flag names must NOT appear in anti_ai_flags."""
    items = [
        ("Built authentication service using JWT for user sessions", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert "skills_not_in_bullets" not in result.anti_ai_flags
    assert "missing_proof_signals" not in result.anti_ai_flags


@_WAVE2_XFAIL
def test_anti_ai_output_shape():
    """check() returns BulletScorerResult with anti_ai_score as int 0-10 and anti_ai_flags as list."""
    items = [
        ("Built distributed caching layer reducing DB load by 50%", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)
    assert isinstance(result, BulletScorerResult)
    assert isinstance(result.anti_ai_score, int)
    assert 0 <= result.anti_ai_score <= 10
    assert isinstance(result.anti_ai_flags, list)
    for flag in result.anti_ai_flags:
        assert isinstance(flag, str)


# ---------------------------------------------------------------------------
# Group 6 — JSON output shape (BULLET-07, D-18 through D-21)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_json_bullets_list_shape():
    """dataclasses.asdict(BulletResult) produces dict with exact keys and types."""
    br = BulletResult(
        score=70,
        text="Built the API endpoint using Flask",
        flags=["no_outcome"],
        has_action_verb=True,
        has_metric=False,
        section="Experience",
    )
    d = dataclasses.asdict(br)
    assert set(d.keys()) == {"score", "text", "flags", "has_action_verb", "has_metric", "section"}
    assert isinstance(d["score"], int)
    assert isinstance(d["text"], str)
    assert isinstance(d["flags"], list)
    assert isinstance(d["has_action_verb"], bool)
    assert isinstance(d["has_metric"], bool)
    assert isinstance(d["section"], str)


@_WAVE2_XFAIL
def test_json_bullets_summary_shape():
    """BulletScorerResult.summary() or .summary returns dict with all required keys."""
    items = [
        ("Built API endpoint using Flask", "Experience"),
        ("Helped with deployment configuration", "Experience"),
    ]
    bullets = _make_bullets(items)
    parsed = _make_parsed_with_bullets(bullets)
    result = check(parsed)

    # summary may be a method or property
    summary = result.summary() if callable(getattr(result, "summary", None)) else result.summary
    assert isinstance(summary, dict)
    required_keys = {"total", "avg_score", "flagged_count", "anti_ai_score", "anti_ai_flags"}
    assert required_keys.issubset(set(summary.keys())), (
        f"Missing keys: {required_keys - set(summary.keys())}"
    )
    assert isinstance(summary["total"], int)
    assert isinstance(summary["avg_score"], float)
    assert isinstance(summary["flagged_count"], int)
    assert isinstance(summary["anti_ai_score"], int)
    assert isinstance(summary["anti_ai_flags"], list)


# ---------------------------------------------------------------------------
# Group 7 — CLI integration (CLI-05, TEST-03)
# ---------------------------------------------------------------------------


@_WAVE2_XFAIL
def test_scan_json_bullets_non_null(real_resume_pdf):
    """CLI-05: --json scan output has bullets as non-null list with correct item shape."""
    import json

    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Unexpected exit {result.exit_code}: {result.output}"
    data = json.loads(result.stdout)
    assert data["bullets"] is not None, "bullets must be non-null after Phase 4"
    assert isinstance(data["bullets"], list)
    for item in data["bullets"]:
        assert "score" in item
        assert "text" in item
        assert "flags" in item
        assert "has_action_verb" in item
        assert "has_metric" in item
        assert "section" in item


@_WAVE2_XFAIL
def test_scan_json_bullets_summary(real_resume_pdf):
    """CLI-05: --json scan output has bullets summary with correct shape."""
    import json

    result = runner.invoke(app, ["--json", "scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Unexpected exit {result.exit_code}: {result.output}"
    data = json.loads(result.stdout)
    assert data.get("bullets_summary") is not None or (
        isinstance(data.get("bullets"), dict) and "summary" in data["bullets"]
    ), "bullets summary must be present in JSON output"
    # Support two possible JSON shapes: bullets_summary at top level or nested in bullets
    summary = data.get("bullets_summary") or data["bullets"].get("summary")
    assert summary is not None
    for key in ("total", "avg_score", "flagged_count", "anti_ai_score", "anti_ai_flags"):
        assert key in summary, f"Missing summary key: {key}"


@_WAVE2_XFAIL
def test_scan_terminal_shows_bullet_section(real_resume_pdf):
    """CLI-05: terminal scan shows Bullet section and Anti-AI panel."""
    result = runner.invoke(app, ["scan", str(real_resume_pdf)])
    assert result.exit_code == 0, f"Unexpected exit {result.exit_code}: {result.output}"
    output_lower = result.output.lower()
    assert "bullet" in output_lower, (
        f"Terminal report must contain a Bullet section — got: {result.output[:400]}"
    )
    assert "anti-ai" in result.output.lower() or "anti_ai" in result.output.lower(), (
        f"Terminal report must contain Anti-AI panel — got: {result.output[:400]}"
    )
