import sys

import pandas as pd


def main():
    companies = pd.read_csv("data/reference/companies.csv")
    classes = pd.read_csv("data/reference/business_classes.csv")
    themes = pd.read_csv("data/reference/vision2030_themes.csv")
    source_quality = pd.read_csv("data/reference/source_quality.csv")

    errors = []

    missing_classes = companies[~companies["sector"].isin(classes["sector"])]
    if not missing_classes.empty:
        errors.append("Missing business_class mapping for sectors:")
        for sector in sorted(missing_classes["sector"].unique()):
            errors.append(f"- {sector}")

    missing_themes = companies[~companies["symbol"].isin(themes["symbol"])]
    if not missing_themes.empty:
        errors.append("Missing Vision 2030 theme mapping for companies:")
        for _, row in missing_themes.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    missing_source_quality = companies[~companies["symbol"].isin(source_quality["symbol"])]
    if not missing_source_quality.empty:
        errors.append("Missing source quality mapping for companies:")
        for _, row in missing_source_quality.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    duplicate_symbols = companies[companies["symbol"].duplicated(keep=False)]
    if not duplicate_symbols.empty:
        errors.append("Duplicate symbols found:")
        for _, row in duplicate_symbols.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
