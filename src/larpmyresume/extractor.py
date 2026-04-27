from __future__ import annotations

import os
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pdfplumber

# ---------------------------------------------------------------------------
# Named constants — every tuneable value is a module-level constant.
# Never inline these literals in logic (PATTERNS.md "Named constants").
# ---------------------------------------------------------------------------

MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024          # 50MB hard limit (T-01-05 security)
MULTI_COLUMN_GAP_THRESHOLD: float = 0.20             # fraction of page width
COLUMN_WITHIN_LINE_GAP_PTS: float = 50.0             # min gap (pts) to flag second column start
HEADER_EXCLUSION_RATIO: float = 0.20                 # top fraction of page excluded from analysis

KNOWN_SECTIONS: frozenset[str] = frozenset({
    # Core sections (narrow canonical names)
    "experience", "education", "skills", "projects",
    "work experience", "technical skills", "selected projects",
    "summary", "objective", "certifications", "awards",
    "publications", "volunteering", "languages", "interests",
    "extracurricular", "activities", "honors", "coursework",
    "relevant coursework", "additional experience", "leadership",
    # Common real-world variants — sourced from ATS parsing research
    # (these are widely used on real resumes and recognized by major ATS systems)
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

# Space-collapsed lookup set — handles PDFs that merge adjacent words into a
# single token (e.g. "WorkExperience" instead of "Work Experience"). Built
# automatically from KNOWN_SECTIONS so it never drifts out of sync.
_KNOWN_SECTIONS_NOSPACE: frozenset[str] = frozenset(
    s.replace(" ", "") for s in KNOWN_SECTIONS
)

# Bullet characters recognized during extraction.
# Includes standard ASCII/Unicode bullets plus right-pointing triangles
# used by some LaTeX and Word resume templates.
BULLET_CHARS: frozenset[str] = frozenset({
    "•", "–", "-", "*", "▪", "◦", "·",
    "▸", "›", "»", ">",   # right-pointing variants used by some templates
})

_DATE_RE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4}|present)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ImageOnlyPDFError(ValueError):
    """Raised when PDF contains images but zero extractable text (scanned PDF)."""


class EmptyPDFError(ValueError):
    """Raised when PDF contains neither text nor images (corrupt or blank)."""


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Bullet:
    text: str        # continuation-merged text; bullet prefix char stripped
    section: str     # raw section heading as found in PDF — NEVER normalized (D-07)
    line_num: int    # line index in raw_text.splitlines()


@dataclass
class ParsedResume:
    raw_text: str                   # D-05: full text, post-NFKC normalization
    sections: dict[str, list[str]]  # D-02: raw heading -> all lines in that section
    bullets: list[Bullet]           # D-01: Bullet objects with continuation lines merged
    chars: list[dict]               # D-03: all pdfplumber char dicts across all pages
    meta: dict                      # D-04: {"is_multi_column": bool, "page_count": int}
    source_path: str = ""           # convenience: original PDF path as string


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _detect_multicolumn(chars: list[dict], page_width: float, page_height: float) -> bool:
    """Detect whether a PDF page has a multi-column layout.

    Uses a histogram-based peak detection approach (PATTERNS.md Pattern 3).
    Excludes the top HEADER_EXCLUSION_RATIO of the page to avoid false positives
    from centered name/contact info in resume headers.

    Args:
        chars: All pdfplumber char dicts, already collected from the PDF.
        page_width: Width of the (first) page in points.
        page_height: Height of the (first) page in points.

    Returns:
        True if two distinct left-margin clusters are detected with a gap
        exceeding MULTI_COLUMN_GAP_THRESHOLD * page_width.
    """
    body_top = page_height * HEADER_EXCLUSION_RATIO
    body_chars = [c for c in chars if c.get("top", 0) > body_top]
    if not body_chars:
        return False

    # Group chars by line (snap top to nearest 2pts to group same-line chars)
    lines: dict[int, list[float]] = defaultdict(list)
    for c in body_chars:
        line_key = round(c.get("top", 0) / 2) * 2
        lines[line_key].append(c.get("x0", 0.0))

    # Collect column-start x positions: leftmost in each line, plus any
    # x position that is more than COLUMN_WITHIN_LINE_GAP_PTS from the previous.
    all_starts: list[float] = []
    for xs in lines.values():
        xs_sorted = sorted(xs)
        all_starts.append(xs_sorted[0])
        for i in range(1, len(xs_sorted)):
            if xs_sorted[i] - xs_sorted[i - 1] > COLUMN_WITHIN_LINE_GAP_PTS:
                all_starts.append(xs_sorted[i])

    if len(all_starts) < 5:
        return False

    # Build a histogram of column-start positions using bucket_size-pt bins.
    bucket_size = max(page_width / 30, 10.0)
    buckets: dict[int, int] = defaultdict(int)
    for s in all_starts:
        buckets[int(s / bucket_size)] += 1

    sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_buckets) < 2:
        return False

    top1_bucket, top1_count = sorted_buckets[0]
    for bucket_idx, count in sorted_buckets[1:]:
        # A secondary cluster is significant if it has at least 25% the count of the top cluster.
        if count >= top1_count * 0.25:
            gap_pts = abs(bucket_idx - top1_bucket) * bucket_size
            if gap_pts / page_width > MULTI_COLUMN_GAP_THRESHOLD:
                return True
    return False


