# Resume Optimization Research

> This document is the evidence base behind LarpMyResume's scoring rules. Every flag, threshold, and rubric in the tool traces back to a claim in this research. If you disagree with a rule, this is where to look for the reasoning — and where to open a PR if you have better evidence.

---

# Evidence-Based Tech Resume Research Dossier (v2)
## For CS Students Applying to Internships and Entry-Level Roles in Canada and the United States

**Document purpose:** A unified, evidence-graded research synthesis compiled from four independent research passes and reconciled for consistency. Where sources disagreed, the safest evidence-backed default is presented and the conflict is noted.

**Version 2 changelog (vs v1):**
- **GPA threshold rule** is now evidence-anchored to NACE Job Outlook 2023's reported median screening cutoff of ~3.0/4.0, not the unevidenced "3.5+" convention
- **Typography recommendation** for serif vs sans-serif has been refined: the previously simplified "no inherent difference" claim now carries a screen/small-size caveat from Richardson (2022) that matters for resume reading
- **Typography monograph citation** has been verified and replaced (Richardson 2022, Springer Open Access)
- **Cover letter section** now includes Google's explicit "cover letter optional" guidance as a Tier 3 data point
- **Bullet count guidance** has been explicitly relabeled as convention rather than evidence
- **GitHub link guidance** has been refined with the Abou El-Komboz & Goldbeck (2024) signaling working paper
- **Open Questions section** has been updated to remove resolved gaps and add new ones

**Core research question (restated):** How can a 4th-year Computer Science student build the strongest possible modern tech resume — optimized first for ATS parse reliability and then for fast human screening and persuasion — when applying broadly to internships and entry-level roles in Canada and the United States?

---

## 1. Executive Summary

The strongest evidence supports a **dual-optimization strategy**: maximize machine-parse reliability and structured-field extraction first, then maximize fast human scanning efficiency and credibility signals. These are not in tension when done correctly — both favor simple, single-column layouts with strong typographic hierarchy and specific, evidence-backed content.

### The seven highest-confidence findings

1. **Initial screening is fast and pattern-driven.** Industry eye-tracking reports place initial review in the 6–8 second range (TheLadders 2012, 2018), and US federal hiring guidance asks whether main credentials are visible within 10–15 seconds. Recruiters scan along the left margin, anchor on job titles and section headers, and penalize clutter. Practical implication: the top quarter of page one must communicate role fit + strongest evidence + core skills immediately.

2. **Compositional quality (detail, clarity, structure) predicts student job-search outcomes.** A 2025 peer-reviewed study tracking Canadian co-op students found that resume and cover letter compositional quality predicted more interviews per application and faster job acquisition, controlling for experience and tailoring (Wingate, Robie, Powell & Bourdage 2025, *International Journal of Selection and Assessment*). This is the single strongest piece of Tier 1 evidence in the entire corpus and applies directly to the target candidate profile.

3. **Internships are the top differentiator when candidates are otherwise equal; the median GPA screening cutoff is ~3.0.** NACE Job Outlook 2023 reports a median GPA cutoff of approximately 3.0/4.0 across industries, regions, and company sizes among employers that screen by GPA. Practical implication: GPA is not a primary differentiator; concrete experience and proof of shipping are. Include GPA on the resume only if it meets typical screening thresholds (~3.0/4.0) or is explicitly requested.

4. **ATS and parsing vendors uniformly warn against multi-column layouts, tables, text boxes, graphics, and headers/footers containing critical information.** Textkernel, Sovren, Bullhorn, and Greenhouse all flag these as parse-breaking risks that can drop or scramble titles, dates, and employer names — exactly the structured fields recruiters search and filter on.

5. **PDF vs DOCX is a portal-dependent risk-management decision, not a religious rule.** Modern ATS commonly accept both. The safest operational approach is to maintain both exports of the same ATS-safe layout, follow upload instructions when given, and prefer DOCX when the application flow obviously relies on parse-to-form mapping.

6. **Projects can compensate for limited internship volume — but only when they carry credible proof signals.** Peer-reviewed software-hiring research (Kuttal et al. 2021) shows evaluators use online contribution traces but rely heavily on low-effort surface signals (READMEs, deployment links, test presence) rather than deep code inspection. Projects without proof signals are discounted.

7. **"Canadian experience" as a hiring requirement is now legally restricted in Ontario, not just policy-discouraged.** Ontario's 2023 legislative announcement became operational law in 2026, prohibiting Canadian-experience requirements in covered publicly advertised job postings, and adding a new requirement that employers disclose AI screening use. International technical experience should be presented with comparability signals (standard role titles, mainstream stack, scope, outcomes), not downplayed.

### Bottom-line safe default for this candidate profile

Single-column layout, standard section headings, body font 11pt with margins at 0.75", clear bolded job titles and dates, a concise role-aligned skills section, high-quality bullets emphasizing ownership plus technical specificity plus credible proof, projects that look like real engineering (deployed, tested, documented), and tight alignment across the resume, LinkedIn, and GitHub.

---

## 2. Evidence Framework

### Evidence tiers used in this dossier

| Tier | What counts | Weight in decisions |
|---|---|---|
| **Tier 1** | Peer-reviewed empirical research directly studying resume/CV screening, recruiter behavior, or measurable job-search outcomes | Can justify defaults; can overturn convention |
| **Tier 2** | Peer-reviewed HCI / readability / typography / scanning research that generalizes to resume contexts; large-scale hiring research and surveys with explicit methods (e.g., NACE, Harvard "Hidden Workers") | Strong priors for what matters |
| **Tier 3** | Primary ATS/parser vendor documentation, official government hiring guidance, legal/human-rights guidance | Defines safe constraints; resolves parsing myths |
| **Tier 4** | Reputable university career center guidance | Practical conventions; conservative safe defaults |
| **Tier 5** | Industry surveys, working papers, and practitioner reports | Used cautiously; only when higher tiers are absent |

### Confidence ratings used

- **High confidence:** Two or more aligned Tier 1–2 sources, or one Tier 1 source plus multiple Tier 3–4 sources agreeing on the same operational recommendation.
- **Medium confidence:** Tier 3–4 sources agree but Tier 1 evidence is absent or indirect (common for resume formatting minutiae).
- **Low confidence / `[insufficient data]`:** Sources conflict without a strong Tier 1/2 anchor, advice is platform-specific, or the question is convention-bound rather than evidence-bound.

### Conflict-handling rule

When sources disagree, this dossier defaults to the **lowest-risk option that preserves both ATS safety and human readability**, and converts the disagreement into an explicit decision rule. Disagreements were most common around PDF vs DOCX, summary section value, and resume length.

### Fact / interpretation / inference separation

Throughout this document, claims are labeled:
- **Fact** — directly supported by a cited source
- **Interpretation** — reasoning from facts to operational implications
- **Inference** — reasoned conjecture where direct evidence is thin; flagged as `(inference)`

---

## 3. Detailed Findings by Topic (A–M)

### A. Recruiter behavior and scanning

**Facts:**
- Industry eye-tracking research (TheLadders 2012, 2018) reports an average initial screen of approximately **6 seconds (2012)** and **7.4 seconds (2018)**, with attention concentrated on six data points: name, current title/company, current dates, previous title/company, previous dates, and education. These reports describe instrumented eye-tracking methodology but are not peer-reviewed and are produced by a commercial career-services entity.
- Peer-reviewed eye-tracking research on CS resumes (Pina et al. 2023, *Machine Learning and Knowledge Extraction*) finds that **time spent in Experience and Education regions correlates with pass decisions** and that machine learning models can predict recruiter approval from gaze patterns.
- A peer-reviewed eye-tracking + dialog study with real recruiters (Törngren et al. 2024, *Frontiers in Sociology*) shows attention allocation differs across CV regions and that manipulated identity signals affect evaluation.
- US federal hiring guidance (USAJOBS) explicitly asks reviewers whether main credentials are visible within **10–15 seconds** and whether the **top quarter** of page one effectively "sells" the candidate.
- Foundational web-reading eye-tracking research (Nielsen Norman Group, 2006/updated) establishes the **F-shaped scanning pattern** — two horizontal sweeps followed by a vertical sweep down the left side. This generalizes to scan-based reading under time pressure.

**Interpretation:**
Resume design must support a two-stage read: (1) a sub-15-second eligibility scan anchored on titles, employers, dates, and section headers; (2) a deeper read where bullets and technical specificity matter. The "6 second" figure should be treated as a **design constraint** rather than a literal universal — but the design implication is the same regardless of which number is right.

**Differences across reviewer types** (`[insufficient data]` for clean experimental separation, but plausible patterns):
- **Technical recruiters** anchor on titles, tech keywords, and relevant experience. They penalize cluttered layouts, keyword stuffing, and unclear titles/dates.
- **Non-technical recruiters / HR generalists** rely more on chronology, education, and locations/eligibility cues. They get stuck on unexplained jargon and unclear ownership.
- **Hiring managers** look for evidence of capability to deliver on team needs. They engage longer when the resume passes the first scan, but penalize vague bullets and inflated claims.
- **Engineers / technical interviewers** look for proof artifacts (GitHub, projects), depth cues, and technical nouns. They penalize buzzword-only content and contradictions between resume claims and linked profiles.

**Differences across employer types:**
- **Big tech / large enterprise:** High ATS prevalence, structured filtering, and high application volume. Conservative formatting and keyword alignment matter more.
- **Startups:** May value shipped projects and visible work; faster, more informal screening. Still use ATS platforms — keep ATS-safe formatting as default.
- **Mid-size tech:** `[insufficient data]` for clean differences from the above two; treat as a blend.
- **Banks / telecom / enterprise:** Heavily ATS-driven, role-match and compliance-focused workflows. Conservative formatting and aligned keywords are safest.
- **Government / public sector:** Distinct rules. US federal resumes have specific content requirements (often longer, with detailed responsibilities and hours worked) per USAJOBS guidance. Do not assume private-sector norms apply.

**Risks and exceptions:**
- The "6 second" and "7.4 second" figures come from a single commercial entity and may overgeneralize. Peer-reviewed work cites timing ranges as wide as 30 seconds to 3 minutes in some contexts.
- Recruiter behavior varies with applicant volume; under high volume, recruiters rely more on filters and structured fields than close reading.

---

### B. ATS and parsing

**Facts:**
- Resume parsing vendors (Textkernel, Sovren, Bullhorn) and ATS platforms (Greenhouse, Workday) commonly accept multiple formats including PDF, DOCX, DOC, RTF, and TXT.
- Textkernel's parser documentation explicitly identifies **column resumes as a common difficulty requiring special extraction handling**, and warns that complex formatting can break linear extraction.
- Sovren's vendor guide *Tips for Electronic Resumes* (2017) provides strong guidance against tables, columns, headers/footers, and graphics — though its absolute "never use PDF" claim is **outdated** and conflicts with modern vendor acceptance (see Corrections section).
- Bullhorn's parsing documentation states that highly formatted resumes may parse poorly or omit crucial information.
- Workday's institutional documentation describes resume parsing into application form fields and notes that complex/academic resumes can be problematic for parsing workflows.
- A US federal hiring guide (USAJOBS) explicitly recommends uploading as PDF to maintain formatting and accepts multiple file types.

**Interpretation:**
ATS safety is not just about "getting past a bot." It's about **ensuring titles, dates, employers, and skills become structured searchable data** that recruiters use for filtering and search. Parse failures cause missing fields, which reduces discoverability.

**Risk classification of formatting decisions:**

| Risk level | Decisions |
|---|---|
| **Low risk** | Single column, standard section headings ("Experience", "Education", "Projects", "Skills"), text-based PDF or DOCX, common system fonts, standard bullet characters, contact info in main body |
| **Medium risk** | Plain horizontal lines, very mild color (e.g., navy headers), clickable hyperlinks, custom but mainstream font (e.g., Calibri, Garamond) |
| **High risk** | Multi-column layouts, tables for layout, text boxes, graphics/icons/logos, skill bars/star ratings, header/footer regions containing critical info, fancy bullet characters, decorative section headings, color-coded meaning |

**PDF vs DOCX — reconciled:**
- **Both formats are accepted by modern major ATS.** The "PDF always fails" myth is unsupported.
- Some institutional ATS guidance prefers DOCX for parse-to-form mapping; some prefers PDF for layout fidelity. Evidence is genuinely mixed across vendors.
- **Safest operational rule:** Maintain both exports of the same ATS-safe layout. Follow upload instructions if given. Prefer PDF for direct human emailing and for portals that don't auto-fill from parse. Prefer DOCX when the application flow clearly relies on parsing into form fields and the PDF produces incorrect mapping.

---

### C. Formatting, typography, and visual hierarchy

