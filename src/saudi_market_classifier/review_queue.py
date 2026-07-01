"""طبقة قائمة المراجعة (Phase 3 — Review Queue Layer).

تجمع في تقرير واحد كل الشركات التي تحتاج مراجعة بشرية أو تحققًا رسميًا،
اعتمادًا على المصادر والتقارير الموجودة فقط. طبقة جودة/إبلاغ — لا تغيّر التصنيف.

تنبيه ثابت: التقرير ليس توصية استثمارية.
"""

import csv
import re
from pathlib import Path

import pandas as pd


COMPANIES_CSV = "data/reference/companies.csv"
CLASSIFIED_CSV = "data/processed/companies_classified.csv"
EXPOSURES_CSV = "data/reference/mega_event_exposures.csv"
DEFERRED_REPORT = Path("reports/excluded_or_deferred_companies.md")
HOLDING_REPORT = Path("reports/holding_companies_review.md")
REPORT_PATH = Path("reports/review_queue.md")

WARNING = (
    "> **تنبيه:** هذا التقرير لأغراض جودة البيانات والمراجعة فقط، "
    "وليس توصية استثمارية ولا نصيحة مالية."
)

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _parse_table_rows(path):
    """صفوف جدول Markdown تبدأ برمز من 4 أرقام؛ ترجع قوائم خلايا نصية."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if ROW_RE.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def _collect_items():
    """يبني قائمة عناصر المراجعة من المصادر. كل عنصر dict موحّد الأعمدة."""
    items = []

    # 1) الشركات المؤجلة (كلها من مراجعة السوق الرئيسية) → أولوية عالية.
    for cells in _parse_table_rows(DEFERRED_REPORT):
        symbol, name_ar = cells[0], cells[1]
        items.append({
            "symbol": symbol,
            "name_ar": name_ar,
            "source": "deferred",
            "reason": "deferred_main_market",
            "priority": "high",
            "note": "شركة مؤجلة من السوق الرئيسية تحتاج تحقق حالة الإدراج.",
        })

    # 2) الشركات القابضة بحالة needs_review → أولوية متوسطة.
    for cells in _parse_table_rows(HOLDING_REPORT):
        # الأعمدة: symbol name_ar name_en sector bclass theme status note
        if len(cells) >= 7 and cells[6] == "needs_review":
            items.append({
                "symbol": cells[0],
                "name_ar": cells[1],
                "source": "holding_review",
                "reason": "holding_needs_review",
                "priority": "medium",
                "note": cells[7] if len(cells) >= 8 else "",
            })

    # 3) طبقة التعرّض للفعاليات.
    exposures = pd.read_csv(EXPOSURES_CSV, dtype={"symbol": str})
    for _, r in exposures.iterrows():
        is_hm = r["expo2030_exposure"] in ("high", "medium") or \
            r["worldcup2034_exposure"] in ("high", "medium")
        rationale = str(r["rationale"]).strip()
        # 3a) تعرّض high/medium بدون rationale → أولوية عالية.
        if is_hm and not rationale:
            items.append({
                "symbol": r["symbol"],
                "name_ar": r["name_ar"],
                "source": "mega_event",
                "reason": "missing_rationale",
                "priority": "high",
                "note": "تعرّض high/medium بدون rationale — يلزم توثيق السبب.",
            })
        # 3b) تعرّض high/medium بثقة منخفضة → أولوية متوسطة.
        elif is_hm and r["confidence"] == "low":
            items.append({
                "symbol": r["symbol"],
                "name_ar": r["name_ar"],
                "source": "mega_event",
                "reason": "low_confidence_exposure",
                "priority": "medium",
                "note": "تعرّض high/medium بثقة منخفضة — يحتاج مراجعة دورية.",
            })

    # 4) عناصر معلوماتية: شركات مصنّفة تنتظر تحققًا رسميًا → أولوية منخفضة.
    with open(CLASSIFIED_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("source_quality", "official") != "official" or \
                    r.get("source_type", "official") != "official":
                items.append({
                    "symbol": r["symbol"],
                    "name_ar": r["name_ar"],
                    "source": "classified",
                    "reason": "needs_official_verification",
                    "priority": "low",
                    "note": "مصدر غير رسمي — يحتاج تحققًا لاحقًا.",
                })

    # إزالة تكرار (symbol, reason) مع الحفاظ على أول ظهور.
    seen = set()
    unique = []
    for it in items:
        key = (it["symbol"], it["reason"])
        if key not in seen:
            seen.add(key)
            unique.append(it)

    # ترتيب ثابت: الأولوية ثم الرمز ثم السبب.
    unique.sort(key=lambda it: (PRIORITY_RANK[it["priority"]], it["symbol"], it["reason"]))
    return unique


def main():
    items = _collect_items()

    by_priority = {p: [it for it in items if it["priority"] == p]
                   for p in ("high", "medium", "low")}
    deferred = [it for it in items if it["source"] == "deferred"]
    holding = [it for it in items if it["source"] == "holding_review"]
    low_conf = [it for it in items if it["reason"] == "low_confidence_exposure"]
    missing_rat = [it for it in items if it["reason"] == "missing_rationale"]

    lines = [
        "# قائمة المراجعة (Review Queue)",
        "",
        WARNING,
        "",
        "تقرير مولّد يجمع كل الشركات التي تحتاج مراجعة بشرية أو تحققًا رسميًا "
        "من المصادر والتقارير الموجودة.",
        "",
        "## الملخص التنفيذي",
        "",
        "| المؤشر | العدد |",
        "|---|---:|",
        f"| إجمالي عناصر المراجعة | {len(items)} |",
        f"| أولوية high | {len(by_priority['high'])} |",
        f"| أولوية medium | {len(by_priority['medium'])} |",
        f"| أولوية low | {len(by_priority['low'])} |",
        f"| شركات مؤجلة | {len(deferred)} |",
        f"| شركات قابضة needs_review | {len(holding)} |",
        f"| تعرّض بثقة منخفضة | {len(low_conf)} |",
        f"| تعرّض high/medium بدون rationale | {len(missing_rat)} |",
        "",
        "## قائمة المراجعة الكاملة",
        "",
        "| symbol | name_ar | source | reason | priority | note |",
        "|---|---|---|---|---|---|",
    ]
    for it in items:
        lines.append(
            f"| {it['symbol']} | {it['name_ar']} | {it['source']} | "
            f"{it['reason']} | {it['priority']} | {it['note']} |"
        )

    lines.extend(["", "## الشركات المؤجلة", ""])
    if deferred:
        for it in deferred:
            lines.append(f"- {it['symbol']} — {it['name_ar']}")
    else:
        lines.append("- لا يوجد.")

    lines.extend(["", "## الشركات القابضة (needs_review)", ""])
    if holding:
        for it in holding:
            lines.append(f"- {it['symbol']} — {it['name_ar']}: {it['note']}")
    else:
        lines.append("- لا يوجد.")

    lines.extend(["", "## تعرّض للفعاليات بثقة منخفضة", ""])
    if low_conf:
        for it in low_conf:
            lines.append(f"- {it['symbol']} — {it['name_ar']}")
    else:
        lines.append("- لا يوجد.")

    lines.extend(["", "## تعرّض high/medium بدون rationale", ""])
    if missing_rat:
        for it in missing_rat:
            lines.append(f"- {it['symbol']} — {it['name_ar']}")
    else:
        lines.append("- لا يوجد.")

    lines.append("")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"تم إنشاء قائمة المراجعة: {REPORT_PATH} ({len(items)} عنصر)")


if __name__ == "__main__":
    main()
