"""اختبارات خفيفة للوحة (Phase 9 — Dashboard). فحص نصي فقط، لا يستورد streamlit."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "dashboard" / "app.py"
DASH_README = ROOT / "dashboard" / "README.md"

FORBIDDEN = ["buy", "sell", "target price", "guaranteed", "winner", "beneficiary"]


def test_app_exists():
    assert APP.exists(), "dashboard/app.py غير موجود"


def test_readme_exists():
    assert DASH_README.exists(), "dashboard/README.md غير موجود"


def test_app_references_matrix_dataset():
    assert "public/datasets/market_intelligence_matrix.csv" in APP.read_text(
        encoding="utf-8"
    )


def test_app_includes_disclaimer():
    assert "not investment advice" in APP.read_text(encoding="utf-8")


def test_app_has_no_forbidden_language():
    text = APP.read_text(encoding="utf-8").lower()
    hits = [w for w in FORBIDDEN if w in text]
    assert not hits, f"لغة استثمارية ممنوعة في app.py: {hits}"


def test_app_has_separate_index_pending_kpi():
    text = APP.read_text(encoding="utf-8")
    assert "Index verification pending" in text
    # Needing review KPI must be driven by review_priority, not the index column.
    assert 'filtered["review_priority"] != "none"' in text
