"""اختبارات طبقة التعرّض الموسمي (Phase 6 — Seasonal Exposure)."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "data" / "reference" / "seasonal_exposures.csv"
PROCESSED = ROOT / "data" / "processed" / "companies_seasonal_exposure.csv"
REPORT = ROOT / "reports" / "seasonal_exposure_report.md"

REQUIRED_COLS = [
    "symbol", "season", "exposure_level", "primary_driver", "confidence",
    "rationale", "evidence_status", "source_url", "last_reviewed", "notes",
]
ALLOWED_SEASON = {"HAJJ", "RAMADAN"}
ALLOWED_LEVEL = {"high", "medium", "low", "none"}
ALLOWED_DRIVER = {
    "food_retail", "restaurants", "hospitality", "airlines", "ground_services",
    "transport", "telecom", "payments", "healthcare", "consumer_goods",
    "advertising_media", "facilities_management", "real_estate_makkah_madinah",
    "none",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_EVIDENCE = {
    "thematic_only", "official_announcement", "contract_disclosed",
    "financial_materiality_disclosed", "needs_verification",
}
ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _report_symbols():
    return {line.strip().strip("|").split("|")[0].strip()
            for line in REPORT.read_text(encoding="utf-8").splitlines()
            if ROW_RE.match(line)}


def test_reference_has_required_columns():
    with open(REFERENCE, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == REQUIRED_COLS


def test_processed_generated():
    assert PROCESSED.exists(), "companies_seasonal_exposure.csv غير موجود — شغّل run.py"


def test_report_generated():
    assert REPORT.exists(), "seasonal_exposure_report.md غير موجود — شغّل run.py"


def test_allowed_values():
    for r in _read(REFERENCE):
        assert r["season"] in ALLOWED_SEASON, r
        assert r["exposure_level"] in ALLOWED_LEVEL, r
        assert r["primary_driver"] in ALLOWED_DRIVER, r
        assert r["confidence"] in ALLOWED_CONFIDENCE, r
        assert r["evidence_status"] in ALLOWED_EVIDENCE, r


def test_no_duplicate_symbol_season():
    rows = _read(REFERENCE)
    keys = [(r["symbol"], r["season"]) for r in rows]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    assert not dupes, f"صفوف مكررة (symbol, season): {dupes}"


def test_high_medium_require_rationale():
    missing = [
        (r["symbol"], r["season"])
        for r in _read(REFERENCE)
        if r["exposure_level"] in ("high", "medium") and not r["rationale"].strip()
    ]
    assert not missing, f"high/medium بدون rationale: {missing}"


def test_report_includes_disclaimer():
    assert "ليس توصية استثمارية" in REPORT.read_text(encoding="utf-8")


def test_missing_rationale_high_medium_surfaced_if_present():
    missing = {
        r["symbol"] for r in _read(PROCESSED)
        if r["exposure_level"] in ("high", "medium") and not r["rationale"].strip()
    }
    surfaced = _report_symbols()
    assert missing.issubset(surfaced) or not missing, \
        f"صفوف high/medium بدون rationale غير معروضة: {sorted(missing - surfaced)}"


def test_needs_verification_surfaced_if_present():
    nv = {r["symbol"] for r in _read(PROCESSED)
          if r["evidence_status"] == "needs_verification"}
    surfaced = _report_symbols()
    assert nv.issubset(surfaced) or not nv, \
        f"صفوف needs_verification غير معروضة: {sorted(nv - surfaced)}"


def test_processed_deterministic():
    """المخرجات مرتبة (season, symbol) — تشغيلان متتاليان يعطيان نفس الملف."""
    rows = _read(PROCESSED)
    keys = [(r["season"], r["symbol"]) for r in rows]
    assert keys == sorted(keys), "ترتيب المخرجات غير حتمي (season, symbol)"