**Facts:**
- Multiple university career centers and government employment guides converge on body font sizes of **10–12pt** and margins of **0.5"–1.0"** for resumes (MIT CAPD, University of Toronto Mississauga, University of Michigan Engineering, Ontario Shared Services).
- One university career center (University of Victoria) specifically recommends **size 11 for content and 12–14 for headers**, and explicitly discourages underlining because it resembles hyperlinks.
- **Richardson (2022)**, *The Legibility of Serif and Sans Serif Typefaces: Reading from Paper and Reading from Screens* (Springer Open Access), reviews decades of legibility research and concludes there is **no consistent inherent legibility advantage** for serif versus sans-serif in general reading on paper or screens. **Important caveat from the same monograph:** at very small type sizes or under low luminance, serif styles can be **less legible** because the serifs themselves may become faint or invisible — a condition that applies directly to resumes read on screens at 10–11pt.
- A 2022 peer-reviewed psychophysics study (Minakata & Beier, *Acta Psychologica*) corroborates that serif vs sans effects depend on font characteristics like stroke contrast rather than the serif/sans category itself.
- A peer-reviewed eye-tracking experiment on online readability (Rello, Pielot, Marcos 2016, CHI) found that font size and line spacing meaningfully affect readability, with extreme values (very tight or very loose) impairing comprehension.
- A 2022 ACM TOCHI paper (Wallace et al.) found that font choice affects reading speed differently across individuals — there is no single best font.
- WCAG 2.2 accessibility standards (W3C) define minimum text contrast ratios of **4.5:1** for normal text against background.
- A 2022 PeerJ Computer Science paper on serif vs sans-serif e-commerce usability found context-dependent effects with no universally large differences.

**Interpretation and operational specs (synthesized safe defaults for one-page, ATS-safe, screen-first reading):**

**Font family (serif vs sans-serif):**
- On average there is no inherent legibility difference between serif and sans-serif (Richardson 2022).
- **However, for resume body text at 10–11pt read on screens — the actual use case here — sans-serif is marginally safer.** Richardson (2022) explicitly notes that at very small type sizes or under low luminance, serif strokes can become faint or invisible. This is a documented exception that applies directly to resumes.
- **Safest default:** A common system sans-serif (Arial, Calibri, Helvetica) for body text. Serif (Times New Roman, Garamond, Georgia) is acceptable but not preferred for screen-first reading at small sizes.
- Either choice should use a mainstream system font; consistency matters more than the specific family.

**Body font size:**
- Recommended range: **10.5–12 pt**
- Safest default: **11 pt**
- Use 10–10.5 only if content-heavy and still uncrowded (`inference`)
- Avoid below 10pt — increases "cram" signal and risks readability

**Heading and subheading sizes (relative to body):**
- Section headers: **+1 to +3 pt** above body (e.g., body 11 → headers 12–14)
- Name: **+2 to +4 pt** above body (e.g., body 11 → name 13–15)
- Subheadings (role/company lines): same as body, differentiated with **bold**

**Margins:**
- Recommended range: **0.5"–1.0"** all sides
- Safest default: **0.75"** all sides
- Do not go below 0.5" unless verified at print size

**Line spacing:**
- Recommended range: **1.0–1.15** for body and bullets
- Safest default: **1.0** within bullets, with explicit space added between sections
- Avoid extremes (≈0.8 too tight, ≈1.8 too loose)

**Bullet and paragraph spacing (Word "before/after" in points):**
- Within a bullet paragraph: **0–3 pt**
- Between role/project entries: **6–10 pt** (or one blank line)
- Between sections: **10–14 pt** or visual header break

**Bold / italics / underline / small caps:**
- **Bold:** Use for job titles, companies, and section headers as scan anchors. Be consistent. Recruiter eye-tracking explicitly identifies bold job titles as effective.
- **Italics:** Use sparingly for secondary metadata (location, dates, qualifiers). Avoid for long bullet text.
- **Underline:** **Avoid by default.** Underlined text resembles hyperlinks and confuses scanning (per UVic career guidance).
- **Small caps:** Avoid. Sovren parsing guidance warns against unusual text effects.

**Color:**
- Safest default: **black or near-black on white**, no color at all.
- If using color: use **one** dark, low-saturation color (e.g., navy, slate) for **name and/or section headers only**, never for bullet body text.
- Ensure contrast meets **≥4.5:1** per WCAG 2.2.
- **Never use color to encode meaning** (e.g., red/green skill levels) — ATS may drop color and the meaning is lost.

**On-screen vs printed review:**
- Most screening is digital — optimize for screen first. Maintain high contrast and avoid color-encoded meaning so the resume survives both contexts.

**Risks and exceptions:**
- These values are best-practice ranges, not experimentally proven optima. True optima vary by viewer, device, and role family. `[insufficient data]` for resume-specific causal experiments on exact point sizes.
- Extremely compact typography harms both ATS (forces layout hacks) and humans (creates clutter).

---

### D. Resume structure and section order

**Facts:**
- Eye-tracking evidence (Pina et al. 2023) shows recruiter attention concentrates on Experience and Education regions, and that time on these regions correlates with pass decisions.
- University guidance (UMich Engineering, MIT CAPD, U of T) commonly recommends one-page student resumes with sections ordered by relevance to the employer.
- NACE college hiring research indicates internship experience is the top differentiator when candidates are otherwise equal.

**Interpretation — recommended canonical order for a 4th-year CS student:**
The most robust default structure for a student applying to internships and entry-level tech roles:

1. **Header** (name, contact, links — GitHub, LinkedIn, optional portfolio)
2. **Education** (top placement for current students; keep compact)
3. **Experience** (internships, technical roles, including international)
4. **Projects** (2–4 strongest, role-aligned)
5. **Skills** (grouped, concise)
6. **Optional: Leadership / Awards / Publications** (only if signal-dense)

**When to deviate from this order:**
- **Experience before Education** if the candidate has substantial recent technical work experience that should anchor the top scan (rare for interns).
- **Projects before Experience** only if projects are materially stronger and more role-aligned than the work history.
- **Education at the top** is the default for current students because it confirms candidacy stage and is what recruiters expect to see early.

**Role-family playbooks:**

#### Software engineering / full-stack / backend / frontend
- **Section order:** Header → Education → Experience → Projects → Skills → optional Leadership/Awards
- **Emphasize:** Shipped features, APIs and services, correctness, performance, reliability, user impact, collaboration
- **Cut first if space-constrained:** Weak coursework, generic soft skills, hobby projects without proof
- **Proof signals that matter most:** Deployed demo, repo quality, tests/CI, clear README, meaningful commits/iterations, concrete job titles and dates
- **Skills grouping order:** Languages → Frameworks/Libraries → Databases → Tools/Platforms
- **Headline project example:** A deployed web app or service with real constraints — authentication, database schema, caching, monitoring/logging, tests, CI, demo link

#### Cloud / DevOps / SRE / infrastructure
- **Section order:** Header → Skills (cloud/tooling-forward) → Experience → Projects → Education → optional Certifications
- **Emphasize:** Automation, reliability, incident prevention, observability, IaC, CI/CD, security hygiene
- **Cut first:** Unrelated front-end UI detail, long narrative bullets
- **Proof signals:** IaC repo (Terraform), CI/CD pipeline example, monitoring dashboards, postmortem-style writeups, infra diagrams
- **Skills grouping order:** Cloud → IaC/CI/CD → Containers → Observability → Scripting/Languages → OS/Networking
- **Headline project example:** "Provisioned and deployed X service on Y cloud using Terraform; built CI/CD + monitoring; demonstrated rollback + cost controls"

#### IT / systems / helpdesk / support
- **Section order:** Header → Skills (platforms/tools first) → Experience → Education → Projects (only if relevant)
- **Emphasize:** Troubleshooting scope, customer communication, incident resolution, asset management, scripting automation
- **Cut first:** Deep algorithmic coursework, irrelevant SWE projects
- **Proof signals:** Clear tools list (OS, MDM, ticketing, networking), bullets demonstrating resolution outcomes
- **Skills grouping order:** OS & Admin → Networking → Support Tools → Scripting → Hardware/Cloud basics
- **Headline project example:** A small automation that saves time — scripted inventory, log parsing, account provisioning — with clear before/after workflow

#### Data / analytics / ML-adjacent
- **Section order:** Header → Skills (data stack-forward) → Projects → Experience → Education
- **Emphasize:** Data pipeline clarity, evaluation rigor, reproducibility, stakeholder framing, model/analysis limitations
- **Cut first:** Generic web-dev projects, long lists of ML buzzwords without experiments
- **Proof signals:** End-to-end runnable notebooks, dataset documentation, evaluation metrics with baselines, reproducible pipeline, honest limitations
- **Skills grouping order:** Python/R/SQL → Data libraries → BI/Viz → ML frameworks → Cloud data tools
- **Headline project example:** "Built reproducible pipeline for X dataset; baseline + improved model; evaluated with Y metrics; documented tradeoffs"

#### HCI / UX / product-adjacent technical roles
- **Section order:** Header → Education → Projects (product/user-value forward) → Experience → Skills
- **Emphasize:** Human impact, prototypes shipped, experiment results, usability findings, stakeholder collaboration
- **Cut first:** Long tech-stack lists not used in projects, deep low-level infra details
- **Proof signals:** Portfolio case studies with problem → intervention → evaluation; link consistency with LinkedIn
- **Skills grouping order:** Research/Methods → Prototyping/Frontend → Analytics → Collaboration tools
- **Headline project example:** "Designed and tested interaction X; iterated using user feedback; implemented prototype; measured improvement"

#### QA / test engineering
- **Section order:** Header → Skills (test tooling + languages) → Experience → Projects → Education
- **Emphasize:** Test automation, coverage strategy, CI integration, defect lifecycle, reliability improvements
- **Cut first:** Purely feature-building bullets not linked to quality outcomes
- **Proof signals:** Example test frameworks, CI pipelines, flaky-test mitigation, clear bug reports, performance/test results
- **Skills grouping order:** Automation frameworks → Languages → CI/CD tools → Testing types → Bug tracking
- **Headline project example:** "Built automated test suite for X; integrated in CI; prevented regressions pre-merge"

**When to include GPA, Summary, Coursework, Extracurriculars, Hackathons, Awards, Publications, Research:**
- **GPA (evidence-anchored rule):** Include GPA on the resume if (a) the posting requests it, **or** (b) your GPA meets typical employer screening cutoffs. NACE Job Outlook 2023 reports a **median GPA cutoff of approximately 3.0/4.0** across industries, regions, and company sizes among employers that screen by GPA. Multiple university career centers (University of Lethbridge, Algonquin College, Carnegie Mellon Tepper) converge on the same ~3.0 threshold. If you include GPA, **always include the scale** (e.g., "GPA: 3.4/4.0"). For non-4.0 Canadian scales (4.3, 4.33, percentage), state the denominator explicitly. Below ~3.0 and not requested → omit and use the line for higher-signal evidence. **Note:** the popular "include only if 3.5+" rule is convention without empirical support; the only employer-side cutoff with real survey data behind it is 3.0.
- **Summary:** Only if it adds non-obvious targeting value in ≤2 lines and contains role-relevant keywords. Otherwise omit.
- **Relevant Coursework:** 0–2 lines under Education *only if* the candidate lacks aligned experience and the courses match the target job family. Otherwise omit to preserve space.
- **Extracurriculars:** Include only if signal-dense (e.g., technical leadership, hackathon wins). Generic club membership is filler.
- **Hackathons:** Include 1–2 strong ones that demonstrate shipping under constraint. Treat as projects.
- **Awards:** Include only if relevant and recognizable. Skip generic merit awards unless prestigious.
- **Publications:** Include if relevant to research-leaning roles. Otherwise treat as bonus credibility.
- **Research:** Include if relevant to ML/data/research roles. Format like a project with reproducibility and methods detail.
- **Capstones:** Format as a project with team size, duration, your specific role, technical decisions, and shipped artifact.

**Risks and exceptions:**
- US federal hiring (USAJOBS) imposes different content requirements — use the federal-specific format separately.
- Direct evidence for role-family-specific section ordering is thin; treat as strong conventions, not proven causal levers.

---

### E. Bullet point quality and content strategy

**Facts:**
- Tier 1 evidence (Wingate et al. 2025) shows that compositional quality — operationalized as detail, clarity, and structure — predicts more interviews per application and faster placement for students, controlling for experience and tailoring degree.
- Eye-tracking evidence (TheLadders 2018) suggests resumes that are easier to process use **short declarative statements** rather than paragraph-length descriptions; job titles function as primary anchors.
- Government and university guidance encourages results-focused language with numbers/percentages when honest, or descriptive proxies when numbers aren't available.
- Government career guidance warns against buzzwords and recommends standard bullet marks (not fancy symbols) because some ATS can't read them.

