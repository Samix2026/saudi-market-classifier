from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
from playwright.sync_api import sync_playwright


OUTPUT_PATH = Path("data/raw/main_market_companies.csv")
DEBUG_DIR = Path("data/raw/debug")

URLS = [
    "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=en",
    "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=ar",
    "https://www.edaa.sa/wps/portal/edaa/participants/issuers/issuerdirectory?locale=en",
    "https://www.edaa.sa/wps/portal/edaa/participants/issuers/issuerdirectory?locale=ar",
]

SECTOR_MAP_EN_TO_AR = {
    "Energy": "الطاقة",
    "Materials": "المواد الأساسية",
    "Capital Goods": "السلع الرأسمالية",
    "Commercial & Professional Services": "الخدمات التجارية والمهنية",
    "Commercial & Professional Svc": "الخدمات التجارية والمهنية",
    "Transportation": "النقل",
    "Consumer Services": "الخدمات الاستهلاكية",
    "Consumer Discretionary Distribution & Retail": "تجزئة وتوزيع السلع الكمالية",
    "Consumer Staples Distribution & Retail": "تجزئة الأغذية",
    "Food & Beverages": "إنتاج الأغذية",
    "Health Care Equipment & Services": "الرعاية الصحية",
    "Health Care Equipment & Svc": "الرعاية الصحية",
    "Banks": "البنوك",
    "Insurance": "التأمين",
    "Telecommunication Services": "الاتصالات",
    "Utilities": "المرافق العامة",
    "Real Estate Management & Development": "إدارة وتطوير العقارات",
    "Real Estate Mgmt & Dev't": "إدارة وتطوير العقارات",
    "Financial Services": "الخدمات المالية",
    "Software & Services": "البرمجيات والخدمات",
    "REITs": "الصناديق العقارية المتداولة",
}


def clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()


def has_arabic(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", text or ""))


def normalize_symbol(value: Any) -> str | None:
    text = clean(value)
    match = re.search(r"\b\d{4}\b", text)
    return match.group(0) if match else None


def normalize_sector(value: Any) -> str:
    text = clean(value)
    return SECTOR_MAP_EN_TO_AR.get(text, text)


def walk_json(obj: Any) -> list[dict[str, Any]]:
    rows = []

    if isinstance(obj, dict):
        values_text = " ".join(clean(v) for v in obj.values() if isinstance(v, (str, int, float)))

        if re.search(r"\b\d{4}\b", values_text):
            rows.append(obj)

        for value in obj.values():
            rows.extend(walk_json(value))

    elif isinstance(obj, list):
        for item in obj:
            rows.extend(walk_json(item))

    return rows


def pick_by_keywords(row: dict[str, Any], keywords: list[str]) -> str:
    for key, value in row.items():
        key_l = clean(key).lower()
        if any(keyword in key_l for keyword in keywords):
            val = clean(value)
            if val:
                return val
    return ""


def row_to_company(row: dict[str, Any]) -> dict[str, Any] | None:
    symbol = ""

    for key, value in row.items():
        key_l = clean(key).lower()
        if any(k in key_l for k in ["symbol", "ticker", "code", "companysymbol", "securitycode"]):
            symbol = normalize_symbol(value) or ""
            if symbol:
                break

    if not symbol:
        for value in row.values():
            symbol = normalize_symbol(value) or ""
            if symbol:
                break

    if not symbol:
        return None

    name_ar = (
        pick_by_keywords(row, ["namear", "arabic", "arabicname", "companynamear", "issuernamear"])
        or pick_by_keywords(row, ["shortnamear", "securitynamear"])
    )

    name_en = (
        pick_by_keywords(row, ["nameen", "english", "englishname", "companynameen", "issuernameen"])
        or pick_by_keywords(row, ["shortnameen", "securitynameen"])
    )

    generic_name = pick_by_keywords(row, ["company", "issuer", "securityname", "name"])

    if not name_ar and has_arabic(generic_name):
        name_ar = generic_name

    if not name_en and generic_name and not has_arabic(generic_name):
        name_en = generic_name

    sector = (
        pick_by_keywords(row, ["sectornamear", "sectorar"])
        or pick_by_keywords(row, ["sectorname", "sector", "industry"])
    )

    market = pick_by_keywords(row, ["marketname", "market"])

    return {
        "symbol": int(symbol),
        "name_ar": clean(name_ar),
        "name_en": clean(name_en),
        "market": clean(market) or "Main Market",
        "sector": normalize_sector(sector),
    }


def extract_from_text_blocks(page) -> list[dict[str, Any]]:
    rows = []

    texts = page.locator("body").inner_text(timeout=10_000)
    lines = [clean(line) for line in texts.splitlines() if clean(line)]

    for i, line in enumerate(lines):
        symbol = normalize_symbol(line)
        if not symbol:
            continue

        nearby = lines[max(0, i - 3): i + 8]
        joined = " | ".join(nearby)

        rows.append({
            "symbol": int(symbol),
            "name_ar": next((x for x in nearby if has_arabic(x) and not normalize_symbol(x)), ""),
            "name_en": next((x for x in nearby if not has_arabic(x) and not normalize_symbol(x)), ""),
            "market": "Main Market" if "Main" in joined or "السوق الرئيسية" in joined else "",
            "sector": "",
        })

    return rows


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    collected_rows: list[dict[str, Any]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1440, "height": 1100},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        def handle_response(response):
            try:
                content_type = response.headers.get("content-type", "")
                url = response.url.lower()

                if "json" not in content_type and not any(k in url for k in ["market", "issuer", "security", "stock", "company"]):
                    return

                text = response.text()

                if not re.search(r"\b\d{4}\b", text):
                    return

                try:
                    data = json.loads(text)
                except Exception:
                    return

                for item in walk_json(data):
                    company = row_to_company(item)
                    if company:
                        collected_rows.append(company)

            except Exception:
                return

        page.on("response", handle_response)

        for idx, url in enumerate(URLS, start=1):
            print(f"Opening: {url}")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                page.wait_for_timeout(12_000)

                page.screenshot(path=str(DEBUG_DIR / f"page_{idx}.png"), full_page=True)

                html = page.content()
                (DEBUG_DIR / f"page_{idx}.html").write_text(html, encoding="utf-8")

                collected_rows.extend(extract_from_text_blocks(page))

            except Exception as exc:
                print(f"Failed: {url}")
                print(exc)

        browser.close()

    if not collected_rows:
        print()
        print("No companies extracted.")
        print(f"Debug files saved in: {DEBUG_DIR}")
        raise SystemExit(1)

    df = pd.DataFrame(collected_rows)
    df = df.dropna(subset=["symbol"])
    df = df.drop_duplicates(subset=["symbol"]).sort_values("symbol")

    df = df[["symbol", "name_ar", "name_en", "market", "sector"]]
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print()
    print(f"Wrote {len(df)} rows to {OUTPUT_PATH}")
    print()
    print(df.head(30).to_string(index=False))


if __name__ == "__main__":
    main()