def _is_section_heading(line: str) -> bool:
    """Determine whether a line is a section heading.

    Uses a two-pass approach (PATTERNS.md Pattern 4):
    1. Known-section canonical match (case-insensitive, colon-stripped).
    2. Style heuristics: ALL CAPS with high alpha ratio, Title Case without
       digits, or ends with a colon — with guards against dates, bullets, and
       long lines.

    Known limitation: "Software Engineer Intern" is classified as a Title Case
    heading. This is acceptable and intentional — documented in PATTERNS.md.
    Do NOT add a special-case override here.
    """
    stripped = line.strip()
    if not stripped or len(stripped) < 2:
        return False
    if stripped[0] in BULLET_CHARS:
        return False

    canonical = stripped.lower().rstrip(":").strip()
    if canonical in KNOWN_SECTIONS:
        return True
    # PDF space-merge fallback: "WorkExperience" → "workexperience" matches "work experience"
    if canonical.replace(" ", "") in _KNOWN_SECTIONS_NOSPACE:
        return True

    if len(stripped) > 40:
        return False
    if "," in stripped or "|" in stripped:
        return False
    if _DATE_RE.search(stripped):
        return False

    # ALL CAPS with >70% alpha ratio
    if stripped.isupper():
        alpha_ratio = sum(1 for c in stripped if c.isalpha()) / len(stripped)
        if alpha_ratio > 0.70:
            return True

    # Title Case (every alphabetic word starts with uppercase) with no digits
    words = stripped.rstrip(":").split()
    if words and all(w[0].isupper() for w in words if w and w[0].isalpha()):
        if not any(c.isdigit() for c in stripped):
            return True

    # Ends with colon
    if stripped.endswith(":"):
        return True

    return False


def _extract_sections_and_bullets(
    raw_text: str,
) -> tuple[dict[str, list[str]], list[Bullet]]:
    """Segment raw_text into sections and extract bullets with continuation merging.

    Single-pass line iteration (PATTERNS.md Pattern 5). Applies decisions:
    - D-06: Known-section list first, then style heuristic.
    - D-07: Sections dict keyed by raw heading (never normalized).
    - D-08: Continuation lines merged into preceding Bullet.text.

    Args:
        raw_text: Full post-NFKC-normalized text from the PDF.

    Returns:
        (sections, bullets) — sections maps raw heading -> list of non-heading lines;
        bullets is a list of Bullet objects with continuation lines merged.
    """
    sections: dict[str, list[str]] = {}
    bullets: list[Bullet] = []
    current_section: str | None = None
    last_bullet: Bullet | None = None
    first_line_seen: bool = False  # tracks name exclusion (D-NAME): first non-empty line is always the candidate name, never a section heading

    for line_num, line in enumerate(raw_text.splitlines()):
        stripped = line.strip()
        if not stripped:
            last_bullet = None      # blank line breaks continuation (D-08, Pitfall 6)
            continue

        # D-NAME: The very first non-empty line that is NOT a known section keyword
        # is the candidate name (e.g. "Bader El-Asadi"). Skip heading classification
        # for it so the Title Case heuristic does not misclassify it as a section.
        # Known sections ("EXPERIENCE", "Education", etc.) are allowed through even
        # when they appear first, because some resume formats start with a section.
        if not first_line_seen:
            first_line_seen = True
            if stripped.lower().rstrip(":").strip() not in KNOWN_SECTIONS:
                continue

        if _is_section_heading(stripped):
            current_section = stripped      # D-07: raw heading — never normalized
            sections.setdefault(current_section, [])
            last_bullet = None
            continue

        if current_section is not None:
            sections[current_section].append(stripped)

        is_bullet = stripped[0] in BULLET_CHARS
        if is_bullet and current_section is not None:
            text = stripped.lstrip("".join(BULLET_CHARS)).strip()
            b = Bullet(text=text, section=current_section, line_num=line_num)
            bullets.append(b)
            last_bullet = b
        elif last_bullet is not None and current_section is not None:
            last_bullet.text = last_bullet.text + " " + stripped   # continuation merge (D-08)
        else:
            last_bullet = None

    return sections, bullets


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------


