# Saudi Market Classifier

مصنف بيانات للشركات المدرجة في السوق السعودي، يربط الشركة بالقطاع، تصنيف النشاط، وثيمات رؤية 2030.

المشروع للبحث وتنظيم البيانات فقط — ليس توصية استثمارية ولا أهدافًا سعرية.

## Current Status

- 259 classified companies
- 12 deferred companies
- 16 sectors
- 16 business classes
- 14 Vision 2030 themes
- 0 unclassified Vision 2030 themes
- 12 data quality tests passing

## ما الذي يفعله المشروع

- يجمع وينظف ويصنّف بيانات الشركات المدرجة.
- ينتج ملف التصنيف الموحّد `data/processed/companies_classified.csv`.
- يولّد تقارير Markdown جاهزة للقراءة من البيانات المصنّفة.
- يحافظ على جودة البيانات عبر اختبارات `pytest`.

آلية التصنيف: `business_class` يُشتق من `sector` عبر `business_classes.csv`،
و `vision2030_theme` يُربط بالشركة عبر `vision2030_themes.csv` (انظر `src/saudi_market_classifier/classify.py`).

## Project structure

```text
data/
  reference/        # المصادر القابلة للتحرير
    companies.csv
    business_classes.csv
    vision2030_themes.csv
    source_quality.csv
    official_sources.csv
  processed/        # مخرجات يولّدها run.py
    companies_classified.csv

reports/            # تقارير Markdown مولّدة وموثّقة
  market_overview.md
  coverage_report.md
  excluded_or_deferred_companies.md
  holding_companies_review.md
  holding_companies_fix_recommendations.md

scripts/            # سكربتات جلب/تنظيف/استيراد مساعدة
src/
  saudi_market_classifier/
    validate.py
    classify.py
    report.py
    coverage.py
tests/              # اختبارات جودة البيانات (pytest)
run.py              # خط التشغيل الكامل
```

## Key reports

| report | purpose | path |
|---|---|---|
| Market overview | نظرة عامة على السوق: مؤشرات وجداول توزيع وقائمة تفصيلية حسب القطاع | `reports/market_overview.md` |
| Coverage report | لوحة جودة وتغطية البيانات | `reports/coverage_report.md` |
| Excluded / deferred | الشركات المؤجلة عن الاستيراد وأسبابها | `reports/excluded_or_deferred_companies.md` |
| Holding companies review | مراجعة تصنيف الشركات القابضة | `reports/holding_companies_review.md` |
| Holding fix recommendations | توصيات معالجة حالات needs_review | `reports/holding_companies_fix_recommendations.md` |

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

`run.py` يقوم بالتحقق من المصادر، ثم التصنيف، ثم توليد التقارير،
ويعيد كتابة `companies_classified.csv` و `reports/` من المصادر.

## How to test

```bash
pytest -q
```

## Data quality guarantees

اختبارات `tests/` تضمن:

- no duplicate symbols (في الملفات الأساسية الثلاثة).
- fixed company count guard (لا ينخفض العدد عن 259).
- symbol set match بين `companies.csv` و `companies_classified.csv`.
- no unclassified Vision 2030 theme.
- processed rows match source rows.

## Data scope and limits

- يغطي 259 شركة حاليًا.
- 12 شركة مؤجلة موثّقة في `reports/excluded_or_deferred_companies.md`.
- الشركات المؤجلة لا تُدخل تلقائيًا — تحتاج تحققًا رسميًا قبل الاستيراد.
- بعض الشركات القابضة تحتاج مراجعة دورية (انظر تقارير holding companies).
- القطاع مأخوذ من تصنيف السوق المالية الرسمي؛ أي تعديل عليه يحتاج تأكيدًا من مصدر رسمي.

## Recent improvements

- Vision 2030 coverage improved from 195 unclassified to 0.
- Holding company review added.
- Two high-confidence holding classifications fixed (4161 BinDawood، 6004 CATRION).
- Coverage report improved (لوحة جودة وتغطية).
- Market overview improved (مؤشرات وجداول توزيع وملخص تنفيذي).
- Data quality tests added (12 tests).

## تنبيه

للبحث والتصنيف وتنظيم البيانات فقط. ليس نصيحة مالية ولا توصية بيع أو شراء.
