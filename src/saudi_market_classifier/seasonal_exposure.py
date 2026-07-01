"""طبقة التعرّض الموسمي (Phase 6 — Seasonal Exposure Layer).

تعرّض موضوعي/نموذج-عمل لموسمي الحج ورمضان فقط. لا ادعاء باستفادة مضمونة أو
عقود أو أثر إيرادي أو ارتفاع سعري. ليست توصية استثمارية.
"""

from pathlib import Path

import pandas as pd


COMPANIES_CSV = "data/reference/companies.csv"
SEASONAL_CSV = "data/reference/seasonal_exposures.csv"
OUTPUT_CSV = "data/processed/companies_seasonal_exposure.csv"
REPORT_PATH = Path("reports/seasonal_exposure_report.md")

WARNING = (
    "> **تنبيه:** هذا التقرير يعرض **تعرّضًا موسميًا محتملًا / ربطًا موضوعيًا "
    "(thematic linkage)** بناءً على نموذج العمل فقط. لا يدّعي استفادة مضمونة أو "
    "عقودًا أو أثرًا إيراديًا، وليس توصية استثمارية."
)


def _ranked(series):
    """قائمة (label, count) مرتبة: العدد تنازليًا ثم الاسم تصاعديًا (tie-break ثابت)."""
    counts = series.value_counts()
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def main():
    companies = pd.read_csv(COMPANIES_CSV, dtype={"symbol": str})
    seasonal = pd.read_csv(SEASONAL_CSV, dtype={"symbol": str})

    df = seasonal.merge(companies[["symbol", "name_ar"]], on="symbol", how="left")
    df["name_ar"] = df["name_ar"].fillna("")

    # ترتيب ثابت للمخرجات (حتمي).
    df = df.sort_values(["season", "symbol"]).reset_index(drop=True)

    ordered_cols = ["symbol", "name_ar"] + [
        c for c in seasonal.columns if c != "symbol"
    ]
    Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    df[ordered_cols].to_csv(OUTPUT_CSV, index=False)

    total = len(df)
    hm = df[df["exposure_level"].isin(["high", "medium"])].sort_values(
        ["season", "symbol"]
    )
    needs_verify = df[df["evidence_status"] == "needs_verification"].sort_values(
        ["season", "symbol"]
    )
    missing_rationale = df[
        df["exposure_level"].isin(["high", "medium"])
        & df["rationale"].apply(lambda v: pd.isna(v) or str(v).strip() == "")
    ].sort_values(["season", "symbol"])

    lines = [
        "# تقرير التعرّض الموسمي (Seasonal Exposure)",
        "",
        WARNING,
        "",
        "الموسمان: الحج (HAJJ)، رمضان (RAMADAN). ربط موضوعي محافظ من نموذج العمل فقط.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي صفوف التعرّض | {total} |",
        f"| تعرّض high/medium | {len(hm)} |",
        f"| صفوف needs_verification | {len(needs_verify)} |",
        f"| high/medium بدون rationale | {len(missing_rationale)} |",
        "",
        "## التوزيع حسب season",
        "",
        "| season | العدد |",
        "|---|---:|",
    ]
    for k, c in _ranked(df["season"]):
        lines.append(f"| {k} | {c} |")

    lines.extend(["", "## التوزيع حسب exposure_level", "",
                  "| exposure_level | العدد |", "|---|---:|"])
    for k, c in _ranked(df["exposure_level"]):
        lines.append(f"| {k} | {c} |")

    lines.extend(["", "## التوزيع حسب primary_driver", "",
                  "| primary_driver | العدد |", "|---|---:|"])
    for k, c in _ranked(df["primary_driver"]):
        lines.append(f"| {k} | {c} |")

    lines.extend(["", "## التوزيع حسب confidence", "",
                  "| confidence | العدد |", "|---|---:|"])
    for k, c in _ranked(df["confidence"]):
        lines.append(f"| {k} | {c} |")

    lines.extend(["", "## تعرّض high/medium", "",
                  "| symbol | name_ar | season | exposure | primary_driver | confidence |",
                  "|---|---|---|---|---|---|"])
    for _, r in hm.iterrows():
        lines.append(
            f"| {r['symbol']} | {r['name_ar']} | {r['season']} | "
            f"{r['exposure_level']} | {r['primary_driver']} | {r['confidence']} |"
        )

    lines.extend(["", "## صفوف needs_verification", ""])
    if len(needs_verify):
        lines.append("| symbol | name_ar | season | primary_driver |")
        lines.append("|---|---|---|---|")
        for _, r in needs_verify.iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['season']} | "
                f"{r['primary_driver']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.extend(["", "## high/medium بدون rationale", ""])
    if len(missing_rationale):
        lines.append("| symbol | name_ar | season | exposure |")
        lines.append("|---|---|---|---|")
        for _, r in missing_rationale.iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['season']} | "
                f"{r['exposure_level']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.extend([
        "",
        "## ملاحظات منهجية",
        "",
        "- المصدر القابل للتحرير: `data/reference/seasonal_exposures.csv`.",
        "- التعرّض مشتق من نموذج العمل فقط، لا من عقود أو إفصاحات مالية.",
        "- كل تعرّض high/medium يتطلب rationale؛ غير الكافي يُخفَّض أو يُعلَّم needs_verification.",
        "- المجموعة الابتدائية محافظة: روابط موضوعية واضحة فقط، وليست تغطية شاملة.",
        "",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء طبقة التعرّض الموسمي: {OUTPUT_CSV} + {REPORT_PATH}")


if __name__ == "__main__":
    main()