**What strong technical bullets consistently include:**
- **Action** — what you did, with a specific verb
- **Artifact / system** — what you built or changed (API, service, pipeline, UI, infra module)
- **Method / stack** — language, framework, cloud, tooling
- **Outcome** — latency, reliability, throughput, dev time, errors, user task time, or a credible qualitative proxy
- **Credibility hook** — tests, monitoring, deployment, users, PRs, docs

**What to avoid:**
- Vague verbs ("worked on," "helped with") without ownership clarity
- Buzzword lists disconnected from action ("leveraged scalable cloud-native microservices")
- Metrics that are ungrounded or implausible
- Paragraph-length bullets
- Repeated structures across all bullets (e.g., every bullet starting with "Designed/Developed/Implemented")

**Operational defaults (convention, not empirical):**
- **Lines per bullet:** 1–2 lines. Add detail by choosing better nouns, not longer sentences. `[insufficient data]` for a strict universal rule.
- **Bullets per role:** Convention suggests 3–5 for recent or relevant roles, 2–3 for older/less relevant. `[insufficient data]` for empirical optima — eye-tracking research operates at section/area-of-interest level (Pina et al. 2023; Törngren et al. 2024), not at the bullet-count level. The convention is grounded in time-budget reasoning, not measured outcomes.
- **First bullet matters most:** Because early attention is limited, ensure the first bullet of each entry is the strongest. Diminishing returns set in after the first few.

**Differences by entry type:**
- **Internships and technical jobs:** Emphasize ownership scope, technical decisions, collaboration with named artifacts, and outcomes
- **Projects:** Emphasize what's deployed, scope of design decisions, tests/CI, README quality
- **Hackathons:** Emphasize what shipped under time constraint, integration choices, working demos
- **Capstones:** Emphasize team size, your specific role, multi-month scope, technical decisions, stakeholder demo
- **Research:** Emphasize methods, reproducibility, baselines, evaluation rigor, ablations, code/artifact sharing

**Risks and exceptions:**
- Over-optimization for keywords harms human credibility. Keyword stuffing is explicitly identified as a negative signal even when it helps automated screening.

---

### F. Projects vs experience

**Facts:**
- Peer-reviewed software-hiring research (Kuttal et al. 2021, *Information and Software Technology*) shows hiring evaluators use both technical and soft-skill cues from GitHub and Stack Overflow, but **rely heavily on low-effort surface signals** (READMEs, deployment, presence of tests) due to time constraints.
- A 2025 preprint interviewing hiring managers suggests open-source contributions can demonstrate employer-valued traits when they are visible and well-documented.
- University guidance (e.g., student career centers) explicitly frames projects as "real experience" for students and recommends formatting them with the same structure as work experience (title, date, bullets).

**Interpretation:**
Projects can compensate for limited internship volume **only when presented as credible, non-toy systems**. The deciding factor is not the project's complexity but its **evaluability under time constraint** — can a reviewer verify quality in under 30 seconds?

**Proof signals that make projects credible:**
- Deployed link or live demo
- GitHub repo with clear README, setup instructions, and meaningful commit history
- Tests / CI / documentation
- Real users or real data (even small scale)
- Evidence of iteration (issues closed, PRs merged)
- Awards or competition placement
- Measurable outcomes (where honest)

**When projects should take more space than work experience:**
- When the candidate has no relevant work experience at all
- When projects are significantly more aligned with the target role family than the work history
- When the work experience is non-technical (retail, food service) and the projects are the only technical evidence

**How to weight different project types:**
- **Personal projects with deployment + users:** Highest credibility
- **Hackathon projects:** Mid-credibility; show ability to ship under constraint
- **Capstones:** Mid-to-high credibility; show team collaboration on multi-month scope
- **Coursework projects:** Lowest credibility unless materially extended beyond the assignment; differentiate with deployment, tests, or scope

**Risks and exceptions:**
- Projects that look like coursework without differentiation (no deployment, no scope, no clear ownership) are discounted by reviewers operating under time constraints.

---

### G. Skills section research

**Facts:**
- ATS parsing documentation recognizes "SKILLS" as a standard section type and treats standard headings as important for extraction.
- ATS guidance emphasizes keyword matching and recommends integrating keywords into bullets, not only listing them in Skills.
- Industry recruiter surveys (Recruiter Nation 2025 and similar) indicate skills-based hiring is increasingly central.
- University templates (e.g., Algonquin College) explicitly advise: do not list skills you cannot support with examples.

**Direct answers to your sub-questions:**

**How many skills total before credibility drops?**
- No empirically validated cutoff exists. `[insufficient data]`
- **Convention-based safe ceiling:** **12–24 hard skills** total across groupings, including only skills relevant to the role family.
- **Hard rule (better than counts):** Every listed skill must be defensible in a bullet or project within ~30 seconds.

**Should proficiency labels be used?**
- **Graphical proficiency indicators (stars, bars, dots):** **Avoid.** Not reliably machine-readable; flagged by ATS-safe guidance as risky formatting.
- **Text proficiency labels ("Proficient," "Familiar," "Expert"):** Mixed evidence; mostly non-empirical. `[insufficient data]`
- **Safest default:** Do not use subjective proficiency labels. Convey level through where and how the skill was used (in project/role bullets) and through ordering (most-used first).
- **Exception:** Objective standardized labels are fine when explicitly requested (e.g., "Fluent in French" for language skills).

**Should coursework be embedded in skills, separate, or omitted?**
- Coursework signals "learned" not "applied." It belongs under **Education** as a "Relevant Coursework" line, not in Skills.
- **Safest default:** 0–2 lines of relevant coursework under Education only if directly matching the job and the candidate lacks aligned experience. Otherwise omit.

**Optimal number of skill groupings:**
- **Safest count:** **3–5 groupings**
- **Recommended group names (ATS-safe and widely legible):**
  - Languages
  - Frameworks / Libraries
  - Tools / Platforms
  - Databases
  - Cloud / DevOps (only if relevant)

**How to handle skills the job description mentions but you've only briefly touched:**
- Do not list under Skills unless you can defend it credibly with at least one concrete usage.
- If you've only briefly used it, mention it inside a project bullet ("Used Redis for caching in X") rather than elevating it to the Skills section.

**What over-stuffed skills sections look like and why they backfire:**
- Patterns: 40+ tools listed, many unreferenced; buzzword clusters (AI/ML/cloud/security) without proof; tools added to mirror job ads
- Backfire mechanisms: human credibility loss ("keyword stuffing"); ATS noise (irrelevant matches dilute fit signal); recruiters discount the entire skills section when one item looks fake

---

### H. Tailoring strategy

**Facts:**
- Tier 1 student outcome evidence (Wingate et al. 2025) shows compositional quality predicts outcomes **even controlling for tailoring degree** — meaning baseline clarity and structure matter as much as tailoring.
- Multiple ATS guidance sources state that ATS systems compare resumes against job descriptions and may rank or score based on keyword match.
- Harvard Business School / Accenture's "Hidden Workers: Untapped Talent" report (2021) argues employers' systems often filter out candidates who could do the job but don't match the criteria language closely — supporting the value of vocabulary alignment.

**How much tailoring is enough?**
For high-volume internship applications, tailoring should be **surgical, not comprehensive**. Update target title, reorder skills, and adjust 2–4 bullets/projects to mirror the job's core keywords and domain constraints — without rewriting the entire resume each time.

