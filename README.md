# Saudi Market Classifier

Open classification layer for Saudi listed companies.

تصنيف مفتوح للشركات المدرجة في السوق السعودي، يهدف إلى تنظيم الشركات حسب القطاع، نوع النشاط، وثيمات رؤية 2030.

## What this project does

The project builds a structured reference layer for Saudi listed companies.

It currently classifies companies by:

- Market
- Sector
- Industry
- Business class
- Vision 2030 theme

This is useful for market research, sector mapping, company screening, and future Saudi market intelligence tools.

## What this project is not

This project is not an investment recommendation tool.

It does not provide buy, sell, or hold recommendations.

## Current version

v0.1 includes:

- 20 Saudi listed companies
- Business class mapping
- Vision 2030 theme mapping
- Processed classification output
- Markdown market overview report

## Project structure

```text
data/
  reference/
    companies.csv
    business_classes.csv
    vision2030_themes.csv
  processed/
    companies_classified.csv

reports/
  market_overview.md

src/
  saudi_market_classifier/
    classify.py
    report.py

run.py
ROADMAP.md
```

## Run

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the full pipeline:

```bash
python3 run.py
```

This will:

1. classify companies
2. create `data/processed/companies_classified.csv`
3. generate `reports/market_overview.md`

## Sample output

The generated report includes:

- number of companies
- number of sectors
- companies grouped by sector
- companies grouped by business class
- companies grouped by Vision 2030 theme

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Disclaimer

This project is for research and classification purposes only.

It is not financial advice.
