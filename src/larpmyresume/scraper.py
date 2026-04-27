"""Job description scraper — httpx + BeautifulSoup4, no LLM calls."""
from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup

USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
SHORT_CONTENT_THRESHOLD: int = 200

LINKEDIN_RE = re.compile(r"linkedin\.com/(in|jobs)/", re.IGNORECASE)
WORKDAY_RE = re.compile(r"\.(workday|myworkdayjobs)\.com", re.IGNORECASE)

SELECTOR_CHAIN: list[str] = [
    "div#app_body",
    "div.job__description",
    "div[data-qa='job-description']",
    "div.section-wrapper",
    "article",
    "main",
]


class LinkedInBlockedError(ValueError):
    """LinkedIn URLs are unconditionally blocked — use --job-text."""


class JSRenderedError(ValueError):
    """Page content too short — likely JS-rendered or login-gated."""


class ScraperHTTPError(ValueError):
    """HTTP error response (403/429/etc) from job posting URL."""


def fetch_jd_text(url: str, *, transport: httpx.BaseTransport | None = None) -> str:
    """Fetch and extract job description text from a URL.

    Args:
        url: Job posting URL.
        transport: Optional MockTransport for testing. Real HTTP if None.

    Returns:
        Extracted job description as plain text.

    Raises:
        LinkedInBlockedError: URL is a LinkedIn job/profile URL.
        JSRenderedError: Page content is < SHORT_CONTENT_THRESHOLD chars.
        ScraperHTTPError: Server returned 403/429 response.
        httpx.TimeoutException: Request timed out.
    """
    # LinkedIn check FIRST — before any HTTP call
    if LINKEDIN_RE.search(url):
        raise LinkedInBlockedError(url)

    client_kwargs: dict = {
        "follow_redirects": True,          # CRITICAL: httpx default is False
        "timeout": httpx.Timeout(10.0),
        "headers": {"User-Agent": USER_AGENT},
    }
    if transport is not None:
        client_kwargs["transport"] = transport

    with httpx.Client(**client_kwargs) as client:
        response = client.get(url)

    if response.status_code in (403, 429):
        raise ScraperHTTPError(f"HTTP {response.status_code}")

    response.raise_for_status()

    text = _extract_text(response.text)
    if len(text) < SHORT_CONTENT_THRESHOLD:
        raise JSRenderedError(f"Content too short ({len(text)} chars)")

    return text


def _make_soup(html: str) -> BeautifulSoup:
    """Parse HTML with lxml if available, falling back to html.parser.

    lxml binary wheels may be absent on some platforms (arm64 macOS, certain CI
    images). Using html.parser as a fallback avoids an unhandled FeatureNotFound
    exception that would produce an unformatted traceback instead of a clean error.
    """
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:  # bs4.FeatureNotFound — avoid importing bs4 internals
        return BeautifulSoup(html, "html.parser")


def _extract_text(html: str) -> str:
    """Extract plain text from HTML using a CSS selector chain with fallback."""
    soup = _make_soup(html)
    for selector in SELECTOR_CHAIN:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator=" ", strip=True)
            if len(text) >= SHORT_CONTENT_THRESHOLD:
                return text
    containers = soup.find_all(["div", "article", "main", "section"])
    if containers:
        biggest = max(containers, key=lambda el: len(el.get_text(strip=True)))
        return biggest.get_text(separator=" ", strip=True)
    return soup.get_text(separator=" ", strip=True)
