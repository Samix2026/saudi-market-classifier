from pathlib import Path
import pandas as pd


RAW_PATH = Path("data/raw/main_market_companies.csv")
CLEAN_PATH = Path("data/raw/main_market_companies_clean.csv")
REVIEW_PATH = Path("data/raw/main_market_companies_needs_sector.csv")
EXCLUDED_PATH = Path("data/raw/excluded_non_main_market.csv")

EXCLUDE_AR_KEYWORDS = [
    "صكوك",
    "صندوق",
    "أداة دين",
]

EXCLUDE_EN_KEYWORDS = [
    "SUKUK",
    "REIT",
    "ETF",
    "Fund",
    "FRNs",
]


def contains_any(text, keywords):
    text = str(text)
    return any(keyword.lower() in text.lower() for keyword in keywords)


def main():
    if not RAW_PATH.exists():
        print(f"Missing file: {RAW_PATH}")
        raise SystemExit(1)

    raw = pd.read_csv(RAW_PATH)

    required = {"symbol", "name_ar", "name_en", "market", "sector"}
    missing_columns = required - set(raw.columns)

    if missing_columns:
        print("Missing columns:")
        for column in sorted(missing_columns):
            print(f"- {column}")
        raise SystemExit(1)

    df = raw.copy()

    # Keep only Main Market rows.
    # M = Main Market
    # S = Nomu / Parallel Market, handled later
    # B/O = Sukuk and bonds
    # E/C = ETFs and traded funds
    main_market = df["market"].astype(str).str.strip().eq("M")
    excluded = df[~main_market].copy()
    df = df[main_market].copy()

    # Remove rows with no Arabic and English names.
    df = df[
        df["name_ar"].fillna("").astype(str).str.strip().ne("")
        | df["name_en"].fillna("").astype(str).str.strip().ne("")
    ]

    # Exclude sukuk, bonds, funds, ETFs, and REITs if they slipped into M.
    mask_excluded_in_main = (
        df["name_ar"].fillna("").apply(lambda x: contains_any(x, EXCLUDE_AR_KEYWORDS))
        | df["name_en"].fillna("").apply(lambda x: contains_any(x, EXCLUDE_EN_KEYWORDS))
    )

    excluded = pd.concat([excluded, df[mask_excluded_in_main]], ignore_index=True)
    df = df[~mask_excluded_in_main].copy()

    df = df.drop_duplicates(subset=["symbol"]).sort_values("symbol")
    excluded = excluded.drop_duplicates(subset=["symbol"]).sort_values("symbol")

    # Rows without sector need review before import.
    needs_sector = df[df["sector"].fillna("").astype(str).str.strip().eq("")].copy()
    clean = df[df["sector"].fillna("").astype(str).str.strip().ne("")].copy()

    clean.to_csv(CLEAN_PATH, index=False)
    needs_sector.to_csv(REVIEW_PATH, index=False)
    excluded.to_csv(EXCLUDED_PATH, index=False)

    print(f"Raw rows: {len(raw)}")
    print(f"Main Market company rows: {len(df)}")
    print(f"Clean import-ready rows: {len(clean)}")
    print(f"Rows needing sector review: {len(needs_sector)}")
    print(f"Excluded non-main-market / instruments: {len(excluded)}")
    print()
    print(f"Wrote: {CLEAN_PATH}")
    print(f"Wrote: {REVIEW_PATH}")
    print(f"Wrote: {EXCLUDED_PATH}")

    if not needs_sector.empty:
        print()
        print("Sample rows needing sector:")
        print(needs_sector.head(30).to_string(index=False))


if __name__ == "__main__":
    main()
