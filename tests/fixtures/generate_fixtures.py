from __future__ import annotations

import base64
import io
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

FIXTURES = Path(__file__).parent

# Minimal 1x1 gray PNG (no text, ensures page.chars == [])
MINIMAL_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9Q"
    "DwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


def make_two_column_pdf(path: Path) -> None:
    """Two text columns at x=36 (left) and x=324 (right). gap_ratio ~0.47 >> 0.20.

    Content is placed in the body region (below top 20% of page = y < 633.6) to
    ensure _detect_multicolumn's HEADER_EXCLUSION_RATIO filter does not exclude it.
    reportlab uses bottom-left origin; pdfplumber uses top-left origin.
    LETTER page is 612 x 792 pts. Body starts below top 20% = below top 158.4 pts.
    reportlab y-equivalent: h - 158.4 = 633.6. We start at h - 200 = 592 (safely in body).
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    w, h = LETTER  # 612 x 792

    # Name/header in top region (above body line — will be excluded by header filter)
    c.drawString(180, h - 72, "Jane Doe - Software Engineer")

    # Left column — EXPERIENCE section with bullets (starts at y=592, safely in body)
    c.drawString(36, h - 200, "EXPERIENCE")
    c.drawString(36, h - 218, "- Built REST API with Python and FastAPI")
    c.drawString(36, h - 236, "  serving production traffic at scale")
    c.drawString(36, h - 254, "- Implemented OAuth2 token refresh flow")
    c.drawString(36, h - 272, "- Reduced latency by 40 percent")
    c.drawString(36, h - 290, "- Led migration to Kubernetes")
    c.drawString(36, h - 308, "- Designed microservices architecture")
    c.drawString(36, h - 326, "- Wrote unit and integration tests")

    # Right column — SKILLS section (gap from left ~288pt, safely two-column)
    c.drawString(324, h - 200, "SKILLS")
    c.drawString(324, h - 218, "Python, Java, JavaScript")
    c.drawString(324, h - 236, "PostgreSQL, Redis, Docker")
    c.drawString(324, h - 254, "Git, Linux, AWS")
    c.drawString(324, h - 272, "FastAPI, Django, Flask")
    c.drawString(324, h - 290, "React, Node.js, TypeScript")
    c.drawString(324, h - 308, "Kubernetes, Terraform")
    c.drawString(324, h - 326, "pytest, RSpec, JUnit")

    c.showPage()
    c.save()


def make_image_only_pdf(path: Path) -> None:
    """Image fills page. No drawString calls — ensures page.chars == []."""
    c = canvas.Canvas(str(path), pagesize=LETTER)
    w, h = LETTER
    img_bytes = base64.b64decode(MINIMAL_PNG_B64)
    img = ImageReader(io.BytesIO(img_bytes))
    c.drawImage(img, 36, 36, width=540, height=720)
    c.showPage()
    c.save()


def make_single_column_pdf(path: Path) -> None:
    """Single-column resume fixture. All text at x=72 — gap_ratio << 0.20.

    Used as the 'real resume' test fixture. Contains sections and bullet points
    so extraction, ATS, bullet-scorer, and keyword-matcher tests all pass.
    No ligatures (plain ASCII only).
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    w, h = LETTER  # 612 x 792
    x = 72
    y = h - 72

    def line(text: str, bold: bool = False, size: int = 11) -> None:
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, text)
        y -= size + 4

    def gap(n: int = 8) -> None:
        nonlocal y
        y -= n

    line("Alex Chen", bold=True, size=14)
    line("alex.chen@example.com | github.com/alexchen | linkedin.com/in/alexchen")
    gap()

    line("EDUCATION", bold=True)
    line("University of Waterloo — Bachelor of Computer Science, 2025")
    line("GPA: 3.7/4.0 | Dean's Honour List")
    gap()

    line("EXPERIENCE", bold=True)
    line("Software Engineering Intern — Stripe (May 2024 – Aug 2024)")
    line("- Reduced payment processing latency by 32 percent by refactoring")
    line("  the retry logic in the charge settlement service using Python and Redis.")
    line("- Built an internal CLI tool adopted by 12 engineers to automate")
    line("  daily deployment rollbacks, cutting mean recovery time by 18 minutes.")
    line("- Wrote 47 new unit and integration tests, raising branch coverage")
    line("  from 71 percent to 89 percent on the billing module.")
    gap()
    line("Software Engineering Intern — Shopify (Jan 2024 – Apr 2024)")
    line("- Migrated three legacy Ruby on Rails endpoints to GraphQL,")
    line("  reducing average API response size by 41 percent.")
    line("- Implemented rate-limiting middleware in Go for the storefront API,")
    line("  handling 50 000 requests per second under peak load.")
    line("- Collaborated with the platform team to containerize two services")
    line("  using Docker and Kubernetes, enabling zero-downtime deploys.")
    gap()

    line("PROJECTS", bold=True)
    line("LarpMyResume (open source) — github.com/B2707/LarpMyResume")
    line("- Rule-based CLI tool that audits resumes for ATS compatibility")
    line("  and keyword matching against job descriptions. Python + Ruby.")
    line("- 131 tests, GitHub Actions CI, pip-installable.")
    gap()
    line("Distributed Key-Value Store — github.com/alexchen/kvstore")
    line("- Implemented Raft consensus in Go; benchmarked at 12 000 ops/sec.")
    line("- Deployed to AWS EC2 with Terraform; automated with GitHub Actions.")
    gap()

    line("SKILLS", bold=True)
    line("Languages: Python, Go, Ruby, Java, JavaScript, TypeScript, SQL")
    line("Frameworks: FastAPI, Django, Rails, React, Node.js")
    line("Infrastructure: AWS, Docker, Kubernetes, Terraform, Linux")
    line("Databases: PostgreSQL, Redis, MySQL, DynamoDB")
    line("Tools: Git, pytest, RSpec, GitHub Actions, Grafana, DataDog")

    c.showPage()
    c.save()


if __name__ == "__main__":
    make_two_column_pdf(FIXTURES / "two_column.pdf")
    make_image_only_pdf(FIXTURES / "image_only.pdf")
    make_single_column_pdf(FIXTURES / "real_resume.pdf")
    print("Fixtures generated:")
    print(f"  {FIXTURES / 'two_column.pdf'}")
    print(f"  {FIXTURES / 'image_only.pdf'}")
    print(f"  {FIXTURES / 'real_resume.pdf'}")
