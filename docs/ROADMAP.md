# Roadmap — Saudi Market Classifier

> **Disclaimer:** Planning document for a research/data-organization project.
> **Not investment advice**; no trading recommendations, price forecasts, or
> outcome-impact claims.

## Completed phases (1–10)

1. Core classification (sector, business class, Vision 2030 theme, source quality).
2. Market Intelligence Taxonomy — mega-event potential exposure (Expo 2030, WC 2034).
3. Review Queue layer — aggregated items needing human review.
4. Source Freshness layer — coverage and staleness tracking.
5. Index Membership layer — conservative market structure.
6. Seasonal Exposure layer — Hajj/Ramadan thematic linkage.
7. Market Intelligence Matrix — one master row per company across all layers.
8. Public Data Package — portable, self-contained dataset bundle.
9. Local Streamlit dashboard — read-only exploration.
10. Productization documentation — this docs set.

## Near-term next phases

- Verify and date index-membership constituents against an official snapshot.
- Expand seasonal/event coverage with reviewed, rationale-backed rows.
- Add per-layer changelogs and a data version bump on each reference edit.

## Possible product tracks

- Hosted dashboard.
- Read-only API over the matrix and layers.
- Templated research/report generator.
- Published, versioned data package.

## Data improvements

- Broaden source URLs and refresh cadence per record.
- Add confidence/evidence trails to more layers.
- Periodic holding-company and classification review cycles.

## Dashboard improvements

- Drill-down from KPI to filtered subset.
- Downloadable filtered views.
- Per-theme and per-sector summary pages.

## API track

- Read-only JSON endpoints for matrix, layers, and manifest.
- Documented schema and versioning; no write paths.

## Governance / review workflow

- Formalize review-priority triage and sign-off.
- Track reviewer, date, and source per verified item.
- Automate drift and freshness alerts in CI.

## Explicit out-of-scope

- Trading recommendations, price forecasts, or any outcome-impact claims.
- Real-time or intraday data.
- Portfolio construction or allocation guidance.
