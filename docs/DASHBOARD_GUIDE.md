# Dashboard Guide — Saudi Market Classifier

> **Disclaimer:** The dashboard is for research and data organization only.
> This is **not investment advice**; no trading recommendations, price
> forecasts, or outcome-impact claims.

## Running it locally

From the repository root:

```bash
pip install -r requirements.txt   # includes streamlit
python3 run.py                    # refresh public/ if needed
streamlit run dashboard/app.py
```

Opens at `http://localhost:8501`. The dashboard is read-only: it never writes,
and connects to no API or database.

## Data source

It reads only the generated public data package:

- `public/datasets/market_intelligence_matrix.csv` — the displayed rows.
- `public/manifest.json` — package summary (schema_version, source_anchor_date,
  dataset count).

## KPI cards

- **Companies** — rows in the current (filtered) view.
- **Vision 2030 themes** — distinct themes present.
- **High/medium event exposure** — companies with mega-event exposure high or medium.
- **HAJJ exposure** / **RAMADAN exposure** — companies with non-`none` seasonal exposure.
- **Needing review** — companies with a real data-quality/exposure review signal
  (`review_priority` ≠ `none`).
- **Index verification pending** — companies whose index membership is still
  `needs_verification`.

## Filters

Sidebar multiselects narrow the whole view (KPIs, charts, table, profile):
sector, business_class, vision2030_theme, event_exposure_overall,
seasonal_hajj_exposure, seasonal_ramadan_exposure, classification_risk,
review_priority. Empty selection = no filter on that field.

## Charts

Simple count distributions: top-10 Vision 2030 themes (horizontal), event
exposure, classification risk, review priority, Hajj exposure, Ramadan exposure.

## Needing review vs Index verification pending

These are **different** signals, kept apart on purpose:

- **Needing review** = a data-quality or exposure issue to act on (missing
  rationale, low-confidence high/medium exposure, seasonal `needs_verification`).
- **Index verification pending** = a structural placeholder — index membership
  awaits an official dated snapshot. It is **not** a data-quality defect, so it
  does not inflate the review count.

## Known limitations

- Shows only the generated snapshot; run `run.py` first to refresh.
- Local only; no deployment, authentication, or sharing built in.
- Intelligence layers are thematic linkages, not measured impact.
