# Product Brief — Saudi Market Classifier

> **Disclaimer:** This project is for research and data organization only. It is
> **not investment advice** and contains no trading recommendations, price
> forecasts, or outcome-impact claims.
> للبحث وتنظيم البيانات فقط — ليست توصية استثمارية.

## What it is

A reference and market-intelligence layer over Saudi listed companies. It links
each company to its sector, business classification, Vision 2030 theme, and a set
of conservative, thematic intelligence layers (mega-event exposure, seasonal
exposure, index membership, source freshness), then consolidates everything into
one deterministic master matrix and a portable public data package.

## The problem it solves

Raw market listings tell you a company exists, but not how it maps to national
priorities, structural context, or thematic linkages. Analysts rebuild that
mapping by hand, inconsistently, with no audit trail. This project turns that
into a versioned, tested, reproducible dataset.

## Who it is for

- Researchers and analysts mapping the Saudi market by theme and structure.
- Data teams needing a clean, documented base layer to build on.
- Stakeholders who want an explainable, auditable market view.
- Future product builders (dashboard, read-only API, report generator).

## What makes it different

- **Deterministic:** same input → byte-identical output; no wall-clock in exports.
- **Conservative:** thematic linkage only; unverified items are marked, not assumed.
- **Tested:** every layer has data-quality tests; CI guards generated outputs.
- **Transparent:** each derived value traces back to an editable reference file.

## Current capabilities

- Company classification (sector, business class, Vision 2030 theme, source quality).
- Mega-event potential-exposure layer (Expo 2030, World Cup 2034).
- Seasonal potential-exposure layer (Hajj, Ramadan).
- Conservative index-membership layer.
- Source-freshness tracking and a consolidated review queue.
- Master market-intelligence matrix + portable public data package.
- Local read-only Streamlit dashboard.

## What it is not

- Not investment advice; no trading signals or price forecasts.
- Not a claim of company revenue impact, contracts, or assured outcomes.
- Not a real-time feed; it is a curated, reviewed, reproducible snapshot.

## Suggested product directions

- **Dashboard:** hosted, richer filters and drill-downs over the public package.
- **Read-only API:** serve the matrix and layers as documented JSON endpoints.
- **Research report generator:** templated thematic and sector briefings.
- **Data package:** published, versioned dataset with a manifest and dictionary.
