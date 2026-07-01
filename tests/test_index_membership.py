"""اختبارات طبقة عضوية المؤشرات (Phase 5 — Index Membership)."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMBERSHIPS = ROOT / "data" / "reference" / "index_memberships.csv"
PROCESSED = ROOT / "data" / "processed" / "companies_index_membership.csv"
REPORT = ROOT / "reports" / "index_membership_report.md"

ALLOWED_INDEX_CODES = {"TASI", "MT30", "TASI50", "LARGE_CAP", "MID_CAP", "SMALL_CAP"}
ALLOWED_STATUS = {"member", "not_member", "needs_verification"}
ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _report_symbols():
    return {line.strip().strip("|").split("|")[0].strip()
            for line in REPORT.read_text(encoding="utf-8").splitlines()
            if ROW_RE.match(line)}


def test_processed_generated():
    assert PROCESSED.exists(), "companies_index_membership.csv غير موجود — شغّل run.py"


def test_report_generated():
    assert REPORT.exists(), "index_membership_report.md غير موجود — شغّل run.py"


def test_required_columns_present():
    for r in _read(PROCESSED):
        assert r["symbol"].strip()
        assert r["index_code"].strip()
        assert r["membership_status"].strip()


def test_allowed_index_codes():
    for r in _read(MEMBERSHIPS):
        assert r["index_code"] in ALLOWED_INDEX_CODES, \
            f"index_code غير مسموح: {r['index_code']} للرمز {r['symbol']}"


def test_allowed_membership_status():
    for r in _read(MEMBERSHIPS):
        assert r["membership_status"] in ALLOWED_STATUS, \
            f"membership_status غير مسموح: {r['membership_status']} للرمز {r['symbol']}"


def test_no_duplicate_symbol_index_rows():
    rows = _read(MEMBERSHIPS)
    keys = [(r["symbol"], r["index_code"]) for r in rows]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    assert not dupes, f"صفوف مكررة (symbol, index_code): {dupes}"


def test_missing_source_url_surfaced():
    rows = _read(PROCESSED)
    missing = {r["symbol"] for r in rows if not r["source_url"].strip()}
    surfaced = _report_symbols()
    assert missing.issubset(surfaced) or not missing, \
        f"صفوف بدون source_url غير معروضة: {sorted(missing - surfaced)}"


def test_report_includes_disclaimer():
    assert "ليست توصية استثمارية" in REPORT.read_text(encoding="utf-8")
