"""اختبارات طبقة حداثة المصادر (Phase 4 — Source Freshness)."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "reports" / "source_freshness_report.md"
COMPANIES = ROOT / "data" / "reference" / "companies.csv"
OFFICIAL = ROOT / "data" / "reference" / "official_sources.csv"
QUALITY = ROOT / "data" / "reference" / "source_quality.csv"

STALE_DAYS = 90
ROW_RE = re.compile(r"^\|\s*\d{4}\b")


def _text():
    return REPORT.read_text(encoding="utf-8")


def _row_symbols():
    return {line.strip().strip("|").split("|")[0].strip()
            for line in _text().splitlines() if ROW_RE.match(line)}


def _joined():
    companies = pd.read_csv(COMPANIES, dtype={"symbol": str})
    official = pd.read_csv(OFFICIAL, dtype={"symbol": str})
    quality = pd.read_csv(QUALITY, dtype={"symbol": str})
    return companies.merge(
        official[["symbol", "official_profile_url", "source_type"]],
        on="symbol", how="left",
    ).merge(quality[["symbol", "last_reviewed"]], on="symbol", how="left")


def test_report_generated():
    assert REPORT.exists(), "reports/source_freshness_report.md غير موجود — شغّل run.py"


def test_disclaimer_present():
    assert "ليس توصية استثمارية" in _text()


def test_source_type_distribution_present():
    text = _text()
    assert "التوزيع حسب source_type" in text
    df = _joined()
    df["source_type"] = df["source_type"].fillna("pending")
    # كل قيمة source_type موجودة يجب أن تظهر في التقرير.
    for value in df["source_type"].unique():
        assert f"| {value} |" in text, f"source_type '{value}' غير مذكور"


def test_missing_official_urls_surfaced_if_present():
    df = _joined()
    missing = {
        r["symbol"] for _, r in df.iterrows()
        if pd.isna(r["official_profile_url"])
        or str(r["official_profile_url"]).strip() == ""
    }
    surfaced = _row_symbols()
    assert missing.issubset(surfaced) or not missing, \
        f"روابط رسمية مفقودة غير معروضة: {sorted(missing - surfaced)}"


def test_stale_records_surfaced_if_present():
    df = _joined()
    parsed = pd.to_datetime(df["last_reviewed"], format="%Y-%m-%d", errors="coerce")
    ref = parsed.max()
    if pd.isna(ref):
        return
    cutoff = ref - pd.Timedelta(days=STALE_DAYS)
    stale = {df.iloc[i]["symbol"] for i in range(len(df))
             if pd.notna(parsed.iloc[i]) and parsed.iloc[i] < cutoff}
    surfaced = _row_symbols()
    assert stale.issubset(surfaced) or not stale, \
        f"سجلات قديمة غير معروضة: {sorted(stale - surfaced)}"
