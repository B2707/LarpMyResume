"""ATS compliance analyzer — deterministic, no LLM calls."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from larpmyresume.extractor import ParsedResume

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STANDARD_HEADINGS: frozenset[str] = frozenset({
    # Core sections (narrow canonical names)
    "experience", "education", "projects", "skills",
    "work experience", "technical skills", "selected projects",
    # Common supplementary sections — all recognized by major ATS parsers
    "summary", "objective", "certifications", "awards", "publications",
    "volunteering", "languages", "interests", "extracurricular",
    "activities", "honors", "coursework", "relevant coursework",
    "additional experience", "leadership",
    # Common real-world variants — kept in sync with KNOWN_SECTIONS in extractor.py.
    # These are widely used by real candidates and recognized by major ATS systems;
    # flagging them as non-standard would be a false positive.
    "professional experience", "professional summary", "career summary",
    "career objective", "professional background", "work history",
    "professional skills", "technical expertise", "core competencies",
    "programming languages", "tools", "technologies", "software",
    "open source", "open source contributions", "side projects",
    "personal projects", "research", "research experience",
    "teaching experience", "volunteer experience",
    "achievements", "accomplishments", "recognition",
    "professional development", "training", "references",
    "about", "profile",
})

_STANDARD_HEADINGS_NOSPACE: frozenset[str] = frozenset(
    s.replace(" ", "") for s in STANDARD_HEADINGS
)

# Four scored families — 25 points each for section_score (ATS-04).
# Each family includes canonical names AND common real-world variants so that
# resumes using "Professional Experience" or "Core Competencies" still receive
# a full section score rather than a false-zero.
_SCORED_FAMILIES: list[frozenset[str]] = [
    frozenset({"education", "academic background", "academic experience"}),
    frozenset({
        "experience", "work experience", "professional experience",
        "professional background", "work history", "additional experience",
        "teaching experience", "research experience",
    }),
    frozenset({
        "skills", "technical skills", "professional skills",
        "core competencies", "technical expertise", "tools",
        "technologies", "programming languages", "software",
    }),
    frozenset({
        "projects", "selected projects", "side projects",
        "personal projects", "open source", "open source contributions",
        "research",
    }),
]

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ATSFlag:
    flag: str
    severity: Literal["High", "Medium", "Low"]
    explanation: str


@dataclass
class ATSResult:
    flags: list[ATSFlag]
    section_score: int  # 0-100


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------

def check(parsed: ParsedResume) -> ATSResult:
    flags: list[ATSFlag] = []

    # ATS-02: multi-column layout → High
    if parsed.meta.get("is_multi_column"):
        flags.append(ATSFlag(
            flag="multi_column_layout",
            severity="High",
            explanation=(
                "Multi-column layout detected. Many ATS parsers read left-to-right "
                "across the full page width, causing skills from the right column to "
                "be interleaved with experience text from the left column."
            ),
        ))

    # ATS-03: image-heavy (belt-and-suspenders — ImageOnlyPDFError already fires in extract())
    if len(parsed.chars) == 0 and len(parsed.raw_text.strip()) > 0:
        flags.append(ATSFlag(
            flag="image_heavy",
            severity="High",
            explanation=(
                "No character-level text data found. The PDF may contain images "
                "of text rather than selectable text. ATS systems cannot read image-based text."
            ),
        ))

    # ATS-01: non-standard headings → Medium
    for heading in parsed.sections:
        canonical = heading.lower().rstrip(":").strip()
        if canonical not in STANDARD_HEADINGS and canonical.replace(" ", "") not in _STANDARD_HEADINGS_NOSPACE:
            flags.append(ATSFlag(
                flag=f"non_standard_heading:{heading}",
                severity="Medium",
                explanation=(
                    f"Heading '{heading}' is not a standard ATS section name. "
                    "Consider renaming to: Experience, Education, Skills, Projects, "
                    "Work Experience, Technical Skills, or Selected Projects."
                ),
            ))

    # ATS-04: section score
    section_keys_lower = {k.lower().rstrip(":").strip() for k in parsed.sections}
    score = sum(
        25 for family in _SCORED_FAMILIES
        if any(member in section_keys_lower for member in family)
    )

    return ATSResult(flags=flags, section_score=score)
