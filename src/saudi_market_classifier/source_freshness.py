"""طبقة حداثة المصادر (Phase 4 — Source Freshness Layer).

تقرير جودة بيانات يتتبع حداثة المصادر وتغطية المصادر الرسمية.

المصدر الأساسي للشركات: data/reference/companies.csv. تُضم حقول المصدر من ملفات
المرجع (official_sources.csv، source_quality.csv). طبقة إبلاغ — لا تغيّر التصنيف.

ملاحظة حتمية: التاريخ المرجعي ("اليوم") مُشتق من أحدث last_reviewed في البيانات،
وليس من ساعة النظام — حتى يبقى التقرير حتميًا ولا يسبّب CI drift.

تنبيه ثابت: تقرير جودة بيانات، وليس توصية استثمارية.
"""

from pathlib import Path

import pandas as pd


COMPANIES_CSV = "data/reference/companies.csv"
OFFICIAL_SOURCES_CSV = "data/reference/official_sources.csv"
SOURCE_QUALITY_CSV = "data/reference/source_quality.csv"
REPORT_PATH = Path("reports/source_freshness_report.md")

STALE_DAYS = 90

WARNING = (
    "> **تنبيه:** هذا تقرير جودة بيانات فقط، وليس توصية استثمارية ولا نصيحة مالية."
)


def _ranked(series):
    """قائمة (label, count) مرتبة: العدد تنازليًا ثم الاسم تصاعديًا (tie-break ثابت)."""
    counts = series.value_counts(dropna=False)
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def _is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def main():
    companies = pd.read_csv(COMPANIES_CSV, dtype={"symbol": str})
    official = pd.read_csv(OFFICIAL_SOURCES_CSV, dtype={"symbol": str})
    quality = pd.read_csv(SOURCE_QUALITY_CSV, dtype={"symbol": str})

    df = companies.merge(
        official[["symbol", "official_profile_url", "source_type"]],
        on="symbol", how="left",
    ).merge(
        quality[["symbol", "last_reviewed"]],
        on="symbol", how="left",
    )

    df["source_type"] = df["source_type"].fillna("pending")
    total = len(df)

    parsed = pd.to_datetime(df["last_reviewed"], format="%Y-%m-%d", errors="coerce")
    df["_reviewed"] = parsed

    # تاريخ مرجعي حتمي: أحدث last_reviewed في البيانات.
    reference_date = parsed.max()
    if pd.isna(reference_date):
        cutoff = None
        as_of = "غير متاح"
    else:
        cutoff = reference_date - pd.Timedelta(days=STALE_DAYS)
        as_of = reference_date.date().isoformat()

    missing_url = df[df["official_profile_url"].apply(_is_blank)]
    missing_reviewed = df[parsed.isna()]
    if cutoff is not None:
        stale = df[df["_reviewed"].notna() & (df["_reviewed"] < cutoff)]
    else:
        stale = df.iloc[0:0]

    lines = [
        "# تقرير حداثة المصادر (Source Freshness)",
        "",
        WARNING,
        "",
        f"التاريخ المرجعي (as of أحدث last_reviewed): **{as_of}** — "
        f"السجلات الأقدم من {STALE_DAYS} يومًا تُعدّ قديمة.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي الشركات | {total} |",
        f"| بدون official_profile_url | {len(missing_url)} |",
        f"| بدون last_reviewed (أو غير صالح) | {len(missing_reviewed)} |",
        f"| سجلات أقدم من {STALE_DAYS} يومًا | {len(stale)} |",
        "",
        "## التوزيع حسب source_type",
        "",
        "| source_type | العدد |",
        "|---|---:|",
    ]
    for source_type, count in _ranked(df["source_type"]):
        lines.append(f"| {source_type} | {count} |")

    lines.extend([
        "",
        f"## السجلات القديمة (أقدم من {STALE_DAYS} يومًا)",
        "",
    ])
    if len(stale):
        lines.append("| symbol | name_ar | last_reviewed | source_type |")
        lines.append("|---|---|---|---|")
        for _, r in stale.sort_values("symbol").iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['last_reviewed']} | "
                f"{r['source_type']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.extend([
        "",
        "## الشركات بدون رابط مصدر رسمي",
        "",
    ])
    if len(missing_url):
        lines.append("| symbol | name_ar | source_type |")
        lines.append("|---|---|---|")
        for _, r in missing_url.sort_values("symbol").iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['source_type']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.append("")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء تقرير حداثة المصادر: {REPORT_PATH}")


if __name__ == "__main__":
    main()
