"""اختبارات وثائق التسويق للمنتج (Phase 10 — Productization Docs). فحص نصي فقط."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
README = ROOT / "README.md"

REQUIRED_DOCS = [
    "PRODUCT_BRIEF.md",
    "METHODOLOGY.md",
    "DASHBOARD_GUIDE.md",
    "ROADMAP.md",
    "STAKEHOLDER_DEMO_SCRIPT.md",
]

FORBIDDEN = [
    "buy", "sell", "target price", "guaranteed return",
    "guaranteed benefit", "beneficiary", "winner",
]


def test_required_docs_exist():
    for name in REQUIRED_DOCS:
        assert (DOCS / name).exists(), f"مفقود: docs/{name}"


def test_docs_include_disclaimer():
    for name in REQUIRED_DOCS:
        text = (DOCS / name).read_text(encoding="utf-8").lower()
        assert "not investment advice" in text, f"لا تنبيه في docs/{name}"


def test_docs_have_no_forbidden_language():
    for name in REQUIRED_DOCS:
        text = (DOCS / name).read_text(encoding="utf-8").lower()
        hits = [w for w in FORBIDDEN if w in text]
        assert not hits, f"لغة ممنوعة في docs/{name}: {hits}"


def test_readme_links_docs():
    text = README.read_text(encoding="utf-8")
    for name in REQUIRED_DOCS:
        assert f"docs/{name}" in text, f"README لا يربط docs/{name}"
