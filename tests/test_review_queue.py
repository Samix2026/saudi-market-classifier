"""اختبارات طبقة قائمة المراجعة (Phase 3 — Review Queue)."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "reports" / "review_queue.md"
EXPOSURES = ROOT / "data" / "reference" / "mega_event_exposures.csv"

VALID_PRIORITIES = {"high", "medium", "low"}
ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _queue_rows():
    """صفوف جدول قائمة المراجعة الكاملة: قوائم خلايا."""
    rows = []
    for line in REPORT.read_text(encoding="utf-8").splitlines():
        if ROW_RE.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def test_report_generated():
    assert REPORT.exists(), "reports/review_queue.md غير موجود — شغّل run.py"


def test_fixed_investment_warning_present():
    text = REPORT.read_text(encoding="utf-8")
    assert "ليس توصية استثمارية" in text


def test_no_duplicate_symbol_reason_rows():
    rows = _queue_rows()
    keys = [(r[0], r[3]) for r in rows]  # (symbol, reason)
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    assert not dupes, f"صفوف مكررة (symbol, reason): {dupes}"


def test_every_item_has_priority():
    rows = _queue_rows()
    assert rows, "قائمة المراجعة فارغة — متوقع عناصر"
    for r in rows:
        priority = r[4]
        assert priority in VALID_PRIORITIES, \
            f"أولوية غير صحيحة '{priority}' للرمز {r[0]}"


def test_missing_rationale_cases_detected_if_present():
    """أي تعرّض high/medium بدون rationale يجب أن يظهر في القائمة بأولوية high."""
    import csv

    with open(EXPOSURES, newline="", encoding="utf-8") as f:
        exposures = list(csv.DictReader(f))

    expected = {
        r["symbol"]
        for r in exposures
        if (r["expo2030_exposure"] in ("high", "medium")
            or r["worldcup2034_exposure"] in ("high", "medium"))
        and not str(r["rationale"]).strip()
    }

    rows = _queue_rows()
    flagged = {r[0] for r in rows if r[3] == "missing_rationale"}
    assert expected == flagged, (
        f"عدم تطابق missing_rationale — متوقع {sorted(expected)} "
        f"موجود {sorted(flagged)}"
    )
    for r in rows:
        if r[3] == "missing_rationale":
            assert r[4] == "high"
