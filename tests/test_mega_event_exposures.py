"""اختبارات جودة طبقة الذكاء السوقي (Phase 2 — Mega Event Exposure)."""

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
COMPANIES = ROOT / "data" / "reference" / "companies.csv"
EXPOSURES = ROOT / "data" / "reference" / "mega_event_exposures.csv"
INTELLIGENCE = ROOT / "data" / "processed" / "companies_intelligence.csv"
CLASSIFIED = ROOT / "data" / "processed" / "companies_classified.csv"

EXPECTED_COUNT = 259

ALLOWED_EXPOSURE = {"high", "medium", "low", "none"}
ALLOWED_DRIVER = {
    "venue_construction", "urban_infrastructure", "transport_mobility",
    "hospitality_tourism", "food_catering", "digital_connectivity",
    "event_services", "media_advertising", "facilities_management",
    "security_operations", "none",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
BANNED_WORDS = ["beneficiary", "winner", "guaranteed"]


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def companies():
    return _read(COMPANIES)


@pytest.fixture(scope="module")
def exposures():
    return _read(EXPOSURES)


@pytest.fixture(scope="module")
def intelligence():
    return _read(INTELLIGENCE)


@pytest.fixture(scope="module")
def classified():
    return _read(CLASSIFIED)


# 1. كل رمز في ملف التعرّض موجود في companies.csv.

def test_exposure_symbols_exist(exposures, companies):
    company_symbols = {r["symbol"] for r in companies}
    missing = sorted({r["symbol"] for r in exposures} - company_symbols)
    assert not missing, f"رموز تعرّض غير موجودة في companies.csv: {missing}"


# 2. لا تكرار للرموز في ملف التعرّض.

def test_no_duplicate_exposure_symbols(exposures):
    symbols = [r["symbol"] for r in exposures]
    dupes = sorted({s for s in symbols if symbols.count(s) > 1})
    assert not dupes, f"رموز مكررة في ملف التعرّض: {dupes}"


# 3. كل القيم ضمن المجموعات المسموحة.

def test_allowed_values(exposures):
    for r in exposures:
        for col in ("expo2030_exposure", "worldcup2034_exposure", "exposure_strength"):
            assert r[col] in ALLOWED_EXPOSURE, f"{col}={r[col]} للرمز {r['symbol']}"
        for col in ("primary_event_driver", "secondary_event_driver"):
            assert r[col] in ALLOWED_DRIVER, f"{col}={r[col]} للرمز {r['symbol']}"
        assert r["confidence"] in ALLOWED_CONFIDENCE, \
            f"confidence={r['confidence']} للرمز {r['symbol']}"


# 4. لا rationale فارغ للشركات ذات تعرّض high/medium.

def test_rationale_present_for_high_medium(exposures):
    missing = []
    for r in exposures:
        exposed = {r["expo2030_exposure"], r["worldcup2034_exposure"]}
        if exposed & {"high", "medium"} and not r["rationale"].strip():
            missing.append(r["symbol"])
    assert not missing, f"rationale فارغ لرموز high/medium: {missing}"


# 5. companies_intelligence.csv يحافظ على 259 صفًا.

def test_intelligence_row_count(intelligence):
    assert len(intelligence) == EXPECTED_COUNT


# 6. تطابق مجموعة الرموز مع التصنيف الأساسي، وغياب الكلمات الممنوعة.

def test_intelligence_symbol_set_matches_classified(intelligence, classified):
    assert {r["symbol"] for r in intelligence} == {r["symbol"] for r in classified}


def test_no_banned_words_in_rationale(exposures, intelligence):
    for rows, label in ((exposures, "exposures"), (intelligence, "intelligence")):
        for r in rows:
            text = r.get("rationale", "").lower()
            hit = [w for w in BANNED_WORDS if w in text]
            assert not hit, f"كلمة ممنوعة {hit} في {label} للرمز {r['symbol']}"
