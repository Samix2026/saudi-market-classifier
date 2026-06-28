"""اختبارات جودة البيانات — تمنع تراجع التغطية أو فساد المفاتيح.

تقرأ الملفات الأساسية الثلاثة وتتحقق من:
- عدد الشركات لا ينخفض عن 259.
- تطابق عدد الشركات بين companies.csv و companies_classified.csv.
- عدم تكرار symbol في أي ملف.
- عدم وجود symbol فارغ.
- عدم وجود unclassified في vision2030_theme بعد تحسين التغطية.
"""

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
COMPANIES = ROOT / "data" / "reference" / "companies.csv"
THEMES = ROOT / "data" / "reference" / "vision2030_themes.csv"
CLASSIFIED = ROOT / "data" / "processed" / "companies_classified.csv"

EXPECTED_COUNT = 259


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def companies():
    return _read(COMPANIES)


@pytest.fixture(scope="module")
def themes():
    return _read(THEMES)


@pytest.fixture(scope="module")
def classified():
    return _read(CLASSIFIED)


# 1. عدد الشركات لا ينخفض عن 259 (ويساوي 259 حاليًا).

def test_companies_count(companies):
    assert len(companies) >= EXPECTED_COUNT
    assert len(companies) == EXPECTED_COUNT


def test_classified_count(classified):
    assert len(classified) == EXPECTED_COUNT


def test_themes_count(themes):
    assert len(themes) == EXPECTED_COUNT


# 2. لا تكرار symbol في أي من الملفات الثلاثة.

@pytest.mark.parametrize("name", ["companies", "themes", "classified"])
def test_no_duplicate_symbols(name, request):
    rows = request.getfixturevalue(name)
    symbols = [r["symbol"] for r in rows]
    dupes = sorted({s for s in symbols if symbols.count(s) > 1})
    assert not dupes, f"رموز مكررة في {name}: {dupes}"


# 3. لا قيم فارغة في symbol.

@pytest.mark.parametrize("name", ["companies", "themes", "classified"])
def test_no_empty_symbols(name, request):
    rows = request.getfixturevalue(name)
    empties = [i for i, r in enumerate(rows) if not r["symbol"].strip()]
    assert not empties, f"رموز فارغة في {name} عند الصفوف: {empties}"


# 4. تطابق مجموعة الرموز بين companies.csv و companies_classified.csv.

def test_symbol_sets_match(companies, classified):
    comp = {r["symbol"] for r in companies}
    clas = {r["symbol"] for r in classified}
    assert comp == clas, (
        f"اختلاف الرموز — فقط في companies: {sorted(comp - clas)} | "
        f"فقط في classified: {sorted(clas - comp)}"
    )


# 5. لا وجود unclassified في vision2030_theme بعد تحسين التغطية.

def test_no_unclassified_theme(classified):
    bad = [r["symbol"] for r in classified if r["vision2030_theme"].strip() == "unclassified"]
    assert not bad, f"رموز ما زالت unclassified: {bad}"


def test_themes_file_no_unclassified(themes):
    bad = [r["symbol"] for r in themes if r["vision2030_theme"].strip() == "unclassified"]
    assert not bad, f"رموز ما زالت unclassified في ملف الثيمات: {bad}"
