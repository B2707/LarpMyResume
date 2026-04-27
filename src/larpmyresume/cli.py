from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import rich.box
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import httpx
import larpmyresume
from larpmyresume.analyzers import ats_checker
from larpmyresume.analyzers import bullet_scorer
from larpmyresume.analyzers import keyword_matcher
from larpmyresume.analyzers.ats_checker import ATSResult
from larpmyresume.analyzers.bullet_scorer import BulletScorerResult
from larpmyresume.extractor import EmptyPDFError, ImageOnlyPDFError, ParsedResume, extract
from larpmyresume.scraper import (
    WORKDAY_RE,
    JSRenderedError,
    LinkedInBlockedError,
    ScraperHTTPError,
    fetch_jd_text,
)

# ---------------------------------------------------------------------------
# Named constants
# ---------------------------------------------------------------------------

EXIT_OK: int = 0
EXIT_ERR: int = 1

# Score weights (D-02, D-03)
ATS_WEIGHT_WITH_KW: float = 0.30
BULLET_WEIGHT_WITH_KW: float = 0.40
KW_WEIGHT: float = 0.30
ATS_WEIGHT_SCAN_ONLY: float = 0.43
BULLET_WEIGHT_SCAN_ONLY: float = 0.57


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

@dataclass
class State:
    json_mode: bool = False


# ---------------------------------------------------------------------------
# Version callback
# ---------------------------------------------------------------------------

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"larp-my-resume {larpmyresume.__version__}")
        raise typer.Exit(EXIT_OK)


# ---------------------------------------------------------------------------
# Typer app
# ---------------------------------------------------------------------------

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    invoke_without_command=True,
)


@app.callback()
def main(
    ctx: typer.Context,
    json_mode: bool = typer.Option(
        False,
        "--json",
        help="Write raw JSON to stdout. All diagnostics go to stderr.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show installed version and exit.",
    ),
) -> None:
    """[bold]larp-my-resume[/bold] — deterministic resume auditor for ATS and keyword matching."""
    ctx.ensure_object(State)
    if ctx.invoked_subcommand is None:
        return
    ctx.obj = State(json_mode=bool(json_mode))


# ---------------------------------------------------------------------------
# JSON schema builder
# ---------------------------------------------------------------------------

def _make_scan_json(
    resume_path: str,
    parsed: ParsedResume | None = None,
    ats_result: ATSResult | None = None,
    bullet_result: BulletScorerResult | None = None,
    kw_result=None,  # KeywordMatchResult | None
) -> dict:
    """Build the scan JSON payload. Null fields signal 'not yet computed'."""
    score_breakdown: dict | None = None
    overall_score: int | None = None

    if ats_result is not None and bullet_result is not None:
        ats_score: int = ats_result.section_score
        bullet_score: float = bullet_result.summary()["avg_score"]

        if kw_result is not None:
            total_kw = len(kw_result.hits) + len(kw_result.weak) + len(kw_result.missing)
            kw_score: float = (
                (len(kw_result.hits) * 100 + len(kw_result.weak) * 50) / total_kw
                if total_kw
                else 0.0
            )
            overall_score = round(
                ats_score * ATS_WEIGHT_WITH_KW
                + bullet_score * BULLET_WEIGHT_WITH_KW
                + kw_score * KW_WEIGHT
            )
            score_breakdown = {
                "ats_score": ats_score,
                "bullet_score": bullet_score,
                "keyword_score": round(kw_score, 1),
                "overall_score": overall_score,
            }
        else:
            # D-03: scan-only — normalize weights (no keyword component)
            overall_score = round(
                ats_score * ATS_WEIGHT_SCAN_ONLY + bullet_score * BULLET_WEIGHT_SCAN_ONLY
            )
            score_breakdown = {
                "ats_score": ats_score,
                "bullet_score": bullet_score,
                "keyword_score": None,
                "overall_score": overall_score,
            }

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "resume_file": resume_path,
        "job_url": None,
        "overall_score": overall_score,
        "sections": {k: list(v) for k, v in parsed.sections.items()} if parsed else {},
        "ats_flags": [dataclasses.asdict(f) for f in ats_result.flags] if ats_result is not None else None,
        "ats_section_score": ats_result.section_score if ats_result is not None else None,
        "bullets": (
            [dataclasses.asdict(r) for r in bullet_result.results]
            if bullet_result is not None
            else None
        ),
        "bullets_summary": bullet_result.summary() if bullet_result is not None else None,
        "keyword_match": None,  # key MUST exist to prevent Ruby KeyError (SCHEMA-04)
        "score_breakdown": score_breakdown,
    }


# ---------------------------------------------------------------------------
# scan command
# ---------------------------------------------------------------------------

