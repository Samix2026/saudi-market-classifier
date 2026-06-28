import pandas as pd


def classify_company(row):
    sector = row["sector"]

    if "البنوك" in sector:
        return "financial"
    if "الطاقة" in sector:
        return "energy"
    if "الاتصالات" in sector:
        return "digital_infrastructure"
    if "المواد" in sector:
        return "basic_materials"

    return "other"


def main():
    df = pd.read_csv("data/reference/companies.csv")
    df["business_class"] = df.apply(classify_company, axis=1)

    df.to_csv("data/processed/companies_classified.csv", index=False)
    print(df)


if __name__ == "__main__":
    main()
