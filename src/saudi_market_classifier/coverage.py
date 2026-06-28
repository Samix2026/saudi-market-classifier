from pathlib import Path

import pandas as pd


TARGET_COMPANIES = 250


def main():
    df = pd.read_csv("data/processed/companies_classified.csv")

    report_path = Path("reports/coverage_report.md")

    total_companies = len(df)
    coverage_pct = round((total_companies / TARGET_COMPANIES) * 100, 1)

    lines = [
        "# تقرير تغطية البيانات",
        "",
        "تقرير يوضح مستوى تغطية بيانات الشركات داخل المشروع.",
        "",
        "## الملخص",
        "",
        f"- الشركات الحالية: {total_companies}",
        f"- هدف التغطية التقريبي: {TARGET_COMPANIES}",
        f"- نسبة التغطية التقريبية: {coverage_pct}%",
        f"- عدد القطاعات المغطاة: {df['sector'].nunique()}",
        f"- عدد تصنيفات الأعمال: {df['business_class'].nunique()}",
        f"- عدد ثيمات رؤية 2030: {df['vision2030_theme'].nunique()}",
        "",
        "## جودة مصادر البيانات",
        "",
    ]

    for source_quality, count in df["source_quality"].value_counts().items():
        lines.append(f"- {source_quality}: {count}")

    lines.extend([
        "",
        "## التغطية حسب القطاع",
        "",
    ])

    for sector, count in df["sector"].value_counts().items():
        lines.append(f"- {sector}: {count}")

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
