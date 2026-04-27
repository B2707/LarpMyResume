# LarpMyResume

![Python CI](https://github.com/B2707/LarpMyResume/actions/workflows/python-ci.yml/badge.svg)
![Ruby CI](https://github.com/B2707/LarpMyResume/actions/workflows/ruby-ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)

**Rule-based, offline resume auditor for ATS compatibility and keyword matching.**

No API keys. No LLMs. No external services. Runs in seconds.

LarpMyResume audits your resume PDF for ATS parse reliability, scores your bullet points against an evidence-graded rubric, and compares your skills against any job description — entirely offline, entirely deterministically.

---

## The Research Behind It

The scoring rules, thresholds, and flags in this tool are grounded in peer-reviewed research on recruiter behavior, ATS parsing, and candidate screening — not convention or guesswork.

See **[RESEARCH.md](RESEARCH.md)** for the full evidence base: a synthesis of ATS vendor documentation, eye-tracking studies, hiring outcome research, and legal guidance on Canadian and US hiring practices. If you disagree with a rule, that's where to look — and where to open a PR if you have better evidence.

---

## What It Checks

**ATS compatibility (`scan`)**
- Multi-column layout detection (column-gap heuristic using character x-positions)
- Non-standard section headings that ATS systems fail to classify
- Tables, text boxes, and graphics that break parser output
- Critical information in headers/footers
- Image-only PDFs (scanned resumes with no extractable text)

**Bullet quality (`scan`)**
- Weak opening verbs and passive phrasing
- Missing or vague metrics
- Anti-AI detection flags (generic, filler, or suspiciously polished language)
- Per-bullet scores with specific improvement flags

**Keyword matching (`match`)**
- 300+ skill gazetteer across languages, frameworks, infra, and tools
- Three-tier output: strong matches, weak/partial matches, and gaps
- Short-skill disambiguation (distinguishes "Go" from prose, "R" from sentences)
- Works against a URL or a local text file — no internet required for `--job-text`

---

## Install

### Python CLI

```bash
pip install larp-my-resume
```

### Ruby Report Generator (optional — for HTML reports)

```bash
gem install larp-my-resume-report
```

---

## Usage

**ATS audit — scan your resume:**

```bash
larp-my-resume scan resume.pdf
```

**Keyword match against a job posting URL:**

```bash
larp-my-resume match resume.pdf --job-url "https://jobs.example.com/posting"
```

**Keyword match against a local job description:**

```bash
larp-my-resume match resume.pdf --job-text job.txt
```

**Full pipeline — JSON output piped to an HTML report:**

```bash
larp-my-resume match resume.pdf --job-url "https://jobs.example.com/posting" --json \
  | larp-my-resume-report --out report.html
```

**JSON output (for scripting or piping):**

```bash
larp-my-resume --json scan resume.pdf
larp-my-resume --json match resume.pdf --job-text job.txt
```

---

## How It Works

`pdfplumber` extracts character-level text from your resume PDF. A column-detection heuristic clusters character x-positions to flag multi-column layouts. Rule-based analyzers run against the extracted text:

- **ATS checker** — regex patterns and structural heuristics against known ATS failure modes
- **Bullet scorer** — verb lists, metric patterns, and flag rules derived from the research in `RESEARCH.md`
- **Keyword matcher** — a curated skill gazetteer with short-token disambiguation and importance weighting

The Ruby gem (`larp-my-resume-report`) reads the JSON output and renders a self-contained HTML report with inline CSS — no JavaScript, no external resources.

---

## Development

```bash
# Python
pip install -e .
pytest

# Ruby gem
cd ruby && bundle install && bundle exec rspec

# Generate test fixture PDFs
python tests/fixtures/generate_fixtures.py
```

Tests require no network access and no API keys. All test fixtures are programmatically generated.

---

## Contributing

MIT licensed — issues and PRs welcome.

Open an issue before submitting large changes: [github.com/B2707/LarpMyResume/issues](https://github.com/B2707/LarpMyResume/issues)

If you have better evidence for any scoring rule, the right place to start is [RESEARCH.md](RESEARCH.md).

---

## License

[MIT](LICENSE) — © 2026 Bader Asadi
