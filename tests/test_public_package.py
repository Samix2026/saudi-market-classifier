"""اختبارات حزمة البيانات العامة (Phase 8 — Public Data Package)."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
MANIFEST = PUBLIC / "manifest.json"
DATASETS = PUBLIC / "datasets"
REPORT = ROOT / "reports" / "public_data_package_report.md"
CLASSIFIED = ROOT / "data" / "processed" / "companies_classified.csv"

EXPECTED_FILES = [
    "companies_classified.csv", "companies_intelligence.csv",
    "companies_index_membership.csv", "companies_seasonal_exposure.csv",
    "market_intelligence_matrix.csv",
]


def _manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_package_files_generated():
    assert MANIFEST.exists()
    assert (PUBLIC / "README.md").exists()
    assert (PUBLIC / "DATA_DICTIONARY.md").exists()
    assert REPORT.exists()
    for name in EXPECTED_FILES:
        assert (DATASETS / name).exists(), f"مفقود: {name}"


def test_manifest_lists_all_datasets():
    files = {Path(d["file"]).name for d in _manifest()["datasets"]}
    assert files == set(EXPECTED_FILES)


def test_manifest_row_counts_match_sources():
    for d in _manifest()["datasets"]:
        name = Path(d["file"]).name
        src = ROOT / "data" / "processed" / name
        with open(src, encoding="utf-8") as f:
            actual = sum(1 for _ in f) - 1
        assert d["rows"] == actual, f"عدد صفوف غير مطابق لـ {name}"


def test_bundled_copies_match_sources():
    for name in EXPECTED_FILES:
        src = (ROOT / "data" / "processed" / name).read_bytes()
        pkg = (DATASETS / name).read_bytes()
        assert src == pkg, f"نسخة الحزمة لا تطابق المصدر: {name}"


def test_uses_source_anchor_date_not_wall_clock():
    m = _manifest()
    assert "source_anchor_date" in m
    assert "generated_at" not in m
    classified = pd.read_csv(CLASSIFIED, dtype={"symbol": str})
    anchor = pd.to_datetime(
        classified["last_reviewed"], format="%Y-%m-%d", errors="coerce"
    ).max().date().isoformat()
    assert m["source_anchor_date"] == anchor


def test_disclaimer_present():
    assert "not investment advice" in MANIFEST.read_text(encoding="utf-8").lower()
    assert "ليست توصية استثمارية" in REPORT.read_text(encoding="utf-8")
    assert "ليست توصية استثمارية" in (PUBLIC / "README.md").read_text(encoding="utf-8")


def test_flagship_row_count():
    assert _manifest()["row_count_flagship"] == 259


def test_deterministic_manifest():
    """البيان مُنتَج بترتيب مفاتيح ثابت (sort_keys) — حتمي."""
    text = MANIFEST.read_text(encoding="utf-8")
    reparsed = json.dumps(json.loads(text), ensure_ascii=False, indent=2,
                          sort_keys=True) + "\n"
    assert text == reparsed
