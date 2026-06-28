import pandas as pd


def main():
    companies = pd.read_csv("data/reference/companies.csv")
    classes = pd.read_csv("data/reference/business_classes.csv")
    themes = pd.read_csv("data/reference/vision2030_themes.csv")
    source_quality = pd.read_csv("data/reference/source_quality.csv")

    classified = companies.merge(classes, on="sector", how="left")
    classified = classified.merge(themes, on="symbol", how="left")
    classified = classified.merge(source_quality, on="symbol", how="left")

    classified["business_class"] = classified["business_class"].fillna("other")
    classified["vision2030_theme"] = classified["vision2030_theme"].fillna("unclassified")
    classified["source_quality"] = classified["source_quality"].fillna("unreviewed")
    classified["source_note"] = classified["source_note"].fillna("")
    classified["last_reviewed"] = classified["last_reviewed"].fillna("")

    classified.to_csv("data/processed/companies_classified.csv", index=False)
    print(classified)


if __name__ == "__main__":
    main()
