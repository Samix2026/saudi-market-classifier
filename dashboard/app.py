"""Saudi Market Intelligence Dashboard — local, read-only Streamlit app.

Reads only the generated public data package. No API, no database, no writes.
For research and data organization only, not investment advice.
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = ROOT / "public/datasets/market_intelligence_matrix.csv"
MANIFEST_PATH = ROOT / "public/manifest.json"

DISCLAIMER = (
    "This dashboard is for research and data organization only, "
    "not investment advice."
)

FILTER_COLS = [
    "sector",
    "business_class",
    "vision2030_theme",
    "event_exposure_overall",
    "seasonal_hajj_exposure",
    "seasonal_ramadan_exposure",
    "classification_risk",
    "review_priority",
]

# vision2030_theme handled separately (top 10, horizontal).
CHART_COLS = [
    ("event_exposure_overall", "Count by event exposure"),
    ("classification_risk", "Count by classification risk"),
    ("review_priority", "Count by review priority"),
    ("seasonal_hajj_exposure", "Count by HAJJ exposure"),
    ("seasonal_ramadan_exposure", "Count by RAMADAN exposure"),
]


@st.cache_data
def load_matrix():
    return pd.read_csv(MATRIX_PATH, dtype={"symbol": str})


@st.cache_data
def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def main():
    st.set_page_config(page_title="Saudi Market Intelligence Dashboard",
                       layout="wide")
    st.title("Saudi Market Intelligence Dashboard")
    st.caption(DISCLAIMER)
    st.info(DISCLAIMER)

    df = load_matrix()
    manifest = load_manifest()

    # Package summary from manifest.
    c1, c2, c3 = st.columns(3)
    c1.metric("schema_version", manifest.get("schema_version", "n/a"))
    c2.metric("source_anchor_date", manifest.get("source_anchor_date", "n/a"))
    c3.metric("datasets", len(manifest.get("datasets", [])))

    # Sidebar filters.
    st.sidebar.header("Filters")
    filtered = df.copy()
    for col in FILTER_COLS:
        options = sorted(df[col].dropna().unique().tolist())
        chosen = st.sidebar.multiselect(col, options)
        if chosen:
            filtered = filtered[filtered[col].isin(chosen)]

    # KPI cards (computed on filtered view).
    hm_event = filtered["event_exposure_overall"].isin(["high", "medium"]).sum()
    hajj = (filtered["seasonal_hajj_exposure"] != "none").sum()
    ramadan = (filtered["seasonal_ramadan_exposure"] != "none").sum()
    # "Needing review" = real data-quality / exposure review signals only.
    # review_priority no longer inherits index-membership needs_verification.
    needs_review = (filtered["review_priority"] != "none").sum()
    # Index membership pending is tracked as its own structural metric.
    index_pending = filtered["index_membership_summary"].str.contains(
        "needs_verification", na=False
    ).sum()

    r1 = st.columns(4)
    r1[0].metric("Companies", len(filtered))
    r1[1].metric("Vision 2030 themes", filtered["vision2030_theme"].nunique())
    r1[2].metric("High/medium event exposure", int(hm_event))
    r1[3].metric("HAJJ exposure", int(hajj))

    r2 = st.columns(4)
    r2[0].metric("RAMADAN exposure", int(ramadan))
    r2[1].metric("Needing review", int(needs_review))
    r2[2].metric("Index verification pending", int(index_pending))

    # Charts.
    st.subheader("Distributions")

    # Vision 2030 themes: top 10, horizontal for readability.
    st.caption("Top 10 Vision 2030 themes")
    theme_counts = filtered["vision2030_theme"].value_counts().head(10)
    try:
        st.bar_chart(theme_counts, horizontal=True)
    except TypeError:
        # Older Streamlit without the horizontal argument.
        st.bar_chart(theme_counts)

    chart_cols = st.columns(2)
    for idx, (col, label) in enumerate(CHART_COLS):
        counts = filtered[col].value_counts().sort_index()
        with chart_cols[idx % 2]:
            st.caption(label)
            st.bar_chart(counts)

    # Main filtered table.
    st.subheader("Companies")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # Company profile.
    st.subheader("Company profile")
    symbols = filtered["symbol"].tolist()
    if symbols:
        chosen_symbol = st.selectbox("Select a symbol", symbols)
        row = filtered[filtered["symbol"] == chosen_symbol].iloc[0]
        profile = row.to_frame(name="value")
        profile.index.name = "field"
        st.table(profile)
    else:
        st.write("No companies match the current filters.")

    st.caption(DISCLAIMER)


if __name__ == "__main__":
    main()
