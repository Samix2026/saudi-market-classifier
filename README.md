# Saudi Market Classifier

تصنيف مفتوح للشركات المدرجة في السوق السعودي.

الهدف من المشروع هو بناء طبقة منظمة لفهم الشركات السعودية حسب:

- السوق
- القطاع
- الصناعة
- نوع النشاط
- الحجم
- السيولة
- ملف التوزيعات
- ارتباط الشركة بثيمات رؤية 2030

هذا المشروع ليس أداة توصيات استثمارية.

## Current version

v0.1 starts with a small reference dataset and a basic classification script.

## Run

```bash
python3 src/saudi_market_classifier/classify.py
```

Output:

```text
data/processed/companies_classified.csv
```

## Run full pipeline

```bash
python3 run.py
```

This runs classification and generates the market overview report.
