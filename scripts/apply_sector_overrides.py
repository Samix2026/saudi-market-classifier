from pathlib import Path
import pandas as pd


REVIEW_PATH = Path("data/raw/main_market_companies_review.csv")
OVERRIDES_PATH = Path("data/raw/main_market_sector_overrides.csv")
OUTPUT_PATH = Path("data/raw/main_market_companies_ready.csv")


def main():
    if not REVIEW_PATH.exists():
        print(f"Missing file: {REVIEW_PATH}")
        raise SystemExit(1)

    if not OVERRIDES_PATH.exists():
        print(f"Missing file: {OVERRIDES_PATH}")
        print("Create it with columns: symbol,sector")
        raise SystemExit(1)

    review = pd.read_csv(REVIEW_PATH)
    overrides = pd.read_csv(OVERRIDES_PATH)

    required = {"symbol", "sector"}
    missing = required - set(overrides.columns)
    if missing:
        print("Missing columns in overrides:")
        for column in sorted(missing):
            print(f"- {column}")
        raise SystemExit(1)

    overrides = overrides.dropna(subset=["symbol", "sector"])
    overrides["symbol"] = overrides["symbol"].astype(int)

    sector_map = dict(zip(overrides["symbol"], overrides["sector"]))

    mask_review = review["import_decision"].eq("review")
    review.loc[mask_review, "sector"] = review.loc[mask_review, "symbol"].map(sector_map).fillna(
        review.loc[mask_review, "sector"]
    )

    ready = review[
        review["import_decision"].eq("review")
        & review["sector"].fillna("").astype(str).str.strip().ne("")
    ].copy()

    ready = ready[["symbol", "name_ar", "name_en", "market", "sector"]]
    ready = ready.sort_values("symbol")

    ready.to_csv(OUTPUT_PATH, index=False)

    remaining = review[
        review["import_decision"].eq("review")
        & review["sector"].fillna("").astype(str).str.strip().eq("")
    ]

    print(f"Overrides: {len(overrides)}")
    print(f"Ready to import: {len(ready)}")
    print(f"Still needs sector: {len(remaining)}")
    print(f"Wrote: {OUTPUT_PATH}")

    if not ready.empty:
        print()
        print("Ready sample:")
        print(ready.head(40).to_string(index=False))

    if not remaining.empty:
        print()
        print("Still needs sector sample:")
        print(remaining[["symbol", "name_ar", "name_en"]].head(40).to_string(index=False))


if __name__ == "__main__":
    main()
