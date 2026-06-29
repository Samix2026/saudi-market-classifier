"""تقرير التعرّض المحتمل للفعاليات الكبرى (Mega Event Exposure) — Phase 2.

يولّد reports/mega_event_exposure_report.md من data/processed/companies_intelligence.csv.

تنبيه ثابت: ربط موضوعي (thematic linkage) لا تعاقدي. لا ادعاء باستفادة مباشرة.
"""

from pathlib import Path

import pandas as pd


INTELLIGENCE_CSV = "data/processed/companies_intelligence.csv"
REPORT_PATH = Path("reports/mega_event_exposure_report.md")

RANK = {"high": 3, "medium": 2, "low": 1, "none": 0}


def _ranked(series):
    """قائمة (label, count) مرتبة: العدد تنازليًا ثم الاسم تصاعديًا (tie-break ثابت)."""
    counts = series.value_counts()
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def _exposure_rows(df, col):
    """صفوف ذات تعرّض high/medium للعمود، مرتبة: التعرّض تنازليًا ثم الرمز تصاعديًا."""
    sub = df[df[col].isin(["high", "medium"])].copy()
    sub = sub.sort_values(
        by=[col, "symbol"],
        key=lambda s: s.map(RANK) if s.name == col else s,
        ascending=[False, True],
    )
    return sub


def main():
    df = pd.read_csv(INTELLIGENCE_CSV, dtype={"symbol": str})
    total = len(df)

    expo_hm = _exposure_rows(df, "expo2030_exposure")
    wc_hm = _exposure_rows(df, "worldcup2034_exposure")
    any_exposed = df[df["event_exposure_overall"] != "none"]

    lines = [
        "# تقرير التعرّض المحتمل للفعاليات الكبرى",
        "",
        "> **تنبيه:** هذا التقرير يعرض **تعرّضًا محتملًا / ربطًا موضوعيًا "
        "(potential exposure / thematic linkage)** بناءً على القطاع ونموذج العمل فقط. "
        "لا يدّعي وجود عقود أو استفادة مباشرة أو أثر مضمون، وليس توصية استثمارية.",
        "",
        "الفعاليتان: Expo 2030 Riyadh، FIFA World Cup 2034 Saudi Arabia.",
        "",
        "## الملخص",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي الشركات | {total} |",
        f"| شركات ذات تعرّض محتمل (overall ≠ none) | {len(any_exposed)} |",
        f"| تعرّض Expo 2030 (high/medium) | {len(expo_hm)} |",
        f"| تعرّض World Cup 2034 (high/medium) | {len(wc_hm)} |",
        "",
        "## توزيع التعرّض الإجمالي (event_exposure_overall)",
        "",
        "| المستوى | العدد |",
        "|---|---:|",
    ]
    for level, count in _ranked(df["event_exposure_overall"]):
        lines.append(f"| {level} | {count} |")

    lines.extend([
        "",
        "## توزيع المحرّك الأساسي (primary_event_driver)",
        "",
        "| المحرّك | العدد |",
        "|---|---:|",
    ])
    for driver, count in _ranked(df[df["primary_event_driver"] != "none"]["primary_event_driver"]):
        lines.append(f"| {driver} | {count} |")

    lines.extend([
        "",
        "## Expo 2030 Riyadh — تعرّض محتمل (high/medium)",
        "",
        "| symbol | name_ar | exposure | primary_driver | confidence |",
        "|---|---|---|---|---|",
    ])
    for _, r in expo_hm.iterrows():
        lines.append(
            f"| {r['symbol']} | {r['name_ar']} | {r['expo2030_exposure']} | "
            f"{r['primary_event_driver']} | {r['confidence']} |"
        )

    lines.extend([
        "",
        "## FIFA World Cup 2034 — تعرّض محتمل (high/medium)",
        "",
        "| symbol | name_ar | exposure | primary_driver | confidence |",
        "|---|---|---|---|---|",
    ])
    for _, r in wc_hm.iterrows():
        lines.append(
            f"| {r['symbol']} | {r['name_ar']} | {r['worldcup2034_exposure']} | "
            f"{r['primary_event_driver']} | {r['confidence']} |"
        )

    lines.extend([
        "",
        "## ملاحظات منهجية",
        "",
        "- التعرّض مشتق من القطاع/نموذج العمل، وليس من عقود أو إعلانات شركات.",
        "- المستويات: high / medium / low / none. الثقة: high / medium / low.",
        "- الشركات غير المدرجة في `data/reference/mega_event_exposures.csv` "
        "تأخذ none/low افتراضيًا عند الدمج.",
        "- المصدر القابل للتحرير: `data/reference/mega_event_exposures.csv`.",
        "",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء تقرير التعرّض للفعاليات: {REPORT_PATH}")


if __name__ == "__main__":
    main()