@app.command()
def scan(
    ctx: typer.Context,
    resume: str = typer.Argument(..., help="Path to resume PDF."),
) -> None:
    """[bold]Scan[/bold] a resume for ATS compatibility and bullet quality."""
    state: State = ctx.obj or State()
    path = Path(resume)

    if not path.exists():
        typer.secho(f"Error: file not found: {resume}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=EXIT_ERR)

    try:
        parsed = extract(path)
    except ImageOnlyPDFError:
        typer.secho(
            "Error: PDF is image-only — no extractable text. Use a text-based PDF.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=EXIT_ERR)
    except EmptyPDFError:
        typer.secho("Error: PDF is empty or corrupt.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=EXIT_ERR)

    ats_result = ats_checker.check(parsed)
    bullet_result = bullet_scorer.check(parsed)

    if state.json_mode:
        typer.echo(json.dumps(_make_scan_json(resume, parsed, ats_result, bullet_result)))
    else:
        console = Console()
        score = ats_result.section_score
        if score >= 70:
            score_markup = f"[green]Section Score: {score}/100[/green]"
        elif score >= 50:
            score_markup = f"[yellow]Section Score: {score}/100[/yellow]"
        else:
            score_markup = f"[red]Section Score: {score}/100[/red]"

        console.print(Panel(
            score_markup,
            title=f"[bold]ATS Report — {path.name}[/bold]",
            subtitle="larp-my-resume",
        ))

        if not ats_result.flags:
            console.print("[green]No ATS issues detected.[/green]")
        else:
            table = Table(box=rich.box.SIMPLE, show_header=True, header_style="bold")
            table.add_column("Severity", width=10)
            table.add_column("Flag", width=35)
            table.add_column("Explanation")
            for flag in ats_result.flags:
                if flag.severity == "High":
                    sev_markup = "[red]High[/red]"
                elif flag.severity == "Medium":
                    sev_markup = "[yellow]Medium[/yellow]"
                else:
                    sev_markup = "[green]Low[/green]"
                table.add_row(sev_markup, flag.flag, flag.explanation)
            console.print(table)

        # --- Bullet Analysis section ---
        bsummary = bullet_result.summary()
        n_bullets = bsummary["total"]
        avg_score = bsummary["avg_score"]
        flagged_count = bsummary["flagged_count"]
        console.print(Panel(
            f"[bold]{n_bullets}[/bold] bullets — avg score [bold]{avg_score}[/bold] — "
            f"[bold]{flagged_count}[/bold] flagged",
            title="[bold]Bullet Analysis[/bold]",
        ))

        if bullet_result.results:
            bullet_table = Table(box=rich.box.SIMPLE, show_header=True, header_style="bold")
            bullet_table.add_column("Score", min_width=5, justify="right", no_wrap=True)
            bullet_table.add_column("Bullet", ratio=1)
            bullet_table.add_column("wk_verb", min_width=7, no_wrap=True)
            bullet_table.add_column("no_outc", min_width=7, no_wrap=True)
            bullet_table.add_column("passive", min_width=7, no_wrap=True)
            bullet_table.add_column("too_lng", min_width=7, no_wrap=True)

            sorted_results = sorted(bullet_result.results, key=lambda r: r.score)
            for r in sorted_results:
                if r.score >= 70:
                    score_col = f"[bold green]{r.score}[/bold green]"
                elif r.score >= 50:
                    score_col = f"[bold yellow]{r.score}[/bold yellow]"
                else:
                    score_col = f"[bold red]{r.score}[/bold red]"

                display_text = r.text[:70] + "…" if len(r.text) > 70 else r.text

                wv = "[red]✗[/red]" if "weak_verb" in r.flags else "[dim]·[/dim]"
                no = "[red]✗[/red]" if "no_outcome" in r.flags else "[dim]·[/dim]"
                pv = "[red]✗[/red]" if "passive_voice" in r.flags else "[dim]·[/dim]"
                tl = "[red]✗[/red]" if "too_long" in r.flags else "[dim]·[/dim]"

                bullet_table.add_row(score_col, display_text, wv, no, pv, tl)

            console.print(bullet_table)
        else:
            console.print("[green]No bullets found in resume.[/green]")

        # --- Anti-AI Risk panel ---
        anti_ai = bullet_result.anti_ai_score
        if anti_ai <= 3:
            risk_label = "[green]Low[/green]"
        elif anti_ai <= 6:
            risk_label = "[yellow]Medium[/yellow]"
        else:
            risk_label = "[red]High[/red]"

        console.print(Panel(
            f"Anti-AI Risk: [bold]{anti_ai}/10[/bold] — {risk_label}",
            title="[bold]Anti-AI Risk[/bold]",
        ))


# ---------------------------------------------------------------------------
# match command — Phase 5 full keyword matcher pipeline
# ---------------------------------------------------------------------------

@app.command()
def match(
    ctx: typer.Context,
    resume: str = typer.Argument(..., help="Path to resume PDF."),
    job_url: Optional[str] = typer.Option(
        None, "--job-url", help="URL of job posting to scrape."
    ),
    job_text: Optional[str] = typer.Option(
        None, "--job-text", help="Job description text (fallback for blocked platforms)."
    ),
) -> None:
    """[bold]Match[/bold] a resume against a job posting for keyword gap analysis."""
    state: State = ctx.obj or State()
    path = Path(resume)

    if not path.exists():
        typer.secho(f"Error: file not found: {resume}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=EXIT_ERR)

    # Validation: need at least one JD source
    if job_url is None and job_text is None:
        typer.secho(
            "Error: provide --job-url or --job-text.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=EXIT_ERR)

    try:
        parsed = extract(path)
    except ImageOnlyPDFError:
        typer.secho(
            "Error: PDF is image-only — no extractable text.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=EXIT_ERR)
    except EmptyPDFError:
        typer.secho("Error: PDF is empty or corrupt.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=EXIT_ERR)

    # Resolve JD text: --job-text wins over --job-url
    jd_text: str
    if job_text is not None:
        jd_text = job_text
    else:
        assert job_url is not None  # validated above
        if WORKDAY_RE.search(job_url):
            typer.secho(
                "Warning: Workday URLs may be JS-rendered — use --job-text if scraping fails.",
                err=True,
            )
        try:
            jd_text = fetch_jd_text(job_url)
        except LinkedInBlockedError:
            typer.secho(
                "LinkedIn requires login — use --job-text instead.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=EXIT_ERR)
        except JSRenderedError:
            typer.secho(
                "Page appears JS-rendered or empty — use --job-text.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=EXIT_ERR)
        except httpx.TimeoutException:
            typer.secho(
                "Request timed out — use --job-text.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=EXIT_ERR)
        except ScraperHTTPError as exc:
            typer.secho(
                f"Access denied ({exc}) — use --job-text.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=EXIT_ERR)

    ats_result = ats_checker.check(parsed)
    bullet_result = bullet_scorer.check(parsed)
    kw_result = keyword_matcher.check(parsed, jd_text)

    if state.json_mode:
        payload = _make_scan_json(resume, parsed, ats_result, bullet_result, kw_result)
        payload["job_url"] = job_url
        payload["keyword_match"] = {
            "hits": [dataclasses.asdict(h) for h in kw_result.hits],
            "weak": [dataclasses.asdict(w) for w in kw_result.weak],
            "missing": [dataclasses.asdict(m) for m in kw_result.missing],
        }
        typer.echo(json.dumps(payload))
    else:
        console = Console()

        # ATS summary panel
        score = ats_result.section_score
        if score >= 70:
            score_markup = f"[green]Section Score: {score}/100[/green]"
        elif score >= 50:
            score_markup = f"[yellow]Section Score: {score}/100[/yellow]"
        else:
            score_markup = f"[red]Section Score: {score}/100[/red]"
        console.print(Panel(
            score_markup,
            title=f"[bold]ATS Report — {path.name}[/bold]",
            subtitle="larp-my-resume",
        ))

        # Bullet summary panel
        bsummary = bullet_result.summary()
        console.print(Panel(
            f"[bold]{bsummary['total']}[/bold] bullets — "
            f"avg score [bold]{bsummary['avg_score']}[/bold] — "
            f"[bold]{bsummary['flagged_count']}[/bold] flagged",
            title="[bold]Bullet Analysis[/bold]",
        ))

        # Keyword gap table
        # Sort order: MISS-required, WEAK-required, WEAK-preferred, MISS-preferred, HITs last
        sorted_entries = (
            [(m, "MISS") for m in kw_result.missing if m.importance == "required"] +
            [(m, "WEAK") for m in kw_result.weak if m.importance == "required"] +
            [(m, "WEAK") for m in kw_result.weak if m.importance == "preferred"] +
            [(m, "MISS") for m in kw_result.missing if m.importance == "preferred"] +
            [(m, "HIT")  for m in kw_result.hits]
        )

        console.print(Panel(
            f"[bold]{len(kw_result.hits)}[/bold] hits  "
            f"[bold]{len(kw_result.weak)}[/bold] weak  "
            f"[bold]{len(kw_result.missing)}[/bold] missing",
            title="[bold]Keyword Gap Report[/bold]",
        ))

        if sorted_entries:
            kw_table = Table(box=rich.box.SIMPLE, show_header=True, header_style="bold")
            kw_table.add_column("Tier", width=8)
            kw_table.add_column("Skill", width=25)
            kw_table.add_column("Importance", width=12)

            for match_obj, tier in sorted_entries:
                if tier == "HIT":
                    tier_markup = "[green]HIT[/green]"
                elif tier == "WEAK":
                    tier_markup = "[yellow]WEAK[/yellow]"
                else:
                    tier_markup = "[red]MISS[/red]"
                imp = match_obj.importance.capitalize()
                kw_table.add_row(tier_markup, match_obj.skill, imp)

            console.print(kw_table)
