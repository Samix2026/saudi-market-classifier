"""طبقة الذكاء السوقي (Market Intelligence Taxonomy) — Phase 2.

تربط التصنيف الأساسي بطبقة "التعرّض المحتمل" (potential exposure) للفعاليات
الكبرى (إكسبو 2030 الرياض، كأس العالم 2034) اعتمادًا على القطاع ونموذج العمل فقط.

تنبيه: هذه الطبقة موضوعية (thematic linkage) وليست تعاقدية. لا تدّعي استفادة
مباشرة أو عقودًا.
"""

from pathlib import Path

import pandas as pd


CLASSIFIED_CSV = "data/processed/companies_classified.csv"
EXPOSURES_CSV = "data/reference/mega_event_exposures.csv"
OUTPUT_CSV = "data/processed/companies_intelligence.csv"

EXPOSURE_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}
RANK_EXPOSURE = {v: k for k, v in EXPOSURE_RANK.items()}

EXPOSURE_COLS = [
    "expo2030_exposure",
    "worldcup2034_exposure",
    "primary_event_driver",
    "secondary_event_driver",
    "exposure_strength",
    "confidence",
    "rationale",
]

DEFAULTS = {
    "expo2030_exposure": "none",
    "worldcup2034_exposure": "none",
    "primary_event_driver": "none",
    "secondary_event_driver": "none",
    "exposure_strength": "none",
    "confidence": "low",
    "rationale": "",
}


def _overall(expo, worldcup):
    """أعلى تعرّض بين الفعاليتين (tie-break ثابت عبر سلم رتب صريح)."""
    rank = max(EXPOSURE_RANK.get(expo, 0), EXPOSURE_RANK.get(worldcup, 0))
    return RANK_EXPOSURE[rank]


def main():
    df = pd.read_csv(CLASSIFIED_CSV, dtype={"symbol": str})

    exposures = pd.read_csv(EXPOSURES_CSV, dtype={"symbol": str})
    # نأخذ عمود الرمز وأعمدة التعرّض فقط؛ الاسم يأتي من التصنيف الأساسي.
    exposures = exposures[["symbol"] + EXPOSURE_COLS]

    merged = df.merge(exposures, on="symbol", how="left")

    for col, default in DEFAULTS.items():
        merged[col] = merged[col].fillna(default)

    merged["event_exposure_overall"] = [
        _overall(e, w)
        for e, w in zip(merged["expo2030_exposure"], merged["worldcup2034_exposure"])
    ]

    Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_CSV, index=False)
    print(f"تم إنشاء طبقة الذكاء السوقي: {OUTPUT_CSV} ({len(merged)} صف)")


if __name__ == "__main__":
    main()
