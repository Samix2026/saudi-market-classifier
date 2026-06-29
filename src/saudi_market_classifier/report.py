from pathlib import Path

import pandas as pd


def _pct(count, total):
    return round((count / total) * 100, 1) if total else 0.0


def _ranked(series):
    """قائمة (label, count) مرتبة: العدد تنازليًا ثم الاسم تصاعديًا (tie-break ثابت)."""
    counts = series.value_counts()
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def _dominant(series):
    """أكثر قيمة تكرارًا مع tie-break ثابت (الاسم تصاعديًا)."""
    return _ranked(series)[0][0]


def main():
    df = pd.read_csv("data/processed/companies_classified.csv", dtype={"symbol": str})

    report_path = Path("reports/market_overview.md")

    total = len(df)
    n_sectors = df["sector"].nunique()
    n_classes = df["business_class"].nunique()
    n_themes = df["vision2030_theme"].nunique()
    unclassified = int((df["vision2030_theme"].astype(str).str.strip()
                        == "unclassified").sum())

    sector_counts = _ranked(df["sector"])
    class_counts = _ranked(df["business_class"])
    theme_counts = _ranked(df["vision2030_theme"])

    top_sector, top_sector_n = sector_counts[0]
    top_class, top_class_n = class_counts[0]
    top_theme, top_theme_n = theme_counts[0]

    lines = [
        "# نظرة عامة على السوق السعودي المصنف",
        "",
        "_Generated from current dataset_",
        "",
        "## الملخص التنفيذي",
        "",
        f"يغطي هذا التقرير {total} شركة مصنّفة موزّعة على {n_sectors} قطاعًا، "
        f"و {n_classes} تصنيف نشاط، و {n_themes} ثيمًا من ثيمات رؤية 2030، "
        f"دون أي شركة غير مصنّفة. أكبر قطاع تمثيلًا هو \"{top_sector}\" "
        f"({top_sector_n} شركة).",
        "",
        "## المؤشرات الرئيسية",
        "",
        "| المؤشر | القيمة |",
        "|---|---|",
        f"| عدد الشركات | {total} |",
        f"| عدد القطاعات | {n_sectors} |",
        f"| عدد تصنيفات الأعمال | {n_classes} |",
        f"| عدد ثيمات رؤية 2030 | {n_themes} |",
        f"| غير مصنّف (unclassified) | {unclassified} |",
        f"| أكبر قطاع | {top_sector} ({top_sector_n}) |",
        f"| أكبر تصنيف نشاط | {top_class} ({top_class_n}) |",
        f"| أكبر ثيم رؤية 2030 | {top_theme} ({top_theme_n}) |",
        "",
        "## توزيع القطاعات",
        "",
        "| القطاع | عدد الشركات | النسبة % | أبرز تصنيف نشاط |",
        "|---|---:|---:|---|",
    ]

    for sector, count in sector_counts:
        top_bc = _dominant(df[df["sector"] == sector]["business_class"])
        lines.append(f"| {sector} | {count} | {_pct(count, total)} | {top_bc} |")

    lines.extend([
        "",
        "## توزيع تصنيفات الأعمال",
        "",
        "| تصنيف النشاط | عدد الشركات | النسبة % |",
        "|---|---:|---:|",
    ])

    for business_class, count in class_counts:
        lines.append(f"| {business_class} | {count} | {_pct(count, total)} |")

    lines.extend([
        "",
        "## توزيع ثيمات رؤية 2030",
        "",
        "| الثيم | عدد الشركات | النسبة % |",
        "|---|---:|---:|",
    ])

    for theme, count in theme_counts:
        lines.append(f"| {theme} | {count} | {_pct(count, total)} |")

    # Highlights — tie-break ثابت في كلا الاتجاهين
    top5 = sector_counts[:5]
    bottom5 = sorted(sector_counts, key=lambda kv: (kv[1], str(kv[0])))[:5]

    lines.extend([
        "",
        "## أبرز الملاحظات (Highlights)",
        "",
        "**أكثر 5 قطاعات تمثيلًا:**",
        "",
    ])
    for sector, count in top5:
        lines.append(f"- {sector}: {count} ({_pct(count, total)}%)")

    lines.extend([
        "",
        "**أقل 5 قطاعات تمثيلًا:**",
        "",
    ])
    for sector, count in bottom5:
        lines.append(f"- {sector}: {count} ({_pct(count, total)}%)")

    lines.extend([
        "",
        "- تفاصيل جودة البيانات في [reports/coverage_report.md](coverage_report.md).",
        "- مراجعة الشركات القابضة في "
        "[reports/holding_companies_review.md](holding_companies_review.md).",
        "",
        "## القائمة التفصيلية حسب القطاع",
        "",
    ])

    for sector, group in df.groupby("sector"):
        count = len(group)
        dom_bc = _dominant(group["business_class"])
        dom_theme = _dominant(group["vision2030_theme"])
        lines.append(f"### {sector}")
        lines.append("")
        lines.append(f"- عدد الشركات: {count}")
        lines.append(f"- التصنيف الغالب: {dom_bc}")
        lines.append(f"- الثيم الغالب: {dom_theme}")
        lines.append("")
        for _, row in group.sort_values("symbol").iterrows():
            lines.append(
                f"- {row['symbol']} — {row['name_ar']} "
                f"({row['business_class']}, {row['vision2030_theme']})"
            )
        lines.append("")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء تقرير نظرة السوق: {report_path}")


if __name__ == "__main__":
    main()
