# Methodology — Saudi Market Classifier

> **Disclaimer:** Research and data-organization methodology only.
> This is **not investment advice**; no trading recommendations, price
> forecasts, or outcome-impact claims.

## Data sources and source-of-truth logic

- `data/reference/companies.csv` is the company universe (source of truth for rows).
- Per-attribute reference files hold the editable inputs: `business_classes.csv`,
  `vision2030_themes.csv`, `source_quality.csv`, `official_sources.csv`,
  `mega_event_exposures.csv`, `index_memberships.csv`, `seasonal_exposures.csv`.
- All processed CSVs and reports in `data/processed/` and `reports/` are
  **generated** from these references by `run.py`; never hand-edited.

## Classification approach

`business_class` is derived from `sector` via `business_classes.csv` (a join, not a
guess). Editing a company's classification means editing its official `sector`,
which requires source confirmation.

## Vision 2030 theme logic

`vision2030_theme` is mapped per company in `vision2030_themes.csv`. A conservative
sector→theme mapping seeded coverage; unmapped companies were resolved so zero
remain unclassified.

## Mega-event exposure methodology

Potential exposure to Expo 2030 and World Cup 2034 is inferred from sector and
business model only — a thematic linkage, never a contract or outcome claim. Every
high/medium row carries a rationale; a test blocks promotional or outcome-claim
vocabulary in rationales.

## Seasonal exposure methodology

Hajj and Ramadan potential exposure follows the same conservative rule: business
model linkage only, curated to obvious links, every high/medium row justified,
uncertain links marked `needs_verification`.

## Index membership methodology

A conservative market-structure layer. Constituents are not assumed: each company
is seeded as `TASI:needs_verification` pending an official dated snapshot. Allowed
index codes and membership statuses are validated by tests.

## Source freshness logic

Each record's `last_reviewed` is compared to a **data-derived anchor** (the newest
`last_reviewed` in the dataset). Older than 90 days from the anchor → `stale`;
missing/unparseable → `missing`; otherwise `current`. The anchor replaces any
system clock so the output is stable.

## Review priority and classification risk logic

Computed conservatively from reference data only:

- `review_priority`: `high` = high/medium exposure missing rationale; `medium` =
  seasonal `needs_verification` or low-confidence high/medium exposure; `low` =
  stale/missing freshness; `none` = no signal.
- Index-membership `needs_verification` is a **structural** signal, tracked
  separately, and deliberately excluded from `review_priority`.
- `classification_risk`: `high` if review_priority high; `medium` if review_priority
  medium or low-confidence high/medium exposure; else `low`.

## Determinism / no wall-clock policy

No export uses system time. Date-sensitive logic anchors to the newest
`last_reviewed`; the public package uses `source_anchor_date`, not a generated-at
timestamp. Aggregations sort with explicit tie-breakers (count desc, label asc) so
runs are byte-identical across machines and Python versions.

## Data quality tests

`tests/` enforces: fixed company count (259), no duplicate symbols, symbol-set
match across files, no unclassified themes, allowed values per layer, rationale
required for high/medium exposure, deterministic outputs, and disclaimer presence.
CI additionally fails on any drift in generated outputs.

## Limitations

- A curated, reviewed snapshot — not a real-time feed.
- Intelligence layers are thematic linkages, not measured impact.
- Index membership is pending official verification.
- Official sector values require source confirmation before change.
