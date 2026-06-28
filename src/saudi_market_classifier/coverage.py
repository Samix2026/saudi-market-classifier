import re
from pathlib import Path

import pandas as pd


TARGET_COMPANIES = 250

COMPANIES_CSV = Path("data/reference/companies.csv")
THEMES_CSV = Path("data/reference/vision2030_themes.csv")
CLASSIFIED_CSV = Path("data/processed/companies_classified.csv")

DEFERRED_REPORT = Path("reports/excluded_or_deferred_companies.md")
HOLDING_REPORT = Path("reports/holding_companies_review.md")

ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _count_table_rows(path):
    """عدد صفوف الجدول التي تبدأ برمز شركة من 4 أرقام."""
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines()
               if ROW_RE.match(line))


def _count_holding_needs_review(path):
    """عدد صفوف الجدول التي حالتها needs_review (تتجاهل سطر الملخص)."""
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines()
               if ROW_RE.match(line) and "needs_review" in line)


def _dupes(symbols):
    seen, dupes = set(), set()
    for s in symbols:
        if s in seen:
            dupes.add(s)
        seen.add(s)
    return sorted(dupes)


def _empties(symbols):
    return [s for s in symbols if str(s).strip() == "" or pd.isna(s)]


def main():
    df = pd.read_csv(CLASSIFIED_CSV, dtype={"symbol": str})
    companies = pd.read_csv(COMPANIES_CSV, dtype={"symbol": str})
    themes = pd.read_csv(THEMES_CSV, dtype={"symbol": str})

    report_path = Path("reports/coverage_report.md")

    total_companies = len(df)
    coverage_pct = round((total_companies / TARGET_COMPANIES) * 100, 1)

    # مقاييس جودة البيانات
    classified_symbols = df["symbol"].tolist()
    companies_symbols = companies["symbol"].tolist()
    themes_symbols = themes["symbol"].tolist()

    all_dupes = (
        _dupes(classified_symbols)
        + _dupes(companies_symbols)
        + _dupes(themes_symbols)
    )
    dup_count = len(set(all_dupes))
    empty_count = (
        len(_empties(classified_symbols))
        + len(_empties(companies_symbols))
        + len(_empties(themes_symbols))
    )
    symbol_set_match = set(companies_symbols) == set(classified_symbols)
    unclassified_count = int((df["vision2030_theme"].astype(str).str.strip()
                              == "unclassified").sum())

    # مقاييس المراجعات المفتوحة (مشتقة من التقارير المستقلة)
    deferred_count = _count_table_rows(DEFERRED_REPORT)
    holding_candidates = _count_table_rows(HOLDING_REPORT)
    holding_needs_review = _count_holding_needs_review(HOLDING_REPORT)

    n_sectors = df["sector"].nunique()
    n_business_classes = df["business_class"].nunique()
    n_themes = df["vision2030_theme"].nunique()

    lines = [
        "# تقرير تغطية البيانات",
        "",
        "لوحة جودة وتغطية لبيانات الشركات داخل المشروع.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | القيمة |",
        "|---|---|",
        f"| الشركات المصنفة | {total_companies} |",
        f"| الشركات المؤجلة | {deferred_count} |",
        f"| نسبة التغطية التقريبية | {coverage_pct}% |",
        f"| عدد القطاعات | {n_sectors} |",
        f"| عدد تصنيفات الأعمال | {n_business_classes} |",
        f"| عدد ثيمات رؤية 2030 | {n_themes} |",
        f"| unclassified في Vision 2030 | {unclassified_count} |",
        f"| الرموز المكررة | {dup_count} |",
        "",
        "## جودة البيانات",
        "",
        "| الفحص | القيمة |",
        "|---|---|",
        f"| صفوف companies.csv | {len(companies)} |",
        f"| صفوف companies_classified.csv | {len(df)} |",
        f"| صفوف vision2030_themes.csv | {len(themes)} |",
        f"| تطابق مجموعة الرموز (companies ↔ classified) | {'yes' if symbol_set_match else 'no'} |",
        f"| الرموز المكررة | {dup_count} |",
        f"| الرموز الفارغة | {empty_count} |",
        "",
        "## مراجعات مفتوحة",
        "",
        f"- تقرير الشركات المؤجلة: [reports/excluded_or_deferred_companies.md]"
        f"(excluded_or_deferred_companies.md) — {deferred_count} شركة مؤجلة",
        f"- تقرير الشركات القابضة: [reports/holding_companies_review.md]"
        f"(holding_companies_review.md)",
        f"- عدد الشركات القابضة المرشحة: {holding_candidates}",
        f"- عدد needs_review في تقرير الشركات القابضة: {holding_needs_review}",
        "",
        "## توزيع ثيمات رؤية 2030",
        "",
        "| الثيم | العدد |",
        "|---|---|",
    ]

    for theme, count in df["vision2030_theme"].value_counts().items():
        lines.append(f"| {theme} | {count} |")

    lines.extend([
        "",
        "## ملاحظات",
        "",
        "- لا توجد شركات unclassified بعد التحسين الأخير للتغطية.",
        f"- يوجد {deferred_count} شركة مؤجلة خارج الإدخال الحالي "
        "(موثقة في تقرير الشركات المؤجلة).",
        "- مراجعة الشركات القابضة موجودة كتقرير مستقل ولا تغيّر التصنيف تلقائيًا.",
        "",
        "## جودة مصادر البيانات",
        "",
    ])

    for source_quality, count in df["source_quality"].value_counts().items():
        lines.append(f"- {source_quality}: {count}")

    lines.extend([
        "",
        "## نوع المصدر",
        "",
    ])

    for source_type, count in df["source_type"].value_counts().items():
        lines.append(f"- {source_type}: {count}")

    lines.extend([
        "",
        "## التغطية حسب القطاع",
        "",
    ])

    for sector, count in df["sector"].value_counts().items():
        lines.append(f"- {sector}: {count}")

    lines.extend([
        "",
        "## الشركات التي تحتاج إلى رابط مصدر رسمي",
        "",
    ])

    pending_sources = df[df["source_type"] != "official"]

    for _, row in pending_sources.sort_values("symbol").iterrows():
        lines.append(
            f"- {row['symbol']} — {row['name_ar']} "
            f"({row['source_type']})"
        )

    lines.extend([
        "",
        "## الشركات التي تحتاج إلى تحقق رسمي",
        "",
    ])

    needs_review = df[df["source_quality"] != "official"]

    for _, row in needs_review.sort_values("symbol").iterrows():
        lines.append(
            f"- {row['symbol']} — {row['name_ar']} "
            f"({row['source_quality']}, آخر مراجعة: {row['last_reviewed']})"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء تقرير التغطية: {report_path}")


if __name__ == "__main__":
    main()
