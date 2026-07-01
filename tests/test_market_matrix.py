"""اختبارات مصفوفة الذكاء السوقي (Phase 7 — Market Intelligence Matrix)."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "data" / "processed" / "market_intelligence_matrix.csv"
REPORT = ROOT / "reports" / "market_intelligence_matrix.md"
SEASONAL = ROOT / "data" / "processed" / "companies_seasonal_exposure.csv"

EXPECTED_COUNT = 259
REQUIRED_COLS = [
    "symbol", "name_ar", "name_en", "sector", "business_class", "vision2030_theme",
    "event_exposure_overall", "primary_event_driver", "event_confidence",
    "seasonal_hajj_exposure", "seasonal_ramadan_exposure", "seasonal_primary_drivers",
    "index_membership_summary", "source_type", "source_freshness_status",
    "review_priority", "classification_risk",
]
ALLOWED_RISK = {"high", "medium", "low"}
ALLOWED_PRIORITY = {"high", "medium", "low", "none"}
ALLOWED_FRESHNESS = {"current", "stale", "missing"}


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_matrix_generated():
    assert MATRIX.exists(), "market_intelligence_matrix.csv غير موجود — شغّل run.py"


def test_report_generated():
    assert REPORT.exists(), "market_intelligence_matrix.md غير موجود — شغّل run.py"


def test_matrix_row_count():
    assert len(_read(MATRIX)) == EXPECTED_COUNT


def test_one_row_per_symbol():
    symbols = [r["symbol"] for r in _read(MATRIX)]
    assert len(symbols) == len(set(symbols)), "رموز مكررة في المصفوفة"


def test_required_columns():
    with open(MATRIX, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == REQUIRED_COLS


def test_allowed_classification_risk():
    for r in _read(MATRIX):
        assert r["classification_risk"] in ALLOWED_RISK, r["symbol"]


def test_allowed_review_priority():
    for r in _read(MATRIX):
        assert r["review_priority"] in ALLOWED_PRIORITY, r["symbol"]


def test_allowed_source_freshness_status():
    for r in _read(MATRIX):
        assert r["source_freshness_status"] in ALLOWED_FRESHNESS, r["symbol"]


def test_seasonal_defaults_to_none_when_missing():
    seasonal_symbols = {r["symbol"] for r in _read(SEASONAL)}
    for r in _read(MATRIX):
        if r["symbol"] not in seasonal_symbols:
            assert r["seasonal_hajj_exposure"] == "none"
            assert r["seasonal_ramadan_exposure"] == "none"
            assert r["seasonal_primary_drivers"] == "none"


def test_index_summary_defaults_when_missing():
    for r in _read(MATRIX):
        summary = r["index_membership_summary"]
        assert summary == "not_available" or "needs_verification" in summary \
            or ":" in summary, f"index summary غير واضح للرمز {r['symbol']}"


def test_report_includes_disclaimer():
    assert "ليست توصية استثمارية" in REPORT.read_text(encoding="utf-8")


def test_deterministic_output():
    """المصفوفة مرتّبة بالرمز — دليل حتمية الترتيب."""
    symbols = [r["symbol"] for r in _read(MATRIX)]
    assert symbols == sorted(symbols), "ترتيب المصفوفة غير حتمي"
