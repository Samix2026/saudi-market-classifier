import pandas as pd


def main():
    companies = pd.read_csv("data/reference/companies.csv")
    classes = pd.read_csv("data/reference/business_classes.csv")

    classified = companies.merge(classes, on="sector", how="left")
    classified["business_class"] = classified["business_class"].fillna("other")

    classified.to_csv("data/processed/companies_classified.csv", index=False)
    print(classified)


if __name__ == "__main__":
    main()
