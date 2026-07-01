"""مصفوفة الذكاء السوقي (Phase 7 — Market Intelligence Matrix).

مصفوفة رئيسية حتمية تدمج التصنيف الأساسي مع كل طبقات الذكاء المبنية سابقًا
(التعرّض للفعاليات، عضوية المؤشرات، التعرّض الموسمي، حداثة المصدر) في صف واحد
لكل شركة.

طبقة ذكاء سوقي وجودة بيانات — ليست توصية استثمارية. لا لغة شراء/بيع ولا ادعاء
استفادة أو عقود أو أثر إيرادي.

كل التواريخ مُشتقة من البيانات (أحدث last_reviewed) وليست من ساعة النظام — حتمي.
"""

from pathlib import Path

import pandas as pd


CLASSIFIED_CSV = "data/processed/companies_classified.csv"
INTELLIGENCE_CSV = "data/processed/companies_intelligence.csv"
INDEX_CSV = "data/processed/companies_index_membership.csv"
SEASONAL_CSV = "data/processed/companies_seasonal_exposure.csv"

OUTPUT_CSV = "data/processed/market_intelligence_matrix.csv"
REPORT_PATH = Path("reports/market_intelligence_matrix.md")

STALE_DAYS = 90
HM = ("high", "medium")

MATRIX_COLS = [
    "symbol", "name_ar", "name_en", "sector", "business_class", "vision2030_theme",
    "event_exposure_overall", "primary_event_driver", "event_confidence",
    "seasonal_hajj_exposure", "seasonal_ramadan_exposure", "seasonal_primary_drivers",
    "index_membership_summary", "source_type", "source_freshness_status",
    "review_priority", "classification_risk",
]

WARNING = (
    "> **تنبيه:** مصفوفة ذكاء سوقي وجودة بيانات فقط. ليست توصية استثمارية ولا "
    "نصيحة مالية، ولا تتضمن لغة شراء/بيع أو ادعاء استفادة أو عقود أو أثر إيرادي."
)


def _ranked(series):
    counts = series.value_counts()
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def _blank(v):
    return pd.isna(v) or str(v).strip() == ""


def _freshness_map(classified):
    parsed = pd.to_datetime(
        classified["last_reviewed"], format="%Y-%m-%d", errors="coerce"
    )
    anchor = parsed.max()
    cutoff = None if pd.isna(anchor) else anchor - pd.Timedelta(days=STALE_DAYS)
    status = {}
    for sym, dt in zip(classified["symbol"], parsed):
        if pd.isna(dt):
            status[sym] = "missing"
        elif cutoff is not None and dt < cutoff:
            status[sym] = "stale"
        else:
            status[sym] = "current"
    return status