**Minimum viable tailoring (high ROI under time constraint), in order:**
1. Title line / role focus (what role you're applying for)
2. Skills section ordering and inclusion (only skills you can defend)
3. Top 2–3 bullets (Experience or Projects) rewritten using job-post language
4. Coursework only if it maps directly to requirements

**Tailoring by subdomain:**

#### Software engineering version
- **Change:** Headline project to match stack (backend vs frontend); reorder Skills so target stack is first; rewrite 2–4 bullets with job's core nouns (API, microservice, React state, performance, testing)
- **Highest-value move:** Replace vague verbs with concrete system nouns + one constraint/outcome per bullet
- **Keyword density tolerance:** Medium — SWE reviewers penalize buzzword clusters

#### Cloud / DevOps / SRE version
- **Change:** Move cloud/tooling skills earlier; select projects showing deployment and reliability; add operational nouns (monitoring, alerts, rollback, IaC)
- **Highest-value move:** One bullet tying automation to reliability or speed
- **Keyword density tolerance:** Medium-High in enterprise ATS contexts, but only with proof

#### IT / systems / helpdesk version
- **Change:** Skills order — OS/tools/ticketing first, frameworks de-emphasized; bullets emphasize troubleshooting scope and user impact; show customer-facing communication
- **Highest-value move:** 1–2 bullets quantifying volume/scope (tickets per week, devices supported) when truthful
- **Keyword density tolerance:** Often higher because tool lists are central; still avoid stuffing

#### Data / analytics / ML version
- **Change:** SQL/Python/data tooling at top of Skills; replace generic ML bullets with evaluation/reproducibility language (baseline, metrics, leakage); add domain nouns from job (forecasting, segmentation, ETL)
- **Highest-value move:** One "rigor bullet" — dataset → method → evaluation → limitation
- **Keyword density tolerance:** Medium; tolerates tool keywords but penalizes "model zoo" lists

#### QA / test engineering version
- **Change:** Test frameworks and CI early in Skills; reframe bullets toward defect prevention, coverage strategy, automation; highlight cross-team collaboration
- **Highest-value move:** A CI/testing bullet that clearly states what was automated and what failures it catches
- **Keyword density tolerance:** Medium-High for tooling terms

#### Product / technical analyst version
- **Change:** Add a 3–5 line profile only if it materially clarifies fit; reorder bullets toward analysis, stakeholder communication, requirements, dashboards; emphasize SQL, Excel, BI, experiment design
- **Highest-value move:** Replace "built X" with "analyzed/translated requirements → built artifact → supported decision"
- **Keyword density tolerance:** Medium; can read consulting-generic fast — use specifics

**Tailoring by company type:**
- **Big tech / enterprise:** Higher ATS keyword discipline; conservative formatting; standard headings critical
- **Startups:** Emphasize shipping and ownership; deployed proof matters more than buzzword density
- **Government:** Use sector-specific format requirements; do not assume private-sector norms apply

**Risks:**
- Over-tailoring can produce inconsistency between resume and LinkedIn, which harms credibility (digital footprint research shows profile inconsistencies affect evaluations).

---

### I. International experience and "Canadian experience"

**Facts:**
- The Ontario Human Rights Commission (OHRC) policy guidance (2013) frames "Canadian experience" requirements as potentially discriminatory and emphasizes job-related, objective criteria.
- The Government of Ontario announced in November 2023 a ban on Canadian work-experience requirements in covered job postings.
- **Updated 2026:** Ontario's job posting obligations are now operational. Covered publicly advertised job postings and application forms generally cannot require Canadian experience. Additionally, employers must disclose AI screening use if AI is used to screen, assess, or select applicants.
- Tier 1 evidence (Wingate et al. 2025) found that domestic students obtained more interviews and faster job acquisition than visa students even controlling for experience, achievement, and writing quality — suggesting non-domestic candidates face additional friction beyond formal requirements.

**Interpretation:**
"Canadian experience" is now partly **legally restricted** (Ontario covered employers) and partly a **credibility heuristic** elsewhere. The best strategy is not to hide international experience but to **translate it into legible, comparable signals**. Reduce ambiguity wherever possible.

**How to frame international technical experience for credibility:**
- **Standard role titles** that map to North American conventions (e.g., "Software Engineering Intern" rather than untranslated local titles)
- **Concise company context** — one phrase explaining what the company does and approximate scale
- **Mainstream technology stack** — list familiar frameworks even if locally branded versions were used
- **Concrete deliverables and outcomes** — shipped services, performance/reliability changes, CI/CD usage, test coverage, incident reduction
- **Clear location and dates** in standard format
- **Avoid apologetic framing** ("only international experience"); instead present concrete systems and outcomes

**What makes international experience appear weaker:**
- Untranslated company names with no context
- Non-standard role titles
- Local technology references without mainstream equivalents
- Vague responsibility descriptions
- Missing dates or unclear timelines

**Recognizable brands vs unknown companies:**
Reviewers operating under time constraints rely on brand recognition as a low-effort credibility signal. For unknown companies, one short context phrase ("e-commerce platform serving X customers") substitutes for brand recognition.

---

### J. Adjacent resume-performance factors

**Facts:**
- Experimental research (Türker 2025, *Frontiers in Psychology*) shows social media content can shift perceived competence and fit and change hiring intentions — even when resume qualifications are strong.
- Research on LinkedIn profiles (Härtel et al. 2024) shows profiles contain measurable cues that can predict traits and influence judgments.
- Software hiring research (Kuttal et al. 2021) shows online contribution platforms inform hiring decisions but reviewers favor low-effort cues.
- University guidance (UMich, others) explicitly notes that links may not work inside ATS and should be treated as secondary proof.

**LinkedIn:**
- **Help when:** Dates, titles, and companies match the resume exactly; profile is professional and complete; key skills and accomplishments are reinforced
- **Hurt when:** Inconsistencies with the resume; gaps in employment that the resume hides; controversial content; sparse or empty profile
- **Operational rule:** Always include a LinkedIn URL on the resume. Always verify resume ↔ LinkedIn consistency before applying.

**GitHub (evidence-cautious):**
- **No verified causal evidence** that adding a GitHub URL increases callbacks for SWE interns or new grads. Peer-reviewed evidence (Kuttal et al. 2021) supports that evaluators *use* GitHub contribution traces in hiring and often rely on low-effort surface signals (aggregate activity, README quality) under time constraints. A 2024 ifo Institute working paper (Abou El-Komboz & Goldbeck) finds that developers' GitHub activity rises during job-search periods, which is consistent with developers themselves treating GitHub-visible work as a labor-market signal — but does not directly measure resume callback effects.
- **Help when:** Pinned repos are clean; READMEs are clear; recent commit activity exists; at least one project has tests or deployment
- **Hurt when:** Empty profile; repos are forks or coursework with no original work; READMEs are missing; commit history is sparse
- **Operational rule:** Include GitHub only if it can withstand a 10–30 second skim. Pin 3–6 strongest repos. A sparse or messy GitHub link is plausibly worse than omitting the link entirely (inference, grounded in evaluator low-effort cue behavior). When in doubt, omit.

**Personal websites (distinct from portfolios):**
- **Help when:** Clean hub linking to GitHub, 2–4 top projects, concise about/skills page consistent with the resume; makes proof low-effort
- **Neutral when:** Purely duplicative of LinkedIn/GitHub
- **Hurt when:** Sloppy design, broken links, controversial content, inconsistent dates/titles, inflated claims
- **Operational rule:** Only include if you can keep it updated and professional. If in doubt, omit.

**Portfolios:**
- High value for HCI/UX/frontend/design-adjacent roles
- Lower value for backend, infrastructure, IT, data engineering — GitHub is sufficient
- Must contain case studies with problem → intervention → outcome structure

**Cover letters (tech-intern specific):**
- **Direct causal evidence for cover letter impact in Canada/US tech internship pipelines is `[insufficient data]`.** General evidence exists (Wingate et al. 2025 — Canadian co-op students; Cui, Dias, Ye 2025 — online labor markets), but neither is tech-intern-specific.
- **At least one major tech employer treats cover letters as optional in their official application flow:** Google Careers' Help Center explicitly states "cover letter [is] optional." This is a single Tier 3 data point, not a general rule, but it indicates that high-volume tech application pipelines do not always weight cover letters.
- The Cui, Dias, Ye 2025 working paper finds that AI cover letter tools can increase tailoring and short-term callbacks but reduce signal value over time as employers adjust skepticism — consistent with the broader trend of cover letters becoming weaker signals.
- **Help when:** Required by employer; role is cross-functional or communication-heavy; candidate needs to explain non-obvious story (career change, visa nuance, unusual timeline); applying to a smaller company where letters are more likely to be read
- **Hurt when:** Generic, obviously templated, or inconsistent with the resume; submitted to a high-volume tech intern funnel where they may not be read
- **Operational rule:** For broad CS intern/new-grad applications, prioritize resume quality and targeted keyword alignment first. Maintain a high-quality base cover letter that is 70% stable, customize 30%. Write a customized letter only when (a) required, (b) high-priority role, or (c) you have a specific high-signal narrative the resume cannot carry.

**Clickable links:**
- ATS may not preserve link functionality. Treat links as backup proof, not primary proof.
- Use short, readable URLs that work as plain text.

**Credibility signals ranked by value:**
1. Deployed project link (live demo)
2. GitHub with clean pinned repos
3. LinkedIn matching resume
4. Portfolio (for relevant roles)
5. Personal website (only if maintained)
6. Cover letter (situational)

---

### K. Risk analysis and myths

**Facts:**
- Multiple ATS and parser sources accept PDFs and parse them, but also warn that formatting can break parsing.
- Columns and tables are repeatedly flagged as high-risk across vendors.
- Color is permitted by some ATS guidance but may map to single-color text in others.

**Detailed myth analysis is in Section 6 (Myths and Misconceptions Table).**

---

### L. Tradeoffs under one-page constraints

**Facts:**
- Undergraduate resume norms emphasize one page for students.
- Eye-tracking research consistently flags clutter as harmful to first impressions.
- Some Canadian career guidance tolerates 1–2 pages depending on field.
- US federal hiring requires longer formats with specific content.

**Detailed cut order is in Section 7 (One-Page Tradeoff Rules).**

---

### M. "Looks strong" vs "looks generic / AI-written"

**Facts:**
- Wingate et al. 2025 notes that compositional features (detail, clarity, structure) can be produced by AI tools, implying signal dilution.
- Cui, Dias, Ye 2025 shows AI tools can increase tailoring and callbacks initially but reduce signal value over time as reviewers adjust skepticism.
- Persuasion-related research (Varma, Toh, Pichler 2006) shows impression management tactics can change perceived qualifications.
- Robert Half 2026 survey: 61% of HR leaders report AI-generated applications are slowing hiring.
- Gartner 2025 survey: only 26% of job applicants trust AI to evaluate them fairly.

**What makes a resume look credible vs AI-written is in Section 8 (Bullet Framework) and the AI red-flag checklist below.**

---

## 4. Comparison Tables

### 4.1 ATS-safe vs recruiter-optimized choices

| Decision area | ATS-safe default | Recruiter-optimized default | Safest balanced choice | Notes |
|---|---|---|---|---|
| Layout | Single column | Single column with strong hierarchy | **Single column + bold headers + whitespace** | Columns flagged as parse-risky and clutter-inducing |
| Tables / text boxes | Avoid | Avoid | **Avoid** | Parsing can miss or reorder content |
| Section headings | Standard names | Same | **Standard headings** | Improves both extraction and scan anchors |
| File format | DOCX (sometimes) | PDF (layout fidelity) | **Keep both, choose per portal** | Vendors accept both; no universal winner |
| Density / whitespace | Moderate | Moderate | **Readable density** | Cluttered resumes perform poorly |
| Keywords | Exact terms in context | Same | **Contextual keywords, never stuffed** | Stuffing harms human credibility |
| Links | Plain-text URLs safest | Clickable helps recruiters | **Short, readable URLs that work as plain text** | ATS may strip link functionality |
| Bullets | Standard characters | Short declarative | **Standard characters + 1–2 line bullets** | Fancy bullets break in some ATS |

### 4.2 One-column vs two-column

| Option | Upside | Downside | Verdict |
|---|---|---|---|
| **One-column** | Highest parsing reliability; predictable read order | Slightly less "designed" look | **Default for ATS-heavy markets** |
| **Two-column** | More content per inch; "modern" appearance | Column extraction can mix content; flagged by every vendor consulted | **Avoid unless** sending direct to a human and accepting ATS risk |

### 4.3 Serif vs sans-serif

| Aspect | Evidence | Verdict |
|---|---|---|
| General legibility | Richardson (2022, Springer Open Access) reviews decades of evidence and concludes **no consistent inherent legibility advantage** for serif vs sans-serif in general reading on paper or screens | No category winner on average |
| Small-size screen reading (resume use case) | Richardson (2022) notes serif strokes can become **faint or invisible at very small type sizes or low luminance** — directly relevant to 10–11pt resumes on screens. Minakata & Beier (2022, *Acta Psychologica*) corroborate that the effect depends on stroke contrast and font characteristics | **Sans-serif marginally safer** for body text at 10–11pt on screens |
| ATS compatibility | Both render reliably if using common system fonts | Either is safe |
| **Recommendation** | — | **Sans-serif (Arial, Calibri, Helvetica) preferred for body text. Serif (Times New Roman, Garamond, Georgia) acceptable but not preferred for screen-first reading at small sizes. Consistency matters more than the specific family.** |

### 4.4 Summary vs no summary

| Choice | Supports | Risks | Rule |
|---|---|---|---|
| **Add summary** | Some eye-tracking work suggests top-performing resumes have an overview; can add keywords and differentiation | Generic "objective" wastes prime space; can look AI-written if vague | Use only if specific in 1–2 lines and adds non-obvious targeting value |
| **No summary** | Saves prime space for evidence; safer default | Misses chance to set context | **Default for most student resumes**; reclaim the space |

### 4.5 Short bullets vs detailed bullets

| Choice | Supports | Risks | Rule |
|---|---|---|---|
| **Short (1–2 lines)** | Easier to process; supports scan; eye-tracking favors short declarative | Some technical depth may be lost | **Default**; add detail via better nouns, not longer sentences |
| **Detailed (3+ lines)** | Shows depth; appropriate for senior roles | Penalized as paragraph-like; clutter signal | Avoid for student resumes |

### 4.6 Projects-first vs experience-first

| Choice | When | Notes |
|---|---|---|
| **Experience-first** | When candidate has relevant recent technical work that anchors the top scan | **Default for most students with any internship** |
| **Projects-first** | When projects are materially stronger and more role-aligned than work history | Use when work experience is non-technical or absent |

### 4.7 Big tech / startup / enterprise / government expectations

| Employer type | Process | Resume implications | Notes |
|---|---|---|---|
| **Big tech** | High volume, structured filtering, ATS-heavy | Conservative format; keyword alignment critical; standard headings | Brand recognition helps; clear titles essential |
| **Startups** | Smaller volume, less formal | Emphasize shipping, ownership, deployed proof | Still use ATS in many cases |
| **Mid-size tech** | Variable | Treat as blend of big tech and startup | `[insufficient data]` for clean differences |
| **Banks / telecom / enterprise** | ATS-heavy, compliance-focused | Conservative formatting, clear skills, aligned keywords | Less tolerance for unconventional formats |
| **Government / public sector** | Distinct rules; specific format requirements | Use sector-specific format (e.g., USAJOBS); often longer; more detail expected | Do not assume private-sector norms apply |

### 4.8 Technical recruiter vs non-technical recruiter vs hiring manager vs engineer

| Reviewer | First look | Time | Disqualifies | Excites | Gets stuck on |
|---|---|---|---|---|---|
| **Technical recruiter** | Titles, tech keywords, recent experience | Short first pass (~6–15s) | Cluttered layout, keyword stuffing, unclear titles/dates | Clear stack match, credible projects, clean hierarchy | Long unsupported skills lists; coursework-looking projects |
| **Non-technical recruiter / HR** | Role fit, chronology, education, location/eligibility | Similar, slightly slower (`[insufficient data]` for clean separation) | Confusing structure, missing basics, footprint red flags | Clear story, transferable impact, simple format | Domain jargon without explanation; unclear ownership |
| **Hiring manager** | Evidence of capability for team needs | Longer when engaged, but not guaranteed | Vague bullets, inflated claims, skills/evidence mismatch | Proof of shipping, technical decisions, concise explanation | Generic content; fake-feeling metrics |
| **Engineer / technical interviewer** | GitHub, projects, depth cues, technical nouns | Variable; brief unless triggered | Buzzword-only, no evidence, messy repos, contradictions | Real project evidence, clear constraints, tests, tradeoffs | Hard-to-evaluate projects (no README/demo); unverifiable claims |

### 4.9 Canada vs US vs broader global differences

| Dimension | Canada norm | US norm | Global variation | Safest default for both Canada + US |
|---|---|---|---|---|
| **Page length (intern/new grad)** | 1 page common; 1–2 tolerated in some fields | 1 page strongly conventional; federal hiring is exception | Some markets prefer longer CVs | **Use 1 page** unless applying to US federal |
| **Photo** | Do not include | Do not include | Some European/Asian formats include photo | **No photo on resume**; LinkedIn only |
| **Date format** | Month Year | Month Year; federal may want more | DD/MM/YYYY in some countries | **Spell month** ("Jan 2025") to avoid ambiguity |
| **Address** | Often optional; city/province may suffice | Often optional | Full address common in some CV formats | **City + province/state + country**; omit street |
| **References** | Separate document, not on resume | Same; "available upon request" discouraged | Some countries expect referees listed | **Do not include on resume** |
| **Personal info (DOB, marital status)** | Do not include | Do not include | Some countries include | **Exclude all personal data** beyond contact and links |
| **Language norms (tone)** | Concise accomplishment bullets | Same | Some markets accept more narrative | **Concise bullets with technical nouns and outcomes** |
| **"Canadian experience" framing** | Now legally restricted in Ontario (2026); discriminatory under OHRC guidance | "US experience" is informal heuristic; not regulated | Local-experience heuristics vary | **Translate international experience into comparable signals** |
| **Work authorization disclosure** | Handled in application forms; do not put status on resume | Employers may ask "authorized?" and "need sponsorship?" in forms | Some countries require visa status on CV | **Do not put visa status on resume** unless explicitly required |
| **Government / public sector** | Varies by agency | US federal has specific format requirements | Varies widely | **Use separate federal resume format** when required |
| **AI screening disclosure (Ontario, 2026)** | Required for covered employers using AI screening | Not federally regulated | Varies | Be aware that Ontario applications may now disclose AI use |

---

## 5. Recommendation Table

**Legend:**
- Evidence strength: Strong / Moderate / Limited / Weak
- Confidence: High / Medium / Low
- Risk: Low / Medium / High (risk of harming ATS or human review if implemented poorly)

| # | Recommendation | Rationale | Source types | Evidence | Confidence | Helps | Tradeoffs / exceptions | Risk |
|---|---|---|---|---|---|---|---|---|
| 1 | Use single-column layout | Minimizes parse errors; improves scan anchors | ATS/parser docs + eye-tracking | Strong | High | ATS + humans | Two-column may look "designed" but parse risk dominates | Low |
| 2 | Avoid tables, text boxes, graphics, icons | Breaks linear extraction; can omit critical fields | ATS/parser docs | Strong | High | ATS | None worth the risk | Low |
| 3 | Use standard section headings | Improves parse and fast navigation | ATS/parser docs | Strong | High | ATS + humans | None | Low |
| 4 | Put contact info in main body at top | Parsers expect it near top | Parser guidance | Moderate | Medium | ATS + humans | Stylized headers can break extraction | Low |
| 5 | Bold job titles and section headers | Recruiters anchor on titles | Eye-tracking | Strong | High | Recruiter | Over-bolding creates noise | Low |
| 6 | Optimize for detail, clarity, structure | Predicts better student outcomes | Peer-reviewed Tier 1 | Strong | High | All | Must remain truthful | Low |
| 7 | Concise role-aligned skills section reinforced in bullets | Supports ATS search + human scan | ATS + parsing | Moderate | Medium | ATS + humans | Some guidance downplays separate skills sections | Low |
| 8 | Use contextual keywords; avoid stuffing | Helps ATS while preserving credibility | Eye-tracking + ATS | Moderate | High | ATS + humans | Requires careful tailoring | Low |
| 9 | Keep bullets to 1–2 lines but specific | Improves cognitive throughput | Eye-tracking + readability | Moderate | Medium | Humans | Some technical roles want more context | Low |
| 10 | Provide proof signals for projects | Reviewers use low-effort online cues | Peer-reviewed software hiring | Moderate | Medium | Recruiter + engineer | Links must be maintained | Medium |
| 11 | Keep LinkedIn / resume consistent | Digital footprint affects judgments | Experimental cybervetting | Moderate | Medium | Humans | Don't add unverifiable claims | Medium |
| 12 | Prepare both PDF and DOCX | Parse success varies by portal | ATS vendor + Workday | Strong | High | ATS | Slight maintenance | Low |
| 13 | Frame international experience with comparable signals | Reduces ambiguity | Policy + outcomes inference | Moderate | Medium | Humans + ATS | Don't over-explain | Low |
| 14 | One page default for interns/new grad | Norms + scan constraints | Institutional + scanning | Limited–Moderate | Medium | Humans | Federal exception; some Canadian sectors accept 2 | Medium |
| 15 | Body 11pt, margins 0.75", line spacing 1.0 | Convention-based safe defaults; readability evidence | University career centers + CHI readability | Moderate | Medium | All | Range 10–12pt acceptable | Low |
| 16 | Use common system font; sans-serif preferred for body text on screens at small sizes | Richardson 2022: no general difference but serifs can become faint at small sizes/low luminance | 2022 typography monograph + Acta Psychologica | Strong | High | All | Avoid uncommon downloaded fonts; serif acceptable but not preferred for body | Low |
| 17 | No photo, no personal info (DOB, marital status, SIN/SSN) | NA convention; bias risk | Government + career guidance | Strong | High | All | Some countries differ | Low |
| 18 | Education near top for current students | Recruiter expectation | Tier 4 + eye-tracking | Moderate | High | Recruiter | Reconsider if experience dominates | Low |
| 19 | Treat capstones and projects with same formatting as experience | Student guidance + signal value | University guidance | Moderate | Medium | Recruiter | Must be credible | Medium |
| 20 | Include 1–3 links max (LinkedIn, GitHub, optional portfolio) | Backup proof; ATS may strip | Tier 4 | Moderate | Medium | Humans | All linked profiles must be clean | Medium |
| 21 | Tailor surgically (title + skills + 2–4 bullets) | High ROI under time constraint | ATS guidance + outcomes | Moderate | High | ATS + humans | Don't introduce inconsistency with LinkedIn | Low |
| 22 | Skip subjective proficiency labels | Unverified utility; graphical bars break ATS | Vendor + university | Moderate | Medium | ATS | Objective labels OK (e.g., language fluency) | Low |
| 23 | Keep skills count to 12–24 defensible items | Convention-based ceiling | University guidance + inference | Limited | Medium | Humans | Hard rule: every skill defensible in 30 seconds | Low |
| 24 | Cover letter only when required, high-priority, or narrative-needed | Mixed evidence; signal dilution risk | Tier 1 outcomes + working paper | Moderate | Medium | Humans | Required for some employers | Low |
| 25 | For Ontario applications: do not anticipate "Canadian experience required" language | Now legally restricted | Government 2024–2026 | Strong | High | All | Implicit preference may persist | Low |
| 26 | Include GPA only if ≥3.0/4.0 or explicitly requested; always include the scale | NACE Job Outlook 2023: median screening cutoff ~3.0; multiple university career centers converge on same threshold | NACE survey + Tier 4 institutional | Moderate | High | ATS + recruiter | Below 3.0 → omit; "3.5+" rule is unevidenced convention | Low |

---

## 6. Myths and Misconceptions Table

| # | Myth | Evidence assessment | Verdict | Safest practical takeaway |
|---|---|---|---|---|
| 1 | "ATS rejects PDFs" | Major ATS accept PDF; parsers support PDF; reliability varies | **Unsupported as a blanket claim** | Use text-based PDF by default; keep DOCX fallback for portals that auto-fill poorly |
| 2 | "Two-column resumes always fail ATS" | Vendors repeatedly warn columns/tables break parsing; some parsers attempt fixes | **Partially supported / high-risk** | Avoid columns; only use if you've verified parse success in target portals |
| 3 | "You must use Times New Roman" | Richardson (2022, Springer): no consistent legibility advantage for serif vs sans in general reading; sans-serif may be marginally safer for body text at small sizes on screens | **Unsupported, with nuance** | Use a common system font; for body text at 10–11pt on screens, sans-serif (Arial, Calibri, Helvetica) is marginally preferred over serif |
| 4 | "Every bullet must include a metric" | Tier 1 student outcomes emphasize detail/clarity/structure, not "metrics always" | **Unsupported** | Use metrics when real and meaningful; otherwise use concrete scope, constraints, and outcomes |
| 5 | "One page means cramming as much as possible" | Eye-tracking flags clutter as worst-performing | **Unsupported** | One page should be selective and readable, not maximally dense |
| 6 | "Recruiters ignore international experience" | Policy + Tier 1 outcomes suggest friction but not "ignore"; legal restrictions in Ontario | **Context-dependent** | Keep prominent if relevant; add comparability signals |
| 7 | "Summaries are always useless" | Mixed evidence; can help if specific, harm if generic | **Context-dependent** | Use only if highly targeted in ≤2 lines; otherwise reclaim space |
| 8 | "Projects don't matter if you have experience" | Online contributions inform hiring; reviewers use low-effort cues | **Unsupported** | Keep best 1–3 role-aligned projects with proof signals |
| 9 | "Color is always bad" | `[insufficient data]` for ATS outcomes; risk is indirect | **Context-dependent** | Use minimal high-contrast color only in headings if at all |
| 10 | "Fancy formatting is always bad" | Formatting that breaks parsing is bad; mild hierarchy is beneficial | **Context-dependent** | Use restrained hierarchy; avoid known parse-breakers (columns/tables/graphics) |
| 11 | "GPA must be on a tech resume" | NACE Job Outlook 2023: median screening cutoff is ~3.0/4.0 among employers that screen; many employers don't screen by GPA at all | **Unsupported** | Include GPA if ≥3.0/4.0 or explicitly requested; always include the scale. The popular "3.5+" rule is convention without empirical backing — 3.0 is the only threshold with real survey data |
| 12 | "You should use action-verb variety to look smarter" | Repeated identical verbs is an AI-written red flag, but forced variety can also feel synthetic | **Partially supported** | Use varied but natural verbs; never sacrifice clarity for variety |

---

## 7. One-Page Tradeoff Rules

For a 4th-year CS student building a one-page resume, apply these decision rules in order.

### Default rule
**Prefer one page** unless the target sector explicitly expects longer (some Canadian fields, US federal hiring) or the candidate has substantial directly relevant experience.

### Cut order (lowest harm → highest harm)

When the resume exceeds one page, cut in this order:

1. **Hobbies / interests** (unless directly relevant to the role)
2. **Generic coursework** (keep only 3–5 highly relevant courses, or omit entirely)
3. **Older / less relevant role bullets** (reduce to 1–2 lines each)
4. **Weak or duplicate skills** (keep only role-relevant; remove anything not defensible)
5. **Low-signal awards or extracurriculars** (keep only signal-dense items)
6. **Weak projects** (keep only those that look like real engineering)
7. **Summary** (unless sharply targeted)

### Add order (highest lift per line)

When the resume has space to fill, add in this order:

1. **One high-signal recent role bullet** with concrete outcome
2. **One high-signal project** with deployed/demo proof link
3. **A tight skills section** aligned to target role keywords
4. **A second project** if it covers a different stack or capability
5. **Relevant coursework** (only if no aligned experience elsewhere)

### Hard rules (never violate)

- **Never trade scannability for content volume.** Do not use ultra-small font, cramped line spacing, or paragraph bullets to cram more in.
- **Never use columns or tables to fit more.** The parse risk is not worth the inch saved.
- **Never include a bullet you cannot defend in an interview.** Padding with unverifiable claims is more damaging than empty space.
- **If you must choose between more bullets vs more whitespace, prefer fewer high-specificity bullets.** Clutter is penalized.

### One-page tradeoff matrix

| Tradeoff | Default winner | Reasoning |
|---|---|---|
| Summary vs more bullets | More bullets | Bullets carry verifiable evidence; summaries risk generic |
| Skills section length vs project detail | Project detail | Skills must be defensible; projects are evidence |
| Coursework vs awards vs extracurriculars | Awards if signal-dense; otherwise omit all three | Most students have low-signal versions of these |
| Experience vs projects ordering | Experience-first when relevant | Default for any candidate with technical work history |
| Breadth vs depth | Depth | Reviewers value verifiable depth over surface breadth |
| Visual hierarchy vs space efficiency | Hierarchy | Hierarchy supports the scan; cramming defeats it |

---

## 8. Bullet Point Writing Framework

This framework is designed to be source-aligned with what is most evidence-supported: clarity, structure, short declarative statements, and proof signals.

### Core structure

**Action + Artifact/System + Method/Stack + Outcome + Credibility hook**

- **Action:** built / implemented / migrated / automated / reduced / debugged / shipped
- **Artifact/system:** API, service, pipeline, UI, infra module, data model
- **Method/stack:** language, framework, cloud, tooling
- **Outcome:** latency, reliability, throughput, dev time saved, errors reduced, user task time, or qualitative proxy
- **Credibility hook:** tests, monitoring, deployment, users, PRs, docs

### What to include (stronger signals)

- **Concrete nouns:** what exactly you built (API, schema, pipeline, dashboard, runbook)
- **Constraints:** scale, performance targets, reliability requirements
- **Evidence work is real:** deployment, monitoring, testing, docs, users, open-source traces
- **Keywords in context:** woven into bullets, not dumped in skills

### What to avoid (common AI / generic signals)

- **Vague verbs:** "worked on," "helped with," "involved in"
- **Buzzword clusters without action:** "leveraged scalable cloud-native microservices to drive innovation"
- **Ungrounded metrics:** "reduced latency by 70%" with no baseline or system context
- **Repeated structures:** every bullet starting with "Designed/Developed/Implemented"
- **Resume-ese intensifiers:** "significantly," "successfully," "robust," "cutting-edge" without evidence
- **Generic collaboration:** "cross-functional collaboration," "stakeholder alignment," "synergy" with no who/what
- **High adjective-to-noun ratio** with low system nouns (no API, schema, pipeline, service, test suite)

### Bullet count and length guidance

- **Lines per bullet:** 1–2 lines. Add detail by choosing better nouns, not longer sentences.
- **Bullets per recent/relevant role:** 3–5 (convention; `[insufficient data]` for empirical optimum)
- **Bullets per older/less relevant role:** 2–3
- **Bullets per project:** 2–4

### How to write impact when no metric is available

Use a **bounded impact proxy**:
1. **What changed:** the system or component
2. **Why it mattered:** risk reduced, reliability improved, time saved, fewer manual steps
3. **How you know:** tests added, monitoring/log evidence, stakeholder adoption, demo used, documentation produced

### Examples (weak → better → strongest)

#### Internship / technical job
- **Weak:** "Worked on backend services using Java and AWS."
- **Better:** "Implemented Java API endpoints for user authentication in AWS-hosted service; reduced login errors by fixing token-refresh edge cases."
- **Strongest:** "Implemented OAuth token-refresh and session validation in Java (Spring) service on AWS; eliminated intermittent login failures observed in CloudWatch logs by adding expiry-aware retries plus integration tests."

#### Project (no hard metrics)
- **Weak:** "Built a full-stack web app with React and Node."
- **Better:** "Built a React + Node.js app for X that supports Y; deployed on Z with CI."
- **Strongest:** "Built and deployed React + Node.js app for [use case]; designed REST API + PostgreSQL schema; implemented auth and error handling; added CI pipeline; documented setup and tradeoffs in README with demo video."

#### Hackathon / competition
- **Weak:** "Participated in hackathon; built an app."
- **Better:** "Built [feature] in 24h; integrated [API]; team of 4."
- **Strongest:** "Owned backend integration in 24h build; shipped working demo integrating [API]; handled failure cases and wrote quick-start docs so judges could test."

#### Capstone (multi-month team deliverable)
- **Weak:** "Worked on a capstone project with a team to build an application."
- **Better:** "Built [component] for 4-month capstone in team of 5; implemented [feature] in [stack]; delivered demo to stakeholders."
- **Strongest:** "Owned backend API and database schema for 4-month capstone (team of 5); implemented auth and core workflows in [stack]; added CI tests and deployment script; shipped demo used by [stakeholder] and documented tradeoffs and next steps."

#### Research
- **Weak:** "Did research on machine learning."
- **Better:** "Investigated [problem]; implemented [method]; presented results."
- **Strongest:** "Built reproducible pipeline (data cleaning → training → evaluation) for [task]; compared baseline vs [approach] with ablations; documented limitations and shared code/artifacts."

#### Internship without metrics available
- **Weak:** "Improved performance and scalability of services."
- **Better:** "Refactored [service/module] in [stack] to remove duplicated logic and improve reliability; added tests for edge cases found in logs."
- **Strongest:** "Diagnosed intermittent auth failures by tracing logs; fixed token-refresh edge case in [service] and added integration tests + runbook entry to prevent recurrence."

### AI-written risk scoring rubric (for downstream LLM use)

Score 0–10 by adding 1 point for each present condition:

1. ≥30% of bullets start with the same 2 verbs (e.g., "Developed/Implemented")
2. ≥3 bullets contain "optimized/improved/enhanced" with no mechanism noun (API, db, test, pipeline, etc.)
3. ≥10 skills listed that never appear in bullets or projects
4. Any metric appears without baseline or system context (what was measured, against what)
5. Leadership/collaboration claims with no named artifacts (PRD, RFC, dashboard, ticket, incident report)
6. Buzzword density: 3+ buzzwords in a single bullet ("cloud-native scalable microservices leveraging AI")
7. Top projects omit proof signals (no link, no deployment, no README/tests)
8. Two bullets are semantically identical across different roles or projects
9. Inconsistent tense or formatting suggests mass templating
10. Resume "reads like marketing" — many adjectives, few technical nouns

**Scores 0–3:** Low risk. **4–6:** Medium risk; targeted rewrites needed. **7–10:** High risk; significant rewrite required.

### Safest rewrite rule when AI risk is high

Replace adjectives with **verifiable nouns + constraints + outcomes**, and ensure each listed skill appears as evidence at least once in a bullet or project.

---

## 9. Decision Rules a Downstream LLM Can Execute

These are operational "Prefer X unless Y" rules. The downstream resume-optimization LLM can apply these directly.

### Format and ATS rules

- **Prefer single-column** unless the candidate is submitting only to a verified channel that preserves parsing order; otherwise treat multi-column as **high risk**.
- **Always avoid** tables, text boxes, graphics, icons, skill bars, and headers/footers containing critical info for any internship or new-grad tech resume targeting ATS pipelines.
- **Use standard headings** ("Experience", "Education", "Projects", "Skills") unless the employer explicitly requests different wording.
- **Prefer PDF** for consistent rendering **unless** the portal auto-parses into form fields and the PDF produces incorrect mapping; then prefer DOCX.
- **If evidence is mixed, default to the low-risk choice:** keep both PDF and DOCX, choose based on portal preview/auto-fill behavior.
- **If using any non-standard or downloaded font**, replace with a common system font.
- **Body font:** 11pt default, 10.5–12pt acceptable range.
- **Margins:** 0.75" default, 0.5"–1.0" acceptable range.
- **Line spacing:** 1.0 within bullets, with explicit space between sections.
- **Color:** none by default; if used, one dark low-saturation color in name and headers only, never in body, never to encode meaning.

### Scanning and hierarchy rules

- **Bold job titles, companies, and section headers** to create scan anchors. Be consistent.
- **Avoid underline** because it resembles hyperlinks.
- **If content feels dense**, cut low-signal bullets before reducing whitespace. Clutter is penalized.

### Structure rules

- **For internship and new-grad candidates, prioritize Education near the top** (often above Experience if work experience is limited or not strongly brand-recognizable).
- **Prefer Experience before Projects** unless projects are significantly stronger and more role-aligned than work history.
- **Use a Summary only if** it adds targeting value in ≤2 lines and contains role-relevant keywords and concrete claims; otherwise omit.
- **Include Relevant Coursework** under Education only if 0–2 lines and directly matching the role and the candidate lacks aligned experience.

### Bullets and skills rules

- **Prefer 1–2 line bullets** unless a bullet contains essential technical constraints that cannot fit; never use paragraph bullets.
- **Include keywords in context;** never keyword-stuff.
- **List only skills that are evidenced** elsewhere in the resume. If a skill appears only in Skills and nowhere else, treat it as lower-credibility and consider removal.
- **Skills count ceiling: 12–24** defensible items across 3–5 groupings.
- **Never use graphical proficiency indicators** (stars, bars, dots).
- **Avoid subjective proficiency labels** ("Proficient", "Familiar") unless objective and standardized (e.g., "Fluent in French").

### Projects and proof rules

- **If a project is listed, include at least one proof signal:** deployed link, GitHub repo, demo video, tests/CI, users.
- **Avoid listing too many projects;** prefer 2–4 high-quality, role-aligned projects for a one-page resume.
- **If a project looks like coursework**, differentiate it with deployment, scope, ownership clarity, or omit.

### International experience rules

- **Never downplay international experience.** Translate it into comparable signals: standard role titles, concise company context, mainstream stack, outcomes.
- **For Ontario applications**, do not assume "Canadian experience" is a legitimate requirement. As of 2026, it is legally restricted in covered job postings.
- **Anticipate AI screening disclosure** for Ontario applications under the 2026 rules.

### Adjacent factor rules

- **Ensure resume ↔ LinkedIn date/title alignment.** Inconsistencies harm credibility.
- **Include only clean linked profiles.** An empty GitHub link is worse than no link.
- **Cover letter:** Required → write one. Optional → maintain a 70% stable base, customize 30% only for high-priority roles.

### Tailoring rules

- **Tailor surgically, not comprehensively.** In order: title line → skills order → top 2–4 bullets → coursework if directly relevant.
- **Mirror job description vocabulary** in bullets when truthful, not in a separate keyword block.
- **Never introduce inconsistencies** between resume versions and LinkedIn.

### When evidence is mixed

- Default to the option that **cannot materially harm parsing** and is **unlikely to be penalized by humans**, unless the application channel clearly favors the other.

---

## 10. High-Confidence Do / Don't Checklist

Ranked by lowest risk and highest expected value for this candidate profile.

### Do (ranked)

1. **Use single-column ATS-safe formatting** with standard headings
2. **Make titles, dates, and employers instantly scannable;** keep layout simple with adequate whitespace
3. **Engineer the top quarter of page one** to communicate fit and strongest evidence within 10–15 seconds
4. **Write bullets for detail, clarity, structure** — specific nouns plus outcomes
5. **Keep a concise skills section** (12–24 items, 3–5 groupings) reinforced by bullets and projects
6. **Maintain both PDF and DOCX exports** and choose per portal behavior
7. **Provide proof signals for projects** — deployed link, GitHub, README, tests, demo
8. **Align resume claims with public profiles** — keep LinkedIn and GitHub professional and matching
9. **Bold job titles and section headers** to create scan anchors
10. **Include Education near the top** for current students
11. **Use a common system font** (Arial, Calibri, Garamond, Times New Roman, Helvetica)
12. **Body 11pt, margins 0.75", line spacing 1.0** as safe defaults
13. **Tailor surgically** for each application: title, skills, top 2–4 bullets
14. **Frame international experience** with standard titles, mainstream stack, and concrete outcomes
15. **Include 1–3 links maximum** (LinkedIn, GitHub, optional portfolio)

### Don't (highest-risk mistakes)

1. **Don't use columns, tables, text boxes, graphics, icons, or skill bars** for layout
2. **Don't put critical info in headers/footers** — many ATS drop them
3. **Don't keyword-stuff** or rely on buzzwords without proof
4. **Don't write paragraph-length bullets** or overly dense text blocks
5. **Don't include public links you wouldn't want screened** — digital footprint affects evaluation
6. **Don't use graphical proficiency indicators** (stars, bars, dots)
7. **Don't include a photo, DOB, marital status, SIN/SSN, or other personal data**
8. **Don't fabricate metrics** or include unverifiable claims
9. **Don't list skills you can't defend** in an interview
10. **Don't use uncommon or downloaded fonts**
11. **Don't underline body text** — it resembles hyperlinks
12. **Don't sacrifice scannability for content volume** (no ultra-small fonts, no cramped spacing)
13. **Don't ignore parse-to-form behavior** — test in actual portals when possible
14. **Don't downplay international experience** or hide it
15. **Don't write resume content that "reads like marketing"** rather than engineering

---

## 11. Open Questions and Weak-Evidence Areas

These are areas where Tier 1 evidence specifically about resume performance (as opposed to general hiring or general readability) is limited. Items partially resolved in v2 are noted.

1. **Exact optimal font family and point size for resumes.** Strong general readability literature exists (Richardson 2022 verified the screen/small-size caveat — see Section 3.C), but direct resume-outcome experiments at typical resume sizes are still sparse. **Partially resolved in v2.**

2. **Best section order by tech subdomain** with causal evidence. Most guidance is convention and practitioner belief. `[insufficient data]`

3. **Measured causal impact of a Summary section** for entry-level tech resumes. Evidence favors clarity/structure overall, but summary-specific experiments are limited. `[insufficient data]`

4. **Canada vs US resume length norms in tech internships.** Institutional guidance varies (one page vs up to two), and tech-specific causal evidence is limited. `[insufficient data]`

5. **Measured effect of including a GitHub link on callback rates.** Targeted research in v2 confirmed no causal field study exists. The closest evidence is Abou El-Komboz & Goldbeck (2024, ifo Working Paper) showing developers' GitHub activity rises during job-search periods, consistent with signaling — but not a direct callback measurement. `[insufficient data]` for callback effect; the "empty GitHub may be worse than no link" claim remains inference. **Confirmed gap in v2.**

6. **Exact "ideal" bullet count per role and exact lines per bullet.** Targeted research in v2 confirmed that eye-tracking studies operate at section/area-of-interest level (Pina et al. 2023; Törngren et al. 2024), not bullet-count level. The "3–5 bullets" rule remains time-budget convention, not measured optimum. **Confirmed gap in v2.**

7. **Universal PDF vs DOCX superiority.** Evidence varies by platform and portal. The dual-format strategy is the operational answer.

8. **Cover letter causal impact for tech internships specifically.** Targeted research in v2 found no Canada/US tech-intern field experiment. The closest evidence is Cui, Dias, Ye (2025, arXiv) on online labor markets and Google Careers' explicit "cover letter optional" Help Center guidance. Tech-intern-specific causal evidence is still missing. **Confirmed gap in v2; partially anchored by Google's operational signal.**

9. **Density tolerance thresholds (words per page, bullets per role) before readability collapses.** No empirical thresholds in resume literature. `[insufficient data]`

10. **Technical vs non-technical recruiter scanning patterns.** Studies measure aggregate recruiter behavior; clean separation by recruiter type is missing. `[insufficient data]`

11. **GPA inclusion threshold — partially resolved in v2.** NACE Job Outlook 2023 establishes a median screening cutoff of ~3.0/4.0 among employers that screen, and multiple university career centers converge on the same threshold. What is still missing is a causal study showing that *including* GPA above 3.0 actually changes callback rates relative to omitting it. The 3.0 anchor is now well-grounded as a screening threshold; the optimal *display* decision above 3.0 remains convention.

12. **Causal effect of profile inconsistency (resume vs LinkedIn) on callback rates.** Digital footprint research shows correlation; field studies are limited.

13. **Empirical effect of personal websites on tech intern outcomes.** Largely conventional wisdom; no causal studies in this corpus.

14. **The Robert Half 2026 finding** that 61% of HR leaders report AI-generated applications slow hiring is self-reported survey data; the actual effect on candidate outcomes is unknown.

---

## 12. Categorized Source List

This bibliography is the cleaned, audited version. Sources are grouped by tier. Where prior reports used opaque internal tokens, sources have been re-identified with real titles, authors, years, and URLs where available.

### Tier 1 — Peer-reviewed empirical evidence on resume/CV screening and outcomes

**T1-01.** Wingate, T.G., Robie, C., Powell, D.M., & Bourdage, J.S. (2025). *The Signals That Matter: Resumes, Cover Letters, and Success on the Job Search*. **International Journal of Selection and Assessment** (Wiley). https://onlinelibrary.wiley.com/doi/10.1111/ijsa.70022
- Establishes: In a tracked Canadian co-op student dataset, resume and cover letter compositional quality (detail, clarity, structure) predicts more interviews per application and faster job acquisition, controlling for experience and tailoring.

**T1-02.** Lacroux, A., & Martin-Lacroux, C. (2022). *Should I Trust the Artificial Intelligence to Recruit? Recruiters' Perceptions and Behavior When Faced With Algorithm-Based Recommendation Systems During Resume Screening*. **Frontiers in Psychology**. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.895997/full
- Establishes: Experimental evidence (N≈694 professionals) that recruiter judgments are influenced by algorithmic vs human recommendations during screening.

**T1-03.** Törngren, S.O., Schütze, C., Van Belle, E., & Nyström, M. (2024). *"We choose this CV because we choose diversity" — What do eye movements say about the choices recruiters make?* **Frontiers in Sociology**. https://www.frontiersin.org/journals/sociology/articles/10.3389/fsoc.2024.1222850/full
- Establishes: Eye-tracking + dialog experiment with real recruiters showing how attention allocation differs across CV regions.

**T1-04.** Pina, A., Petersheim, C., Cherian, J., Lahey, J.N., Alexander, G., & Hammond, T. (2023). *Using Machine Learning with Eye-Tracking Data to Predict if a Recruiter Will Approve a Resume*. **Machine Learning and Knowledge Extraction** (MDPI). https://www.mdpi.com/2504-4990/5/3/38
- Establishes: Resume-screening eye-tracking features can predict pass/fail decisions; time spent viewing Experience and Education correlates with passing.

**T1-05.** Kuttal, S.K., Chen, X., Wang, Z., Balali, S., & Sarma, A. (2021). *Visual Resume: Exploring developers' online contributions for hiring*. **Information and Software Technology** (Elsevier). https://www.sciencedirect.com/science/article/abs/pii/S0950584921001002
- Establishes: Hiring evaluators use technical and soft-skill cues from GitHub and Stack Overflow but rely heavily on low-effort surface signals due to time constraints.

**T1-06.** Türker, N. (2025). *Digital footprints and recruitment: an experimental study on the impact of social media content on hiring decisions*. **Frontiers in Psychology**. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1693850/full
- Establishes: Social media content can shift perceived competence and fit and change hiring intentions in experimental settings.

**T1-07.** Varma, A., Toh, S.M., & Pichler, S. (2006). *Ingratiation in job applications: impact on selection decisions*. **Journal of Managerial Psychology** (Emerald). https://www-2.rotman.utoronto.ca/facbios/file/varma%2C%20toh%2C%20pichler.pdf
- Establishes: Impression management tactics in application letters can increase perceived qualifications.

**T1-08.** Härtel, T.M., Sorieh, S., Trzebiatowski, J.J.W., & Sonnentag, S. (2024). *"LinkedIn, LinkedIn on the screen, who is the greatest and smartest ever seen?" A machine learning approach using valid LinkedIn cues to predict narcissism and intelligence*. **Journal of Occupational and Organizational Psychology**. https://www.econstor.eu/bitstream/10419/313767/1/JOOP_JOOP12531.pdf
- Establishes: LinkedIn profiles contain measurable cues that can predict traits and influence judgments.

### Tier 2 — HCI / readability / typography / scanning research

**T2-01.** Rello, L., Pielot, M., & Marcos, M.-C. (2016). *Make It Big! The Effect of Font Size and Line Spacing on Online Readability*. **CHI 2016**. https://pielot.org/pubs/Rello2016-Fontsize.pdf
- Establishes: Font size and line spacing affect readability; extreme values impair comprehension.

**T2-02.** Wallace, S., Bylinskii, Z., Dobres, J., Kerr, B., Berlow, S., Treitman, R., Kumawat, N., Arpin, K., Miller, D.B., Huang, J., & Sawyer, B.D. (2022). *Towards Individuated Reading Experiences: Different Fonts Increase Reading Speed for Different Individuals*. **ACM Transactions on Computer-Human Interaction**. https://dl.acm.org/doi/10.1145/3502222
- Establishes: Font choice affects reading speed differently across individuals — no single best font.

**T2-03.** Nielsen, J. (2006, updated). *F-Shaped Pattern For Reading Web Content*. **Nielsen Norman Group**. https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/
- Establishes: Robust evidence for top/left bias in scanning digital content.

**T2-04.** W3C Web Accessibility Initiative. *Understanding Success Criterion 1.4.3: Contrast (Minimum)*. WCAG 2.2. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Establishes: Minimum contrast ratio of 4.5:1 for normal text.

**T2-05.** Vecino, S., Mehtali, J., de Andrés, J., Gonzalez-Rodriguez, M., & Fernandez-Lanvin, D. (2022). *How does serif vs sans serif typeface impact the usability of e-commerce websites?* **PeerJ Computer Science**. https://peerj.com/articles/cs-1139.pdf
- Establishes: Serif vs sans-serif effects are context-dependent and not universally large.

**T2-06.** Richardson, J.T.E. (2022). *The Legibility of Serif and Sans Serif Typefaces: Reading from Paper and Reading from Screens*. **SpringerBriefs in Education** (Open Access). https://link.springer.com/book/10.1007/978-3-030-90984-0
- Establishes: No consistent inherent legibility advantage for serif vs sans-serif in general reading on paper or screens. **Important caveat (from "General Conclusions to Part II", https://link.springer.com/chapter/10.1007/978-3-030-90984-0_15):** at very small type sizes or under low luminance, serif styles can be less legible because serifs may become faint or invisible. The book's "Coda: Lessons Learned" chapter (https://link.springer.com/chapter/10.1007/978-3-030-90984-0_16) summarizes the bottom-line conclusion.

**T2-07.** Minakata, K., & Beier, S. (2022). *The dispute about sans serif versus serif fonts: An interaction between the variables of serif and stroke contrast*. **Acta Psychologica**. https://doi.org/10.1016/j.actpsy.2022.103623
- Establishes: Serif vs sans-serif effects depend on stroke contrast and font characteristics rather than the serif/sans category itself. Corroborates Richardson (2022) and supports replacing simple serif-vs-sans rules with attention to font characteristics and reading conditions.

### Tier 3 — ATS / parser vendor documentation

**T3-01.** Textkernel. *Parser Output / Resume Quality (Tx Platform Resume Parser docs)*. https://developer.textkernel.com/tx-platform/v10/resume-parser/overview/parser-output/
- Establishes: Vendor-recognized resume artifacts including columns can degrade extraction.

**T3-02.** Textkernel. *File Formats (Resume/CV Parser)*. https://developer.textkernel.com/TKPlatform/master/file-formats/
- Establishes: Supported input formats include PDF, DOC, DOCX; OCR available for scanned input.

**T3-03.** Textkernel. *Improving Information Extraction from Column Resumes*. https://www.textkernel.com/learn-support/blog/improving-extraction-from-column-resumes/
- Establishes: Columns are common and difficult; extraction pipelines must explicitly handle them.

**T3-04.** Greenhouse Software. *Supported formats for resumes, cover letters and other candidate uploads*. https://support.greenhouse.io/hc/en-us/articles/360052218132
- Establishes: Common ATS accepts multiple formats; PDF vs DOCX is portal-dependent.

**T3-05.** Bullhorn. *Resume Parsing Basics*. https://kb.bullhorn.com/bh4sf/Content/BH4SF/Topics/resumeParsingBasics.htm
- Establishes: Highly formatted resumes may parse poorly or omit crucial information.

**T3-06.** Sovren (now Textkernel). *Tips for Electronic Resumes: How to Ensure that Automated Recruiting Software Can Read Your Resume* (2017). https://assets.ctfassets.net/u8jdxbed12ax/47PwcozRU4sqAUYAUu2Ga4/28deb18981fb4b73cb8532d0a2769ae6/TipsForElectronicResumes.pdf
- Establishes: Strong guidance against tables, columns, headers/footers, and graphics. **Note:** Contains an outdated "never use PDF" claim that conflicts with modern vendor acceptance.

**T3-07.** Google. *Apply for a job* (Google Careers Help Center). https://support.google.com/googlecareers/answer/6095391
- Establishes: Google's official application guidance explicitly states "cover letter [is] optional" in its application flow. This is one Tier 3 data point indicating that at least one major tech employer treats cover letters as optional inputs at the application stage. Does not prove cover letters are never read, but is concrete operational evidence about a major tech intern hiring funnel.

### Tier 4 — Institutional / government / reputable career guidance

**T4-01.** MIT Career Advising & Professional Development. *Resume checklist and worksheet*. https://capd.mit.edu/resources/resume-checklist/
- Establishes: Concrete formatting conventions (margins 0.5–1.0", font 10–12pt); warns against templates that may confuse ATS.

**T4-02.** University of Toronto Mississauga Career Centre. *Formatting Matters*. https://www.utm.utoronto.ca/careers/resume-cover-letter-resources/formatting-matters
- Establishes: Body font 11–12, margins ~¾"–1".

**T4-03.** University of Michigan Engineering Career Resource Center. *Resumes, CVs and Cover Letters*. https://career.engin.umich.edu/resumes-cvs-cover-letters/
- Establishes: Margins 0.5–1", impact statements 1–2 lines, consistency rules.

**T4-04.** University of Victoria Career Services. *Build your résumé (including ATS tips)*. https://www.uvic.ca/career-services/find-work/apply-for-jobs/resume-examples/
- Establishes: Body font size 11, headers 12–14, avoid underlining, no photos/DoB in Canada/US.

**T4-05.** University of Toronto Student Life Career Centre. *Resume and Cover Letter Toolkit*. https://studentlife.utoronto.ca/wp-content/uploads/CC-Resume-and-Cover-Letter-Toolkit.pdf
- Establishes: Canadian student resume conventions and tailoring guidance.

**T4-06.** Rotman Commerce (2021). *Resume Guide*. https://rotmancommerce.utoronto.ca/current-students/wp-content/uploads/sites/3/2021/03/Resume-Guide-2021.pdf
- Establishes: Name 2–3 sizes larger; full mailing address often unnecessary.

**T4-07.** Settlement.Org (2021). *What do I include in my Canadian resume?* https://settlement.org/ontario/employment/find-a-job/resume/what-do-i-include-in-my-canadian-resume-what-do-i-exclude/
- Establishes: Canadian norms for what to exclude (photo, age, SIN).

**T4-08.** Georgetown University Career Center. *Sharing Your Immigration Status*. https://careercenter.georgetown.edu/diversity-career-resources/international-students/job-search-in-the-us/sharing-your-immigration-status/
- Establishes: US employer can/can't ask guidance for international students.

**T4-09.** US Equal Employment Opportunity Commission. *Pre-Employment Inquiries and Citizenship*. https://www.eeoc.gov/pre-employment-inquiries-and-citizenship
- Establishes: Legal framing for pre-employment authorization inquiries.

**T4-10.** USAJOBS. *How do I write a resume for a federal job?* https://help.usajobs.gov/faq/application/documents/resume/what-to-include
- Establishes: Federal resume content requirements; "top quarter" and "10–15 second" guidance.

**T4-11.** Ontario Human Rights Commission (2013). *Removing the "Canadian experience" barrier — A guide for employers and regulatory bodies*. https://www3.ohrc.on.ca/en/removing-canadian-experience-barrier-guide-employers-and-regulatory-bodies
- Establishes: "Canadian experience" requirements can create discriminatory barriers.

**T4-12.** Government of Ontario (2023). *Ontario To Ban Requirements for Canadian Work Experience in Job Postings*. https://news.ontario.ca/en/release/1003798/ontario-to-ban-requirements-for-canadian-work-experience-in-job-postings
- Establishes: Policy direction restricting Canadian work experience requirements.

**T4-13.** Ontario Shared Services (2019). *Cover Letter and Résumé Writing Guide*. https://www.gojobs.gov.on.ca/docs/OPSCoverLetterandResumeWritingGuide.pdf
- Establishes: Font 10–12, standard fonts, electronic submission guidance.

**T4-14.** Region of Waterloo (2020). *Tips for Creating a Resume*. https://www.regionofwaterloo.ca/en/living-here/resources/Employment-and-Income-Support/Tips-for-Creating-a-Resume.pdf
- Establishes: Practical formatting suggestions, font size 11–12.

**T4-15.** Algonquin College Co-op and Career Centre. *Resume 101 (Resume Template PDF)*. https://www.algonquincollege.com/coop-career-centre/files/2024/05/CCC-Resume-Template.pdf
- Establishes: "Do not list skills/knowledge that cannot be supported by examples."

**T4-16.** UBC Applied Science (2023). *Cover Letter Toolkit for Engineering Students*. https://experience.apsc.ubc.ca/sites/default/files/2023-05/Cover%20Letter%20Toolkit%20for%20Engineering%20Students.pdf
- Establishes: Cover letter structure for technical roles.

**T4-17.** UC Davis Internship and Career Center. *Resumes*. https://careercenter.ucdavis.edu/resumes-and-materials/resumes
- Establishes: References should be a separate document; "available upon request" unnecessary.

**T4-18.** Government of Ontario (2024–2026). *Job posting obligations updates: Canadian experience prohibition and AI screening disclosure*. (Multiple law firm summaries available.)
- Establishes: Effective 2026, covered Ontario employers cannot require Canadian experience in publicly advertised postings; AI screening must be disclosed if used.

**T4-19.** University of Lethbridge Career Bridge. *Resume*. https://www.ulethbridge.ca/career-bridge/resume
- Establishes: Concrete convention for GPA inclusion: share overall GPA if 3.0 or higher; always include the scale.

**T4-20.** Carnegie Mellon University Tepper School of Business (2022). *Tepper Resume Guide*. https://www.cmu.edu/tepper/programs/career-center/_files/resume-guide.pdf
- Establishes: Convention-based GPA threshold rule — include GPA if 3.0 or above. One of multiple university career centers converging on the ~3.0 threshold.

### Tier 5 — Industry surveys, working papers, lower-weight sources

**T5-01.** TheLadders (2012). *Eye Tracking Online Metacognition: Cognitive Complexity and Recruiter Decision Making*. https://www.bu.edu/com/files/2018/10/TheLadders-EyeTracking-StudyC2.pdf
- Establishes: ~6 second initial screen claim; "six data points" attention pattern. **Note:** Marketing-adjacent industry report, not peer-reviewed.

**T5-02.** TheLadders (2018). *Eye-Tracking Study*. https://www.theladders.com/static/images/basicSite/pdfs/TheLadders-EyeTracking-StudyC2.pdf
- Establishes: ~7.4 second average initial screen; bold job titles work as anchors; clutter penalized. **Note:** Not peer-reviewed.

**T5-03.** Cui, J., Dias, G., & Ye, J. (2025). *Signaling in the Age of AI: Evidence from Cover Letters*. Working paper. https://arxiv.org/html/2509.25054v1
- Establishes: AI cover letter tools increase tailoring and callbacks but reduce signal value over time.

**T5-04.** Robert Half (2026). *New survey: 61% of HR leaders report AI-generated applications are slowing hiring*. https://press.roberthalf.ca/2026-03-10-New-survey-61-per-cent-of-HR-leaders-report-AI-generated-applications-are-slowing-hiring
- Establishes: Self-reported HR leader perception of AI application impact.

**T5-05.** Gartner (2025). *Gartner Survey Shows Just 26% of Job Applicants Trust AI Will Fairly Evaluate Them*. https://www.gartner.com/en/newsroom/press-releases/2025-07-31-gartner-survey-shows-just-26-percent-of-job-applicants-trust-ai-will-fairly-evaluate-them
- Establishes: Candidate trust in AI screening is low.

**T5-06.** National Association of Colleges and Employers (NACE). *Job Outlook 2023* (employer survey report). https://cdn.careerhub.students.duke.edu/wp-content/uploads/sites/128/2022/10/2023-nace-job-outlook.pdf
- Establishes: (a) Internships are the top differentiator when candidates are otherwise equal; (b) **median GPA screening cutoff is approximately 3.0/4.0** across industries, regions, and company sizes among employers that screen by GPA; (c) GPA screening exists but is not universal. NACE is the major US college hiring industry association; the report is hosted by Duke University Career Hub. **Verified in v2.**

**T5-07.** Harvard Business School & Accenture (2021). *Hidden Workers: Untapped Talent*. https://www.hbs.edu/managing-the-future-of-work/Documents/research/hiddenworkers09032021.pdf
- Establishes: Automated hiring systems often filter out candidates who could do the job but don't match criteria language closely.

**T5-08.** Abou El-Komboz, L., & Goldbeck, M. (2024). *Career Concerns As Public Good: The Role of Signaling for Open Source Software Development*. **ifo Working Paper No. 405** (ifo Institute Munich). https://www.ifo.de/DocDL/wp-2024-405_goldbeck_carreer%20concerns.pdf
- Establishes: Quasi-experimental evidence that developers' open-source contribution activity rises during job-search periods, consistent with developers themselves treating GitHub-visible work as a labor-market signal. Does not measure the resume-link inclusion effect directly. **Note:** URL contains a "carreer" typo in the actual filename — verify before external use.

---

## Corrections to prior reports (carried forward and v2)

**Carried forward from v1:**
- **The Sovren 2017 "never use PDF" claim is outdated.** Modern ATS vendors (Greenhouse, Workday, Bullhorn) accept PDF, and the 2017 absolute claim conflicts with current vendor reality. Treat as historical guidance, not current practice.
- **The "6 second" and "7.4 second" recruiter time figures are Tier 5 industry reports**, not peer-reviewed evidence. Use them as design constraints rather than universal facts. Peer-reviewed work cites broader ranges.
- **Tier 1 evidence on student outcomes (Wingate et al. 2025) is the strongest single piece of evidence in the corpus** and should be weighted accordingly when conflicts arise with anecdotal or survey data.

**New in v2:**
- **The simplified "no inherent serif vs sans-serif legibility difference" claim is too clean.** Richardson (2022) — the actual source — does conclude there is no general difference, but explicitly notes that **at very small type sizes or low luminance, serif strokes can become faint or invisible**. This applies directly to resumes read on screens at 10–11pt, where sans-serif is therefore marginally safer. The v1 claim has been refined, not discarded.
- **The popular "include GPA only if 3.5+" rule is convention without empirical support.** The only employer-side number with real survey backing is NACE Job Outlook 2023's median screening cutoff of ~3.0/4.0. Multiple university career centers converge on the same threshold. v2 has updated the GPA recommendation accordingly.
- **The previous T2-06 "scholarly monograph" placeholder citation has been resolved** to Richardson (2022), Springer Open Access. The previous note flagging it as needing verification has been removed.

---

# Where Further Research Would Help

This unified report integrates everything from four research passes and answers the original prompt's 13 topic areas (A through M) plus all 12 required output sections. It is operationally usable as-is for a downstream resume-optimization LLM. The targeted v2 follow-up resolved several high-priority gaps; remaining gaps are listed below with their current status.

## Resolved or partially resolved in v2

These gaps from v1 have been substantially addressed by the targeted follow-up research:

- **GPA inclusion threshold (v1 high-priority #1).** **Resolved.** NACE Job Outlook 2023 reports a median screening cutoff of ~3.0/4.0; multiple university career centers (Lethbridge, Algonquin, CMU Tepper, U of T Mississauga) converge on the same threshold. The popular "3.5+" rule is convention without empirical backing.
- **Typography monograph verification (v1 high-priority #5).** **Resolved.** The source is Richardson (2022), *The Legibility of Serif and Sans Serif Typefaces*, Springer Open Access. The claim has been refined: no general difference in legibility, but serif strokes can be less legible at very small sizes / low luminance — directly relevant to resume reading.
- **Cover letter causal impact for tech interns (v1 high-priority #4).** **Partially resolved.** Still no Canada/US tech-intern field experiment, but Google Careers' explicit "cover letter optional" Help Center guidance is now anchored as a Tier 3 data point. Cui, Dias, Ye 2025 remains the closest causal evidence from adjacent labor markets.
- **NACE source verification (v1 lower-priority #12).** **Resolved.** Job Outlook 2023 is now cited with a verifiable URL.
- **Empirical effect of GitHub link inclusion (v1 high-priority #2).** **Confirmed gap, but with new adjacent evidence.** The Abou El-Komboz & Goldbeck (2024) ifo working paper provides quasi-experimental evidence that developers' GitHub activity rises during job searches, consistent with signaling — but no direct field study on the resume-link inclusion effect on callbacks exists.

## Still genuinely unresolved (high-priority)

1. **Bullet count per role with empirical support.** Confirmed in v2 that eye-tracking studies operate at section level, not bullet level. The 3–5 convention has no empirical backing.

2. **Direct causal evidence for adding a GitHub URL → callback rates** for SWE interns specifically. Adjacent signaling evidence exists; the causal field experiment does not.

3. **Tech-intern-specific cover letter field experiments** in Canada/US. Adjacent evidence and one major employer's "optional" policy are now anchored, but the causal study is still missing.

## Medium-priority research gaps (carried forward from v1)

4. **Density tolerance thresholds** (words per page, bullets per role) before readability collapses. No empirical thresholds in resume literature.

5. **Technical vs non-technical recruiter scanning differences.** Studies measure aggregate behavior; clean type-by-type separation is missing.

6. **Personal website causal impact on tech intern outcomes.** Largely conventional wisdom; no causal studies in the corpus.

7. **Resume–LinkedIn inconsistency causal impact.** Digital footprint research shows correlation; field studies tying specific inconsistencies to callback rates are missing.

8. **Section length proportions on a one-page student resume.** What share of vertical space should Education vs Experience vs Projects vs Skills occupy? No source addresses this.

## Lower-priority polish items

9. **Action verb lists** validated as effective rather than convention-recommended.

10. **Robert Half 2026 survey methodology** to assess how reliable the "61% report AI slowing hiring" figure actually is.

11. **Empirical comparison of resume formats accepted by specific major company portals** (Workday at large enterprises, Greenhouse at startups, etc.) — a portal-by-portal evidence base would improve the PDF-vs-DOCX decision rule.

12. **Verification of two URLs** in the v2 bibliography:
    - The ifo working paper URL contains "carreer" (typo); confirm whether the actual filename has the typo or whether the URL needs correction
    - The Frontiers PDF URL on the `public-pages-files-2025.frontiersin.org` subdomain is unusual; confirm or replace with the standard `frontiersin.org` URL

## Topic-specific notes

- **Section A (Recruiter behavior):** The recruiter-type breakdown (technical vs non-technical vs hiring manager vs engineer) is currently inference-heavy. A targeted study would help.
- **Section C (Typography):** Body size, margin, and spacing numbers are convention-based safe defaults, not experimentally proven optima. The serif vs sans recommendation is now evidence-anchored to Richardson (2022).
- **Section D (Structure):** Role-family playbooks are mostly inference. The SWE playbook is best-evidenced; cloud, IT, data, HCI/UX, and QA playbooks lean on convention.
- **Section H (Tailoring):** Subdomain-specific keyword density tolerance is entirely inference. This remains the weakest evidence area in the entire dossier.
- **Section J (Adjacent factors):** The cover letter recommendation now anchors on three sources — Wingate et al. 2025 (general student outcomes), Cui/Dias/Ye 2025 (working paper, online labor market), and Google Careers' explicit "optional" Help Center policy (Tier 3). Tech-intern-specific causal evidence would still strengthen this materially.

## Bottom line on research completeness

This v2 dossier covers every topic and sub-topic from the original prompt with at least some evidence and operational guidance. The targeted v2 follow-up resolved or partially resolved five high-priority gaps from v1: GPA threshold, typography monograph verification, GitHub link evidence base, cover letter tech-intern anchoring, and NACE source verification. Where evidence remains thin, it is marked `[insufficient data]` or `(inference)`. The downstream resume-optimization LLM can apply this report immediately and should treat the inference-heavy sections (role-family playbooks, subdomain tailoring tolerances, recruiter-type differences, density thresholds) as conventions to follow rather than empirically proven rules. The remaining gaps are now mostly medium- and lower-priority items that would represent polish rather than substantive improvement.
