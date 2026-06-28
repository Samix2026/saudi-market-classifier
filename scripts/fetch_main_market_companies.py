from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import requests


OUTPUT_PATH = Path("data/raw/main_market_companies.csv")

SAUDI_EXCHANGE_URLS = [
    "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=en",
    "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=ar",
]

EDAA_URLS = [
    "https://www.edaa.sa/wps/portal/edaa/participants/issuers/issuerdirectory?locale=en",
    "https://www.edaa.sa/wps/portal/edaa/participants/issuers/issuerdirectory?locale=ar",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
}


SECTOR_MAP_EN_TO_AR = {
    "Energy": "الطاقة",
    "Materials": "المواد الأساسية",
    "Capital Goods": "السلع الرأسمالية",
    "Commercial & Professional Svc": "الخدمات التجارية والمهنية",
    "Commercial & Professional Services": "الخدمات التجارية والمهنية",
    "Transportation": "النقل",
    "Consumer Durables & Apparel": "السلع طويلة الاجل والملابس",
    "Consumer Services": "الخدمات الاستهلاكية",
    "Media and Entertainment": "الإعلام والترفيه",
    "Consumer Discretionary Distribution & Retail": "تجزئة وتوزيع السلع الكمالية",
    "Consumer Staples Distribution & Retail": "تجزئة الأغذية",
    "Food & Beverages": "إنتاج الأغذية",
    "Household & Personal Products": "السلع الشخصية والمنزلية",
    "Health Care Equipment & Svc": "الرعاية الصحية",
    "Health Care Equipment & Services": "الرعاية الصحية",
    "Pharma, Biotech & Life Science": "الأدوية والتقنية الحيوية وعلوم الحياة",
    "Banks": "البنوك",
    "Financial Services": "الخدمات المالية",
    "Insurance": "التأمين",
    "Software & Services": "البرمجيات والخدمات",
    "Telecommunication Services": "الاتصالات",
    "Utilities": "المرافق العامة",
    "REITs": "الصناديق العقارية المتداولة",
    "Real Estate Mgmt & Dev't": "إدارة وتطوير العقارات",
    "Real Estate Management & Development": "إدارة وتطوير العقارات",
}


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def normalize_symbol(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    match = re.search(r"\b\d{4}\b", text)
    if not match:
        return None

    return match.group(0)


def normalize_sector(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).strip()
    return SECTOR_MAP_EN_TO_AR.get(text, text)


def clean_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def dataframe_from_html_tables(url: str) -> pd.DataFrame:
    html = fetch_html(url)

    try:
        tables = pd.read_html(html)
    except ValueError:
        return pd.DataFrame()

    candidates = []

    for table in tables:
        table.columns = [clean_text(col) for col in table.columns]
        columns_text = " ".join(table.columns).lower()

        if not any(keyword in columns_text for keyword in ["symbol", "company", "issuer", "sector", "market"]):
            continue

        candidates.append(table)

    if not candidates:
        return pd.DataFrame()

    return pd.concat(candidates, ignore_index=True)


def walk_json(obj: Any) -> list[dict[str, Any]]:
    rows = []

    if isinstance(obj, dict):
        if any(key.lower() in {"symbol", "companysymbol", "ticker"} for key in obj.keys()):
            rows.append(obj)

        for value in obj.values():
            rows.extend(walk_json(value))

    elif isinstance(obj, list):
        for item in obj:
            rows.extend(walk_json(item))

    return rows


def dataframes_from_json_in_html(url: str) -> pd.DataFrame:
    html = fetch_html(url)
    rows = []

    script_jsons = re.findall(
        r"<script[^>]*>(.*?)</script>",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )

    for script in script_jsons:
        script = script.strip()

        json_candidates = re.findall(r"(\{.*?\}|\[.*?\])", script, flags=re.DOTALL)

        for candidate in json_candidates:
            if "symbol" not in candidate.lower() and "company" not in candidate.lower():
                continue

            try:
                parsed = json.loads(candidate)
            except Exception:
                continue

            rows.extend(walk_json(parsed))

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def pick_column(columns: list[str], keywords: list[str]) -> str | None:
    lowered = {col: col.lower() for col in columns}

    for col, lower in lowered.items():
        if any(keyword in lower for keyword in keywords):
            return col

    return None


def normalize_companies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["symbol", "name_ar", "name_en", "market", "sector"])

    df = df.copy()
    df.columns = [clean_text(col) for col in df.columns]

    symbol_col = pick_column(
        list(df.columns),
        ["symbol", "companysymbol", "ticker", "code", "رمز"],
    )
    name_col = pick_column(
        list(df.columns),
        ["company", "issuer", "name", "الشركة", "المصدر", "الاسم"],
    )
    sector_col = pick_column(
        list(df.columns),
        ["sector", "industry", "قطاع"],
    )
    market_col = pick_column(
        list(df.columns),
        ["market", "السوق"],
    )

    if symbol_col is None:
        # Try every cell and keep rows with a 4-digit symbol.
        symbols = []
        for _, row in df.iterrows():
            symbol = None
            for value in row.values:
                symbol = normalize_symbol(value)
                if symbol:
                    break
            symbols.append(symbol)
        df["_symbol"] = symbols
        symbol_col = "_symbol"

    rows = []

    for _, row in df.iterrows():
        symbol = normalize_symbol(row.get(symbol_col))

        if not symbol:
            continue

        name = clean_text(row.get(name_col)) if name_col else ""
        sector = normalize_sector(row.get(sector_col)) if sector_col else ""
        market = clean_text(row.get(market_col)) if market_col else "Main Market"

        # Keep only regular Saudi 4-digit symbols; exclude obvious non-equity rows later by market/sector if possible.
        if not re.fullmatch(r"\d{4}", symbol):
            continue

        rows.append(
            {
                "symbol": int(symbol),
                "name_ar": name,
                "name_en": name,
                "market": market or "Main Market",
                "sector": sector,
            }
        )

    out = pd.DataFrame(rows)

    if out.empty:
        return pd.DataFrame(columns=["symbol", "name_ar", "name_en", "market", "sector"])

    out = out.drop_duplicates(subset=["symbol"]).sort_values("symbol")
    return out[["symbol", "name_ar", "name_en", "market", "sector"]]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    frames = []

    for url in SAUDI_EXCHANGE_URLS + EDAA_URLS:
        print(f"Trying HTML tables: {url}")
        html_df = dataframe_from_html_tables(url)
        normalized = normalize_companies(html_df)

        if not normalized.empty:
            print(f"  Found {len(normalized)} rows from HTML tables.")
            frames.append(normalized)

        print(f"Trying JSON extraction: {url}")
        json_df = dataframes_from_json_in_html(url)
        normalized = normalize_companies(json_df)

        if not normalized.empty:
            print(f"  Found {len(normalized)} rows from JSON.")
            frames.append(normalized)

    if not frames:
        print()
        print("No company rows could be extracted automatically.")
        print("The official pages may be rendered dynamically or protected from direct scraping.")
        print("Use a browser export/copy, then save it as data/raw/main_market_companies.csv")
        raise SystemExit(1)

    companies = pd.concat(frames, ignore_index=True)
    companies = companies.drop_duplicates(subset=["symbol"]).sort_values("symbol")

    companies.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print()
    print(f"Wrote {len(companies)} rows to {OUTPUT_PATH}")
    print()
    print(companies.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
