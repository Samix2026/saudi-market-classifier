from pathlib import Path
import pandas as pd


RAW_PATH = Path("data/raw/main_market_companies.csv")
CURRENT_PATH = Path("data/reference/companies.csv")
REVIEW_PATH = Path("data/raw/main_market_companies_review.csv")

EXCLUDE_AR_KEYWORDS = ["صكوك", "صندوق", "أداة دين"]
EXCLUDE_EN_KEYWORDS = ["SUKUK", "REIT", "ETF", "Fund", "FRNs"]


def contains_any(text, keywords):
    text = str(text)
    return any(keyword.lower() in text.lower() for keyword in keywords)


def main():
    raw = pd.read_csv(RAW_PATH)
    current = pd.read_csv(CURRENT_PATH)

    df = raw.copy()

    # السوق الرئيسية فقط
    df = df[df["market"].astype(str).str.strip().eq("M")].copy()

    # استبعاد الصكوك والصناديق لو تسربت
    excluded = (
        df["name_ar"].fillna("").apply(lambda x: contains_any(x, EXCLUDE_AR_KEYWORDS))
        | df["name_en"].fillna("").apply(lambda x: contains_any(x, EXCLUDE_EN_KEYWORDS))
    )
    df = df[~excluded].copy()

    # حذف الصفوف بلا اسم
    df = df[
        df["name_ar"].fillna("").astype(str).str.strip().ne("")
        | df["name_en"].fillna("").astype(str).str.strip().ne("")
    ].copy()

    df = df.drop_duplicates(subset=["symbol"]).sort_values("symbol")

    current_sectors = current[["symbol", "sector"]].rename(
        columns={"sector": "sector_from_current_project"}
    )

    review = df.merge(current_sectors, on="symbol", how="left")

    review["existing_in_project"] = review["sector_from_current_project"].notna()
    review["sector"] = review["sector_from_current_project"].fillna("")
    review["import_decision"] = review["existing_in_project"].map(
        {True: "already_exists", False: "review"}
    )
    review["review_note"] = ""

    review = review[
        [
            "symbol",
            "name_ar",
            "name_en",
            "market",
            "sector",
            "existing_in_project",
            "import_decision",
            "review_note",
        ]
    ]

    review.to_csv(REVIEW_PATH, index=False)

    print(f"Main Market review rows: {len(review)}")
    print(f"Already in project: {review['existing_in_project'].sum()}")
    print(f"Needs review: {(review['import_decision'] == 'review').sum()}")
    print(f"Wrote: {REVIEW_PATH}")

    print()
    print("Sample needs review:")
    print(review[review["import_decision"] == "review"].head(40).to_string(index=False))


if __name__ == "__main__":
    main()
