from pathlib import Path
import pandas as pd


TODAY = "2026-06-28"

current_path = Path("data/reference/companies.csv")
incoming_path = Path("data/raw/main_market_companies.csv")
themes_path = Path("data/reference/vision2030_themes.csv")
quality_path = Path("data/reference/source_quality.csv")
sources_path = Path("data/reference/official_sources.csv")

base_url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/hidden/company-profile-main/%21ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8ziTR3NDIw8LAz83d2MXA0C3SydAl1c3Q0NvE30I4EKzBEKDMKcTQzMDPxN3H19LAzdTU31w8syU8v1wwkpK8hOMgUA-oskdg%21%21/?companySymbol={symbol}"

if not incoming_path.exists():
    print(f"Missing file: {incoming_path}")
    raise SystemExit(1)

companies = pd.read_csv(current_path)
incoming = pd.read_csv(incoming_path)
themes = pd.read_csv(themes_path)
quality = pd.read_csv(quality_path)
sources = pd.read_csv(sources_path)

required = {"symbol", "name_ar", "name_en", "market", "sector"}
missing_columns = required - set(incoming.columns)

if missing_columns:
    print("Missing columns in incoming file:")
    for column in sorted(missing_columns):
        print(f"- {column}")
    raise SystemExit(1)

missing = incoming[~incoming["symbol"].isin(companies["symbol"])].copy()
missing = missing.sort_values("symbol")

if missing.empty:
    print("No missing companies to import.")
    raise SystemExit(0)

companies = pd.concat([companies, missing], ignore_index=True)
companies = companies.sort_values("symbol")

new_themes = pd.DataFrame({
    "symbol": missing["symbol"],
    "vision2030_theme": "unclassified",
})

new_quality = pd.DataFrame({
    "symbol": missing["symbol"],
    "source_quality": "official",
    "source_note": "Official Saudi Exchange company profile link added.",
    "last_reviewed": TODAY,
})

new_sources = pd.DataFrame({
    "symbol": missing["symbol"],
    "official_profile_url": missing["symbol"].apply(lambda symbol: base_url.format(symbol=symbol)),
    "source_type": "official",
})

themes = pd.concat([themes, new_themes], ignore_index=True).sort_values("symbol")
quality = pd.concat([quality, new_quality], ignore_index=True).sort_values("symbol")
sources = pd.concat([sources, new_sources], ignore_index=True).sort_values("symbol")

companies.to_csv(current_path, index=False)
themes.to_csv(themes_path, index=False)
quality.to_csv(quality_path, index=False)
sources.to_csv(sources_path, index=False)

print(f"Imported {len(missing)} companies:")
for _, row in missing.iterrows():
    print(f"- {row['symbol']} — {row['name_ar']} — {row['sector']}")
