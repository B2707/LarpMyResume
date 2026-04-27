"""Keyword gap analyzer — deterministic gazetteer matching, no LLM calls."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from larpmyresume.analyzers.skills_gazetteer import (
    DISAMBIGUATION_BLOCKLIST,
    GAZETTEER,
    SKILL_PARENTS,
)

if TYPE_CHECKING:
    from larpmyresume.extractor import ParsedResume

# ── Constants ──────────────────────────────────────────────────────────────

REQUIRED_RE = re.compile(r"\b(must|required|mandatory|essential)\b", re.IGNORECASE)
PREFERRED_RE = re.compile(
    r"\b(nice\s+to\s+have|preferred|bonus|plus|desirable|ideally)\b",
    re.IGNORECASE,
)
NEGATED_REQUIRED_RE = re.compile(
    r"\bnot\s+(?:required|mandatory|essential)\b", re.IGNORECASE
)

# Matches term in a comma/colon-separated list context (e.g. "Skills: Go, Python")
COMMA_LIST_TEMPLATE = r"(?:^|[:,]\s*){term}\s*(?:,|$)"

# ── Dataclasses ────────────────────────────────────────────────────────────


@dataclass
class SkillMatch:
    skill: str        # display name (e.g. "PostgreSQL")
    importance: str   # "required" | "preferred"
    found_in: str     # section name normalized, "other" if section unknown, or "" for MISS


@dataclass
class KeywordMatchResult:
    hits: list[SkillMatch]
    weak: list[SkillMatch]
    missing: list[SkillMatch]

    def summary(self) -> dict:
        return {
            "hit_count": len(self.hits),
            "weak_count": len(self.weak),
            "miss_count": len(self.missing),
        }

# ── Normalization ──────────────────────────────────────────────────────────


def _normalize(text: str) -> str:
    """Lowercase + strip punctuation except + and # (for C++, C#)."""
    text = text.lower()
    text = re.sub(r"[^\w\s+#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# ── Importance classification ──────────────────────────────────────────────

def _split_sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", text)


def _classify_importance(skill_pattern: str, jd_sentences: list[str]) -> str:
    """Return 'required' or 'preferred' for a skill in the JD. Default: 'required'."""
    for i, sent in enumerate(jd_sentences):
        if not re.search(skill_pattern, sent, re.IGNORECASE):
            continue
        # ±1 sentence window
        window = " ".join(jd_sentences[max(0, i - 1): i + 2])
        # strip negations before checking required signal
        cleaned = NEGATED_REQUIRED_RE.sub("", window)
        if REQUIRED_RE.search(cleaned):
            return "required"
        if PREFERRED_RE.search(window):
            return "preferred"
    return "required"  # KW-05: default when no signal present


# ── Disambiguation ─────────────────────────────────────────────────────────

def _matches_blocklist_term(
    canonical: str,
    aliases: list[str],
    norm_text: str,
    raw_text: str,
) -> bool:
    """For blocklist terms: accept only if non-canonical alias found OR comma-list context.

    Args:
        canonical: The canonical skill key (e.g. "go").
        aliases: Full alias list; aliases[0] is the display name.
        norm_text: Normalized (lowercase, punctuation-stripped) JD text for alias matching.
        raw_text: Original JD text (commas preserved) for comma-list context matching.
    """
    # Check all aliases except bare canonical (which is ambiguous — handled by comma-list).
    # This correctly handles single-alias entries like "r": ["r"] and "c": ["c"].
    for alias in aliases:
        norm_alias = alias.lower()
        if norm_alias == canonical:
            continue  # skip bare canonical — it's ambiguous; handled by comma-list below
        if re.search(r"\b" + re.escape(norm_alias) + r"\b", norm_text):
            return True
    # Comma-list check on raw text (commas preserved after normalization strips them)
    pattern = re.compile(
        COMMA_LIST_TEMPLATE.format(term=re.escape(canonical)),
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(pattern.search(raw_text))


# ── Resume skill search ────────────────────────────────────────────────────

def _find_skill_in_resume(
    canonical: str,
    aliases: list[str],
    parsed: "ParsedResume",
) -> str:
    """Return normalized section name where skill is found, or '' if not found."""
    norm_raw = _normalize(parsed.raw_text)
    for alias in aliases:
        norm_alias = _normalize(alias)
        # word-boundary search on normalized text
        if re.search(r"\b" + re.escape(norm_alias) + r"\b", norm_raw):
            # identify the section
            for section_name, lines in parsed.sections.items():
                section_text = _normalize(" ".join(lines))
                if re.search(r"\b" + re.escape(norm_alias) + r"\b", section_text):
                    return section_name.lower().rstrip(":").strip()
            return "other"
    return ""


# ── Main entry point ───────────────────────────────────────────────────────

def check(parsed: "ParsedResume", jd_text: str) -> KeywordMatchResult:
    """Classify all gazetteer skills found in jd_text as HIT, WEAK, or MISS.

    Args:
        parsed: Extracted resume data.
        jd_text: Raw job description text (plain text, not HTML).

    Returns:
        KeywordMatchResult with hits, weak, and missing lists.
    """
    norm_jd = _normalize(jd_text)
    jd_sentences = _split_sentences(jd_text)

    hits: list[SkillMatch] = []
    weak: list[SkillMatch] = []
    missing: list[SkillMatch] = []

    for canonical, aliases in GAZETTEER.items():
        # 1. Is this skill mentioned in the JD?
        found_in_jd = False
        for alias in aliases:
            norm_alias = _normalize(alias)
            if canonical in DISAMBIGUATION_BLOCKLIST:
                if _matches_blocklist_term(canonical, aliases, norm_jd, jd_text):
                    found_in_jd = True
                    break
            else:
                if re.search(r"\b" + re.escape(norm_alias) + r"\b", norm_jd):
                    found_in_jd = True
                    break

        if not found_in_jd:
            continue  # not in JD — skip

        # 2. Classify importance from JD sentence context
        # Build pattern from raw aliases so it matches raw JD sentences.
        # _normalize would corrupt aliases like "C++" → "c  " or "GitHub Actions" → "github_actions".
        alias_pattern = "|".join(re.escape(a) for a in aliases)
        importance = _classify_importance(alias_pattern, jd_sentences)

        # Display name: first alias
        display_name = aliases[0]

        # 3. Is this skill in the resume? (exact or alias match)
        found_in_resume = _find_skill_in_resume(canonical, aliases, parsed)

        if found_in_resume:
            # HIT
            hits.append(SkillMatch(
                skill=display_name,
                importance=importance,
                found_in=found_in_resume,
            ))
            continue

        # 4. WEAK check: does resume have a child skill that satisfies this parent?
        # For each skill R in resume, if SKILL_PARENTS[R] == canonical → WEAK
        weak_found = False
        for child_canonical, parent_canonical in SKILL_PARENTS.items():
            if parent_canonical != canonical:
                continue
            child_aliases = GAZETTEER.get(child_canonical, [child_canonical])
            child_section = _find_skill_in_resume(child_canonical, child_aliases, parsed)
            if child_section:
                weak.append(SkillMatch(
                    skill=display_name,
                    importance=importance,
                    found_in=child_section,
                ))
                weak_found = True
                break

        if not weak_found:
            # MISS
            missing.append(SkillMatch(
                skill=display_name,
                importance=importance,
                found_in="",
            ))

    return KeywordMatchResult(hits=hits, weak=weak, missing=missing)
