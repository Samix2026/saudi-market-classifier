# Stakeholder Demo Script (3–5 minutes)

> **Disclaimer:** For research and data organization only. **Not investment
> advice**; no trading recommendations, price forecasts, or outcome-impact claims.

## Opening (20s)

"This project turns the Saudi listed market into a structured, tested,
reproducible intelligence layer — a clean base for research and future products.
It's for data organization and research, not investment advice."

## Problem (30s)

"Raw listings show that a company exists, but not how it maps to national
priorities or market structure. Analysts rebuild that by hand, inconsistently,
with no audit trail. We make it a versioned, tested dataset."

## What the repo does (45s)

"Each company is linked to its sector, business classification, and Vision 2030
theme, then enriched with conservative thematic layers: mega-event exposure,
seasonal exposure, index membership, and source freshness. Everything is
consolidated into one master matrix — one row per company."

## Show the public package (45s)

"Here's `public/` — a portable package: five datasets, a machine-readable
`manifest.json`, and a data dictionary. It uses a `source_anchor_date` derived
from the data, not a system clock, so exports are byte-identical every run."

## Show the dashboard (60s)

"Locally, `streamlit run dashboard/app.py` opens a read-only view: KPI cards,
sidebar filters, simple distribution charts, a company table, and per-company
profiles. Note two distinct signals — 'Needing review' for real data-quality
issues, and 'Index verification pending' for structural placeholders."

## Quality controls (45s)

"Every layer is tested — fixed company count, no duplicate symbols, allowed
values, rationale required for high/medium exposure, and fully deterministic
output. CI fails on any drift in generated files. Language is constrained to
thematic linkage; promotional or outcome-claim wording is blocked by tests."

## Next steps (30s)

"From here: a hosted dashboard, a read-only API, or a research-report generator —
all on the same reviewed, reproducible base. See `docs/ROADMAP.md`."
