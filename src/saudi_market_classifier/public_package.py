"""حزمة البيانات العامة (Phase 8 — Public Data Package).

تجمّع المخرجات المصنّفة وطبقات الذكاء في حزمة قابلة للمشاركة داخل مجلد public/
مع بيان (manifest) وقاموس بيانات وتنبيه ثابت.

حتمي بالكامل: تاريخ الحزمة مُشتق من أحدث last_reviewed (لا ساعة نظام).
حزمة بيانات وبحث — ليست توصية استثمارية.
"""

import json
from pathlib import Path

import pandas as pd


CLASSIFIED_CSV = "data/processed/companies_classified.csv"
PUBLIC_DIR = Path("public")
DATASETS_DIR = PUBLIC_DIR / "datasets"
REPORT_PATH = Path("reports/public_data_package_report.md")

SCHEMA_VERSION = "1.0"

DISCLAIMER = (
    "This dataset is provided for research, market-mapping and data-quality "
    "purposes only. It is NOT investment advice and contains no buy/sell "
    "recommendations, guaranteed-benefit, contract, or revenue-impact claims."
)
DISCLAIMER_AR = (
    "هذه البيانات لأغراض البحث ورسم خريطة السوق وجودة البيانات فقط. ليست توصية "
    "استثمارية ولا تتضمن توصيات شراء/بيع أو ادعاء استفادة أو عقود أو أثر إيرادي."
)

# (اسم الملف المصدر، وصف مختصر)
DATASETS = [
    ("companies_classified.csv",
     "التصنيف الأساسي: قطاع، تصنيف نشاط، ثيم رؤية 2030، جودة المصدر."),
    ("companies_intelligence.csv",
     "التصنيف + طبقة التعرّض المحتمل للفعاليات الكبرى."),
    ("companies_index_membership.csv",
     "عضوية مؤشرات السوق (بنية سوق محافظة)."),
    ("companies_seasonal_exposure.csv",
     "التعرّض الموسمي المحتمل (حج/رمضان)."),
    ("market_intelligence_matrix.csv",
     "المصفوفة الرئيسية: صف واحد لكل شركة يدمج كل الطبقات."),
]


def _anchor_date():
    classified = pd.read_csv(CLASSIFIED_CSV, dtype={"symbol": str})
    parsed = pd.to_datetime(
        classified["last_reviewed"], format="%Y-%m-%d", errors="coerce"
    )
    anchor = parsed.max()
    return "not_available" if pd.isna(anchor) else anchor.date().isoformat()


def _read_csv_meta(path):
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split(",")
        rows = sum(1 for _ in f)
    return header, rows


def main():
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    as_of = _anchor_date()

    manifest_datasets = []
    for filename, description in DATASETS:
        src = Path("data/processed") / filename
        header, rows = _read_csv_meta(src)
        # نسخة محمولة داخل الحزمة (نسخ بايتي حتمي).
        (DATASETS_DIR / filename).write_bytes(src.read_bytes())
        manifest_datasets.append({
            "file": f"datasets/{filename}",
            "description": description,
            "rows": rows,
            "columns": header,
        })

    manifest = {
        "name": "saudi-market-classifier-public-data",
        "schema_version": SCHEMA_VERSION,
        "source_anchor_date": as_of,
        "generated_from": "current dataset",
        "row_count_flagship": next(
            d["rows"] for d in manifest_datasets
            if d["file"].endswith("market_intelligence_matrix.csv")
        ),
        "datasets": manifest_datasets,
        "disclaimer": DISCLAIMER,
    }
    (PUBLIC_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    # قاموس البيانات.
    dd = ["# Data Dictionary — Saudi Market Classifier Public Data", "",
          f"> {DISCLAIMER}", "", f"_source_anchor_date (newest last_reviewed): {as_of}_", ""]
    for d in manifest_datasets:
        dd.append(f"## `{d['file']}` ({d['rows']} rows)")
        dd.append("")
        dd.append(d["description"])
        dd.append("")
        dd.append("| column |")
        dd.append("|---|")
        for col in d["columns"]:
            dd.append(f"| `{col}` |")
        dd.append("")
    (PUBLIC_DIR / "DATA_DICTIONARY.md").write_text(
        "\n".join(dd) + "\n", encoding="utf-8"
    )

    # README للحزمة.
    readme = [
        "# Saudi Market Classifier — Public Data Package", "",
        f"> {DISCLAIMER}", "",
        f"> {DISCLAIMER_AR}", "",
        f"- Schema version: `{SCHEMA_VERSION}`",
        f"- source_anchor_date (newest last_reviewed): `{as_of}`",
        f"- Datasets: {len(manifest_datasets)} (see `manifest.json`)",
        "",
        "## Contents", "",
        "| file | rows | description |",
        "|---|---:|---|",
    ]
    for d in manifest_datasets:
        readme.append(f"| `{d['file']}` | {d['rows']} | {d['description']} |")
    readme.extend([
        "",
        "See `manifest.json` (machine-readable) and `DATA_DICTIONARY.md` (columns).",
        "",
    ])
    (PUBLIC_DIR / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    # تقرير الحزمة.
    rep = [
        "# تقرير حزمة البيانات العامة (Public Data Package)", "",
        f"> **تنبيه:** {DISCLAIMER_AR}", "",
        f"إصدار المخطط: `{SCHEMA_VERSION}` — source_anchor_date المرجعي: **{as_of}**.",
        "",
        "## محتوى الحزمة", "",
        "| ملف | صفوف | أعمدة | وصف |",
        "|---|---:|---:|---|",
    ]
    for d in manifest_datasets:
        rep.append(
            f"| `{d['file']}` | {d['rows']} | {len(d['columns'])} | {d['description']} |"
        )
    rep.extend([
        "",
        "## ملاحظات منهجية", "",
        "- الحزمة مولّدة حتميًا من `data/processed/` (لا ساعة نظام).",
        "- التاريخ المرجعي مُشتق من أحدث `last_reviewed`.",
        "- الملفات في `public/` نسخ محمولة قابلة للمشاركة مع manifest وقاموس بيانات.",
        "- حزمة بحث وجودة بيانات — ليست توصية استثمارية.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(rep) + "\n", encoding="utf-8")

    print(f"تم إنشاء حزمة البيانات العامة: {PUBLIC_DIR}/ ({len(manifest_datasets)} ملف بيانات)")


if __name__ == "__main__":
    main()
