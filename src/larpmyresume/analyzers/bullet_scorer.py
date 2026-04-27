"""Bullet quality scorer — deterministic, no LLM calls."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from larpmyresume.extractor import Bullet, ParsedResume

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STRONG_VERBS: frozenset[str] = frozenset({
    # Leadership
    "spearheaded", "directed", "orchestrated", "led", "established", "managed",
    "oversaw", "supervised", "chaired",
    # Analysis
    "evaluated", "assessed", "researched", "identified", "forecasted", "diagnosed",
    "analyzed", "investigated", "audited",
    # Achievement
    "increased", "generated", "reduced", "improved", "exceeded", "delivered",
    "achieved", "accelerated", "boosted",
    # Communication
    "presented", "negotiated", "persuaded", "authored", "influenced", "documented",
    "reported", "published",
    # Technical
    "programmed", "engineered", "designed", "implemented", "constructed", "built",
    "developed", "deployed", "migrated", "automated", "refactored", "optimized",
    "integrated", "shipped", "debugged", "architected",
})

WEAK_PHRASES: tuple[str, ...] = (
    "worked on",
    "helped",
    "assisted",
    "responsible for",
    "involved in",
    "participated in",
    "contributed to",
    "supported",
    "handled",
)

NON_VERB_START_TOKENS: frozenset[str] = frozenset({
    # Articles
    "the", "a", "an",
    # Pronouns
    "i", "we", "our", "my", "your", "their", "its",
})

BUZZWORDS: frozenset[str] = frozenset({
    "leveraged", "scalable", "robust", "cutting-edge", "synergy", "cloud-native",
    "innovative", "seamlessly", "revolutionized", "game-changing", "significantly",
    "best-in-class",
    # Extended
    "leveraging", "dynamic", "passionate", "results-driven", "results-oriented",
    "thought-leadership", "value-add", "go-getter",
})

MECHANISM_NOUNS: frozenset[str] = frozenset({
    "api", "db", "database", "test", "pipeline", "service", "schema", "cache",
    "queue", "endpoint", "migration", "index", "circuit breaker", "microservice",
    "function", "lambda", "container", "cluster", "ingress", "webhook", "job",
    "worker", "stream", "topic", "bucket", "table", "query", "view", "trigger",
    "cron", "model", "module",
})

COLLABORATION_ARTIFACTS: frozenset[str] = frozenset({
    "api", "rfc", "pr", "dashboard", "runbook", "ticket", "pipeline", "prd",
    "incident report", "readme", "spec", "adr", "design doc", "oncall", "postmortem",
})

COLLABORATION_TERMS: frozenset[str] = frozenset({
    "led", "collaborated", "aligned", "partnered", "facilitated", "coordinated",
})

STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "up", "about", "into", "through", "during", "is", "are",
    "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "it", "its", "this",
    "that", "these", "those", "i", "we", "my", "our", "your", "their", "his", "her",
})

MARKETING_ADJECTIVES: frozenset[str] = frozenset({
    "highly", "innovative", "exceptional", "exceptionally", "passionate", "dynamic",
    "remarkable", "remarkably", "results-driven", "results-oriented", "talented",
    "motivated", "dedicated", "hardworking", "outstanding", "excellent",
    "best-in-class", "cutting-edge", "robust", "scalable", "seamless",
    "revolutionary", "game-changing",
})

# Compiled regex patterns
HAS_METRIC_RE: re.Pattern[str] = re.compile(
    r'\d+\s*%'                          # percentages: 40%, 100 %
    r'|\$\d+'                           # dollar amounts: $500, $1M
    r'|\d+[xX]\b'                       # multipliers: 2x, 10X
    r'|\d+[kKmMbB]\b'                   # scale suffixes standalone: 10k, 1M, 2B
    r'|\d+\s*(users|customers|requests|ms|seconds|minutes|hours|days|lines|'
    r'files|tests|commits|engineers|services|endpoints|queries|errors|incidents|'
    r'teams|repos|repositories|deployments|builds|records|transactions|'
    r'components|features|tickets|issues|bugs|prs|sprints|releases|'
    r'environments|instances|pods|nodes|countries|regions|clients|accounts)',
    re.IGNORECASE,
)

PASSIVE_VOICE_RE: re.Pattern[str] = re.compile(
    # Matches regular -ed past participles AND common irregular past participles
    r'\b(was|were|is|are|been|being)\s+'
    r'(?:\w+ed|caught|built|done|given|found|known|made|run|set|sent|taken|'
    r'thought|left|brought|bought|taught|sought|written|chosen|broken|driven|'
    r'grown|shown|stolen|thrown|worn|begun|come|become|seen|held|kept|lost|'
    r'meant|met|paid|read|said|stood|told|understood|won)\b',
    re.IGNORECASE,
)

PAST_TENSE_RE: re.Pattern[str] = re.compile(
    r'^(built|deployed|migrated|refactored|designed|implemented|reduced|increased|'
    r'led|automated|engineered|shipped|debugged|architected|developed|analyzed|'
    r'generated|achieved|delivered|improved)\b',
    re.IGNORECASE,
)

PRESENT_TENSE_RE: re.Pattern[str] = re.compile(
    r'^(builds|deploys|manages|operates|maintains|develops|leads|runs|handles|'
    r'designs|implements|coordinates|reviews|monitors)\b',
    re.IGNORECASE,
)

TOO_LONG_CHARS: int = 200  # ~2.5 lines at typical resume font sizes; 160 falsely fires on normal 2-line bullets

SCORE_PENALTIES: dict[str, int] = {
    "weak_verb": 35,
    "no_outcome": 30,
    "passive_voice": 20,
    "too_long": 15,
}

FUZZY_DUPLICATE_THRESHOLD: float = 0.60


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class BulletResult:
    score: int
    text: str
    flags: list[str]
    has_action_verb: bool
    has_metric: bool
    section: str


@dataclass
class BulletScorerResult:
    results: list[BulletResult]
    anti_ai_score: int
    anti_ai_flags: list[str]

    def summary(self) -> dict:
        total = len(self.results)
        avg_score = sum(r.score for r in self.results) / total if total else 0.0
        flagged_count = sum(1 for r in self.results if r.flags)
        return {
            "total": total,
            "avg_score": round(avg_score, 1),
            "flagged_count": flagged_count,
            "anti_ai_score": self.anti_ai_score,
            "anti_ai_flags": self.anti_ai_flags,
        }


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _score_bullet(bullet: Bullet) -> BulletResult:
    """Score a single bullet using penalty-based algorithm (D-01 through D-05).

    Algorithm:
    1. Detect weak_verb: fires when first token is NON_VERB_START/digit/weak_phrase,
       OR when no STRONG_VERB appears in tokens[:8].
    2. has_action_verb: True only when no weak_verb trigger fires AND a STRONG_VERB
       appears in tokens[:8].
    3. no_outcome: fires when NOT has_metric AND NOT (passive_voice AND has_action_verb).
       Rationale: a bullet with a strong action verb + passive voice implies something
       happened as a result; suppress no_outcome. Without a strong action verb, passive
       does not suppress no_outcome.
    """
    text = bullet.text
    tokens = text.lower().split()

    has_action_verb = False
    weak_verb = False

    if tokens:
        first_token = tokens[0]

        # D-09: Non-verb start (articles, pronouns, numbers) → unconditional override
        if first_token in NON_VERB_START_TOKENS or first_token[0].isdigit():
            weak_verb = True
            has_action_verb = False
        else:
            # Check for weak phrases against first ~3 tokens
            first_few = " ".join(tokens[:3])
            phrase_matched = False
            for phrase in WEAK_PHRASES:
                if " " not in phrase:
                    if first_token == phrase:
                        phrase_matched = True
                        break
                else:
                    if first_few.startswith(phrase):
                        phrase_matched = True
                        break

            if phrase_matched:
                # Weak phrase detected — has_action_verb=False (overrides strong verb check)
                weak_verb = True
                has_action_verb = False
            else:
                # Check first 8 tokens for a strong verb (D-04)
                first_8 = tokens[:8]
                if any(t in STRONG_VERBS for t in first_8):
                    has_action_verb = True
                    weak_verb = False
                else:
                    # No strong verb found in first 8 tokens → weak
                    weak_verb = True
                    has_action_verb = False

    # --- Metric detection ---
    has_metric = bool(HAS_METRIC_RE.search(text))

    # --- Passive voice ---
    passive_voice = bool(PASSIVE_VOICE_RE.search(text.lower()))

    # --- no_outcome: fires when no metric AND NOT (passive + strong action) ---
    # A bullet with a strong action verb (has_action_verb=True) that also contains a
    # passive construction implies an outcome was described (even without a number).
    # When weak_verb=True (has_action_verb=False), passive does not suppress no_outcome.
    no_outcome = not has_metric and not (passive_voice and has_action_verb)

    too_long = len(text) > TOO_LONG_CHARS

    # --- Build flags list ---
    flags: list[str] = []
    if weak_verb:
        flags.append("weak_verb")
    if no_outcome:
        flags.append("no_outcome")
    if passive_voice:
        flags.append("passive_voice")
    if too_long:
        flags.append("too_long")

    # --- Score with floor at 0 ---
    score = max(0, 100 - sum(SCORE_PENALTIES[f] for f in flags))

    return BulletResult(
        score=score,
        text=text,
        flags=flags,
        has_action_verb=has_action_verb,
        has_metric=has_metric,
        section=bullet.section,
    )


def _compute_anti_ai(bullets: list[Bullet]) -> tuple[int, list[str]]:
    """Compute anti-AI rubric score and flags (D-10, D-11).

    Conditions computed in order 1,2,(skip 3),4,5,6,(skip 7),8,9,10.
    Returns (score, flags).
    """
    score = 0
    flags: list[str] = []

    if not bullets:
        return score, flags

    # Condition 1 (verb_repetition): top-2 opening verbs account for ≥30% of all bullets
    # AND the most common opening verb appears at least twice (actual repetition).
    opening_tokens = [b.text.lower().split()[0] for b in bullets if b.text.split()]
    if opening_tokens:
        token_counts = Counter(opening_tokens)
        most_common = token_counts.most_common(2)
        # Require the top verb appears at least twice — prevents false positives on
        # resumes with all-unique opening verbs where top-2 sum is still ≥30%.
        if most_common[0][1] >= 2:
            top2_count = sum(count for _, count in most_common)
            ratio = top2_count / len(opening_tokens)
            if ratio >= 0.30:
                score += 1
                flags.append("verb_repetition")

    # Condition 2 (vague_improvement): ≥3 bullets with vague verbs and no mechanism noun
    # Use word-set intersection for mechanism noun check (word boundary, not substring).
    vague_verbs = {"optimized", "improved", "enhanced"}
    vague_count = 0
    for b in bullets:
        text_lower = b.text.lower()
        words = set(text_lower.split())
        has_vague = any(v in words for v in vague_verbs)
        has_mechanism = bool(words & MECHANISM_NOUNS)
        if has_vague and not has_mechanism:
            vague_count += 1
    if vague_count >= 3:
        score += 1
        flags.append("vague_improvement")

    # Condition 3: SKIP (requires skills section data not in ParsedResume.bullets)

    # Condition 4 (ungrounded_metric): metric without mechanism noun in same bullet.
    # Use exact whole-word matching — "services" does NOT match noun "service".
    # Intentional: break after first offending bullet — rubric flags the pattern, not every instance.
    for b in bullets:
        if HAS_METRIC_RE.search(b.text):
            text_lower = b.text.lower()
            words = set(text_lower.split())
            has_mechanism = bool(words & MECHANISM_NOUNS)
            if not has_mechanism:
                score += 1
                flags.append("ungrounded_metric")
                break

    # Condition 5 (collaboration_no_artifact): collaboration term with no artifact.
    # Use word-set intersection for both collab terms and artifacts to avoid substring
    # false matches (e.g. "pr" matching "priorities", "api" matching "captain").
    # Intentional: break after first offending bullet — rubric flags the pattern, not every instance.
    for b in bullets:
        text_lower = b.text.lower()
        words = set(text_lower.split())
        has_collab = bool(words & COLLABORATION_TERMS)
        if has_collab:
            # For artifacts: check whole-word match; multi-word artifacts use phrase match.
            has_artifact = False
            for a in COLLABORATION_ARTIFACTS:
                if " " in a:
                    # Multi-word artifact: phrase match
                    if a in text_lower:
                        has_artifact = True
                        break
                else:
                    # Single-word artifact: whole-word match only
                    if a in words:
                        has_artifact = True
                        break
            if not has_artifact:
                score += 1
                flags.append("collaboration_no_artifact")
                break

    # Condition 6 (buzzword_density): ≥3 buzzwords in a single bullet
    for b in bullets:
        text_lower = b.text.lower()
        word_tokens = text_lower.split()
        buzzword_count = sum(1 for w in word_tokens if w in BUZZWORDS)
        if buzzword_count >= 3:
            score += 1
            flags.append("buzzword_density")
            break

    # Condition 7: SKIP (requires project/proof signal data not in bullets)

    # Condition 8 (fuzzy_duplicate): >60% non-stopword token overlap between any pair
    def _content_tokens(text: str) -> frozenset[str]:
        return frozenset(t for t in text.lower().split() if t not in STOPWORDS)

    token_sets = [_content_tokens(b.text) for b in bullets]
    fuzzy_found = False
    for i in range(len(token_sets)):
        for j in range(i + 1, len(token_sets)):
            si, sj = token_sets[i], token_sets[j]
            union = si | sj
            if not union:
                continue
            overlap = len(si & sj) / len(union)
            if overlap > FUZZY_DUPLICATE_THRESHOLD:
                fuzzy_found = True
                break
        if fuzzy_found:
            break
    if fuzzy_found:
        score += 1
        flags.append("fuzzy_duplicate")

    # Condition 9 (tense_inconsistency): mix of past and present tense verbs across bullets
    has_past = any(PAST_TENSE_RE.match(b.text) for b in bullets)
    has_present = any(PRESENT_TENSE_RE.match(b.text) for b in bullets)
    if has_past and has_present:
        score += 1
        flags.append("tense_inconsistency")

    # Condition 10 (marketing_tone): adj/adverb density >35% AND technical noun count <2
    for b in bullets:
        text_lower = b.text.lower()
        word_tokens = [w for w in text_lower.split() if w not in STOPWORDS]
        content_word_count = len(word_tokens)
        if content_word_count == 0:
            continue
        adj_adv_count = sum(1 for w in word_tokens if w in MARKETING_ADJECTIVES)
        tech_noun_count = sum(1 for w in word_tokens if w in MECHANISM_NOUNS)
        if (adj_adv_count / content_word_count > 0.35) and (tech_noun_count < 2):
            score += 1
            flags.append("marketing_tone")
            break

    return score, flags


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def check(parsed: ParsedResume) -> BulletScorerResult:
    """Score all bullets in parsed resume and compute anti-AI risk rubric."""
    results = [_score_bullet(b) for b in parsed.bullets]
    anti_ai_score, anti_ai_flags = _compute_anti_ai(parsed.bullets)
    return BulletScorerResult(
        results=results,
        anti_ai_score=anti_ai_score,
        anti_ai_flags=anti_ai_flags,
    )
