from pathlib import Path

import pandas as pd


def main():
    df = pd.read_csv("data/processed/companies_classified.csv")

    report_path = Path("reports/market_overview.md")

    lines = [
        "# Saudi Market Overview",
        "",
        "ملخص أولي لتصنيف الشركات المدرجة في عينة المشروع.",
        "",
        "## Summary",
        "",
        f"- عدد الشركات: {len(df)}",
        f"- عدد القطاعات: {df['sector'].nunique()}",
        f"- عدد تصنيفات الأعمال: {df['business_class'].nunique()}",
        f"- عدد ثيمات رؤية 2030: {df['vision2030_theme'].nunique()}",
        "",
        "## Companies by sector",
        "",
    ]

    sector_counts = df["sector"].value_counts()

    for sector, count in sector_counts.items():
        lines.append(f"- {sector}: {count}")

    lines.extend([
        "",
        "## Companies by business class",
        "",
    ])

    class_counts = df["business_class"].value_counts()

    for business_class, count in class_counts.items():
        lines.append(f"- {business_class}: {count}")

    lines.extend([
        "",
        "## Companies by Vision 2030 theme",
        "",
    ])

    theme_counts = df["vision2030_theme"].value_counts()

    for theme, count in theme_counts.items():
        lines.append(f"- {theme}: {count}")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    main()