def extract(pdf_path: str | Path) -> ParsedResume:
    """Extract text and structure from a PDF file.

    Security: raises ValueError if file exceeds MAX_FILE_SIZE_BYTES (50MB).
    Raises ImageOnlyPDFError if PDF is image-only (scanned).
    Raises EmptyPDFError if PDF contains no text or images.
    Caller (CLI layer in Phase 2) is responsible for user-facing error messages.

    Opens the PDF exactly ONCE (PATTERNS.md anti-patterns: "Do not re-open").
    All page data collected in a single with-block pass.
    """
    path = Path(pdf_path)

    # SECURITY (T-01-05): 50MB file size guard — must happen BEFORE pdfplumber.open()
    file_size = os.path.getsize(path)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"{path.name}: file size {file_size // (1024 * 1024)}MB exceeds 50MB limit."
        )

    # Single pdfplumber.open() — do NOT re-open (see PATTERNS.md anti-patterns).
    # unicode_norm="NFKC" expands FB-block ligatures (U+FB00–U+FB06) at parse time
    # (EXTRACT-03). Confirmed supported by pdfplumber 0.11.9 (Wave 1 SUMMARY.md).
    with pdfplumber.open(str(path), unicode_norm="NFKC") as pdf:
        page_count = len(pdf.pages)

        # EXTRACT-02: fail-fast on image-only PDFs — check BEFORE extract_text() calls
        # (RESEARCH.md Pitfall 3). Summing .chars and .images is lazy/metadata only.
        total_chars = sum(len(p.chars) for p in pdf.pages)
        total_images = sum(len(p.images) for p in pdf.pages)

        if total_chars == 0 and total_images > 0:
            raise ImageOnlyPDFError(
                f"{path.name}: PDF appears to be image-only (scanned). "
                "No extractable text found. Please use a text-based PDF."
            )
        if total_chars == 0 and total_images == 0:
            raise EmptyPDFError(
                f"{path.name}: PDF contains no text or images."
            )

        # Collect chars and text from all pages in ONE pass (RESEARCH.md Pitfall 4).
        all_chars: list[dict] = []
        page_texts: list[str] = []
        page_width: float = pdf.pages[0].width
        page_height: float = pdf.pages[0].height
        for page in pdf.pages:
            all_chars.extend(page.chars)
            page_texts.append(page.extract_text() or "")

    raw_text = "\n".join(page_texts)
    # Note: unicode_norm="NFKC" at open time handles ligature normalization (EXTRACT-03).
    # If pdfplumber raises TypeError on the unicode_norm kwarg (older versions), apply manually:
    #   raw_text = unicodedata.normalize("NFKC", raw_text)
    # (chars list text fields would remain unnormalized in that fallback case.)
    # pdfplumber 0.11.9 supports this kwarg directly — no fallback needed here.

    # EXTRACT-04: multi-column detection using body chars (excludes header region).
    is_multi_column = _detect_multicolumn(all_chars, page_width, page_height)

    # EXTRACT-05 + EXTRACT-06: single-pass section segmentation + bullet extraction.
    sections, bullets = _extract_sections_and_bullets(raw_text)

    return ParsedResume(
        raw_text=raw_text,
        sections=sections,
        bullets=bullets,
        chars=all_chars,
        meta={"is_multi_column": is_multi_column, "page_count": page_count},
        source_path=str(path),
    )