def main():
    classified = pd.read_csv(CLASSIFIED_CSV, dtype={"symbol": str})
    intelligence = pd.read_csv(INTELLIGENCE_CSV, dtype={"symbol": str})
    index_df = pd.read_csv(INDEX_CSV, dtype={"symbol": str})
    seasonal = pd.read_csv(SEASONAL_CSV, dtype={"symbol": str})

    freshness = _freshness_map(classified)

    intel = intelligence.set_index("symbol")

    # تجميع صفوف المؤشرات لكل رمز: "CODE:status" مرتّبة.
    index_by_symbol = {}
    for sym, grp in index_df.groupby("symbol"):
        pairs = sorted(f"{r['index_code']}:{r['membership_status']}"
                       for _, r in grp.iterrows())
        index_by_symbol[sym] = ";".join(pairs)

    # تجميع صفوف الموسمية لكل رمز.
    seasonal_by_symbol = {}
    for sym, grp in seasonal.groupby("symbol"):
        seasonal_by_symbol[sym] = list(grp.to_dict("records"))

    rows = []
    for _, c in classified.iterrows():
        sym = c["symbol"]

        # طبقة الفعاليات (من companies_intelligence).
        i = intel.loc[sym] if sym in intel.index else None
        if i is not None:
            event_overall = str(i.get("event_exposure_overall", "none"))
            primary_event_driver = str(i.get("primary_event_driver", "none"))
            expo = str(i.get("expo2030_exposure", "none"))
            wc = str(i.get("worldcup2034_exposure", "none"))
            event_conf_raw = str(i.get("confidence", "low"))
            event_rationale = "" if _blank(i.get("rationale")) else str(i.get("rationale"))
        else:
            event_overall = primary_event_driver = "none"
            expo = wc = "none"
            event_conf_raw = "low"
            event_rationale = ""
        event_is_hm = expo in HM or wc in HM
        event_confidence = event_conf_raw if event_overall != "none" else "not_available"

        # الطبقة الموسمية.
        srows = seasonal_by_symbol.get(sym, [])
        hajj = "none"
        ramadan = "none"
        drivers = set()
        seasonal_missing_rationale = False
        seasonal_needs_verify = False
        seasonal_lowconf_hm = False
        for s in srows:
            level = str(s["exposure_level"])
            season = str(s["season"])
            if season == "HAJJ":
                hajj = level
            elif season == "RAMADAN":
                ramadan = level
            drv = str(s["primary_driver"])
            if drv and drv != "none":
                drivers.add(drv)
            if level in HM and _blank(s.get("rationale")):
                seasonal_missing_rationale = True
            if str(s.get("evidence_status")) == "needs_verification":
                seasonal_needs_verify = True
            if level in HM and str(s.get("confidence")) == "low":
                seasonal_lowconf_hm = True
        seasonal_primary_drivers = ";".join(sorted(drivers)) if drivers else "none"

        # عضوية المؤشرات.
        index_summary = index_by_symbol.get(sym, "not_available")
        index_needs_verify = "needs_verification" in index_summary

        freshness_status = freshness.get(sym, "missing")

        # أولوية المراجعة (محافظة، بأسبقية high>medium>low>none).
        event_missing_rationale = event_is_hm and not event_rationale
        event_lowconf_hm = event_is_hm and event_conf_raw == "low"
        if event_missing_rationale or seasonal_missing_rationale:
            review_priority = "high"
        elif (index_needs_verify or seasonal_needs_verify
              or event_lowconf_hm or seasonal_lowconf_hm):
            review_priority = "medium"
        elif freshness_status in ("stale", "missing"):
            review_priority = "low"
        else:
            review_priority = "none"

        # مخاطر التصنيف.
        if review_priority == "high":
            classification_risk = "high"
        elif review_priority == "medium" or event_lowconf_hm or seasonal_lowconf_hm:
            classification_risk = "medium"
        else:
            classification_risk = "low"

        rows.append({
            "symbol": sym,
            "name_ar": c["name_ar"],
            "name_en": c["name_en"],
            "sector": c["sector"],
            "business_class": c["business_class"],
            "vision2030_theme": c["vision2030_theme"],
            "event_exposure_overall": event_overall,
            "primary_event_driver": primary_event_driver,
            "event_confidence": event_confidence,
            "seasonal_hajj_exposure": hajj,
            "seasonal_ramadan_exposure": ramadan,
            "seasonal_primary_drivers": seasonal_primary_drivers,
            "index_membership_summary": index_summary,
            "source_type": c["source_type"],
            "source_freshness_status": freshness_status,
            "review_priority": review_priority,
            "classification_risk": classification_risk,
        })

    matrix = pd.DataFrame(rows, columns=MATRIX_COLS).sort_values(
        "symbol"
    ).reset_index(drop=True)

    Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(OUTPUT_CSV, index=False)

    total = len(matrix)
    hm_risk = matrix[matrix["classification_risk"].isin(HM)].sort_values("symbol")

    def _dist(title, col):
        out = ["", f"## {title}", "", "| القيمة | العدد |", "|---|---:|"]
        for k, v in _ranked(matrix[col]):
            out.append(f"| {k} | {v} |")
        return out

    lines = [
        "# مصفوفة الذكاء السوقي (Market Intelligence Matrix)",
        "",
        WARNING,
        "",
        "صف واحد لكل شركة يدمج التصنيف مع طبقات: الفعاليات، عضوية المؤشرات، "
        "التعرّض الموسمي، وحداثة المصدر.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي الشركات | {total} |",
        f"| مخاطر تصنيف high/medium | {len(hm_risk)} |",
    ]
    lines += _dist("التوزيع حسب classification_risk", "classification_risk")
    lines += _dist("التوزيع حسب review_priority", "review_priority")
    lines += _dist("التوزيع حسب vision2030_theme", "vision2030_theme")
    lines += _dist("التوزيع حسب event_exposure_overall", "event_exposure_overall")
    lines += _dist("التوزيع حسب seasonal_hajj_exposure", "seasonal_hajj_exposure")
    lines += _dist("التوزيع حسب seasonal_ramadan_exposure", "seasonal_ramadan_exposure")
    lines += _dist("التوزيع حسب source_freshness_status", "source_freshness_status")

    lines += [
        "",
        "## جدول مخاطر التصنيف high/medium",
        "",
        "| symbol | name_ar | classification_risk | review_priority | "
        "event_exposure_overall | source_freshness_status |",
        "|---|---|---|---|---|---|",
    ]
    for _, r in hm_risk.iterrows():
        lines.append(
            f"| {r['symbol']} | {r['name_ar']} | {r['classification_risk']} | "
            f"{r['review_priority']} | {r['event_exposure_overall']} | "
            f"{r['source_freshness_status']} |"
        )

    lines += [
        "",
        "## ملاحظات منهجية",
        "",
        "- المصدر: `companies_classified` + طبقات الذكاء (left join، 259 صفًا محفوظة).",
        "- القيم المفقودة تصبح محايدة: `none` / `not_available` / `needs_verification`.",
        "- `source_freshness_status` يعتمد أحدث `last_reviewed` كمرساة (لا ساعة نظام).",
        "- `review_priority` و `classification_risk` محسوبان بتحفّظ من البيانات المرجعية.",
        "- طبقة جودة بيانات وذكاء سوق — ليست توصية استثمارية.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء مصفوفة الذكاء السوقي: {OUTPUT_CSV} + {REPORT_PATH}")


if __name__ == "__main__":
    main()
