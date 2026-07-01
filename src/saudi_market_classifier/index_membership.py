"""طبقة عضوية المؤشرات (Phase 5 — Index Membership Layer).

طبقة جودة بيانات وبنية سوق. تربط الشركات بعضوية مؤشرات السوق السعودي من ملف
مرجعي محافظ (لا تخمين للمكوّنات). طبقة إبلاغ — لا تغيّر التصنيف.

تنبيه ثابت: عضوية المؤشرات ليست توصية استثمارية.
"""

from pathlib import Path

import pandas as pd


COMPANIES_CSV = "data/reference/companies.csv"
MEMBERSHIPS_CSV = "data/reference/index_memberships.csv"
OUTPUT_CSV = "data/processed/companies_index_membership.csv"
REPORT_PATH = Path("reports/index_membership_report.md")

ALLOWED_INDEX_CODES = ["TASI", "MT30", "TASI50", "LARGE_CAP", "MID_CAP", "SMALL_CAP"]
ALLOWED_STATUS = ["member", "not_member", "needs_verification"]

WARNING = (
    "> **تنبيه:** عضوية المؤشرات معروضة لأغراض بنية السوق وجودة البيانات فقط، "
    "وليست توصية استثمارية ولا نصيحة مالية."
)


def _ranked(series, order=None):
    """قائمة (label, count) مرتبة: العدد تنازليًا ثم الاسم تصاعديًا (tie-break ثابت)."""
    counts = series.value_counts()
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def _is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def main():
    companies = pd.read_csv(COMPANIES_CSV, dtype={"symbol": str})
    memberships = pd.read_csv(MEMBERSHIPS_CSV, dtype={"symbol": str})

    # إثراء بالاسم العربي من مصدر الشركات (بنية سوق فوق التصنيف).
    df = memberships.merge(
        companies[["symbol", "name_ar"]], on="symbol", how="left"
    )
    df["name_ar"] = df["name_ar"].fillna("")

    # ترتيب ثابت للمخرجات.
    df = df.sort_values(["symbol", "index_code"]).reset_index(drop=True)

    ordered_cols = ["symbol", "name_ar"] + [
        c for c in memberships.columns if c != "symbol"
    ]
    Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    df[ordered_cols].to_csv(OUTPUT_CSV, index=False)

    total_rows = len(df)
    unique_symbols = df["symbol"].nunique()
    needs_verify = df[df["membership_status"] == "needs_verification"]
    missing_url = df[df["source_url"].apply(_is_blank)]

    lines = [
        "# تقرير عضوية المؤشرات (Index Membership)",
        "",
        WARNING,
        "",
        "طبقة بنية سوق محافظة تربط الشركات بمؤشرات السوق السعودي. المكوّنات غير "
        "المؤكدة تُعلَّم `needs_verification` بدل التخمين.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي الشركات (رموز فريدة) | {unique_symbols} |",
        f"| إجمالي صفوف العضوية | {total_rows} |",
        f"| تحتاج تحققًا (needs_verification) | {len(needs_verify)} |",
        f"| بدون source_url | {len(missing_url)} |",
        "",
        "## التوزيع حسب index_code",
        "",
        "| index_code | العدد |",
        "|---|---:|",
    ]
    for code, count in _ranked(df["index_code"]):
        lines.append(f"| {code} | {count} |")

    lines.extend([
        "",
        "## التوزيع حسب membership_status",
        "",
        "| membership_status | العدد |",
        "|---|---:|",
    ])
    for status, count in _ranked(df["membership_status"]):
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## الشركات التي تحتاج تحققًا (needs_verification)",
        "",
    ])
    if len(needs_verify):
        lines.append("| symbol | name_ar | index_code | confidence |")
        lines.append("|---|---|---|---|")
        for _, r in needs_verify.sort_values(["symbol", "index_code"]).iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['index_code']} | "
                f"{r['confidence']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.extend([
        "",
        "## صفوف بدون source_url",
        "",
    ])
    if len(missing_url):
        lines.append("| symbol | name_ar | index_code |")
        lines.append("|---|---|---|")
        for _, r in missing_url.sort_values(["symbol", "index_code"]).iterrows():
            lines.append(
                f"| {r['symbol']} | {r['name_ar']} | {r['index_code']} |"
            )
    else:
        lines.append("- لا يوجد.")

    lines.extend([
        "",
        "## ملاحظات منهجية",
        "",
        "- المصدر القابل للتحرير: `data/reference/index_memberships.csv`.",
        f"- قيم index_code المسموحة: {'، '.join(ALLOWED_INDEX_CODES)}.",
        f"- قيم membership_status المسموحة: {'، '.join(ALLOWED_STATUS)}.",
        "- لا يتم تخمين مكوّنات المؤشرات؛ غير المؤكد يُعلَّم needs_verification.",
        "- TASI مؤشر السوق الرئيسية الشامل؛ العضوية الدقيقة تحتاج لقطة رسمية مؤرخة.",
        "",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء طبقة عضوية المؤشرات: {OUTPUT_CSV} + {REPORT_PATH}")


if __name__ == "__main__":
    main()
