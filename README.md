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
- Market intelligence layer: mega-event potential exposure (Expo 2030، World Cup 2034)
- Review queue layer: aggregates all items needing human review
- 24 data quality tests passing

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
    mega_event_exposures.csv   # Phase 2: التعرّض المحتمل للفعاليات
  processed/        # مخرجات يولّدها run.py
    companies_classified.csv
    companies_intelligence.csv # Phase 2: التصنيف + طبقة التعرّض

reports/            # تقارير Markdown مولّدة وموثّقة
  market_overview.md
  coverage_report.md
  excluded_or_deferred_companies.md
  holding_companies_review.md
  holding_companies_fix_recommendations.md
  mega_event_exposure_report.md
  review_queue.md

scripts/            # سكربتات جلب/تنظيف/استيراد مساعدة
src/
  saudi_market_classifier/
    validate.py
    classify.py
    report.py
    coverage.py
    intelligence.py            # Phase 2: توليد companies_intelligence.csv
    event_report.py            # Phase 2: تقرير التعرّض للفعاليات
    review_queue.py            # Phase 3: توليد review_queue.md
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
| Mega event exposure | التعرّض المحتمل لإكسبو 2030 وكأس العالم 2034 | `reports/mega_event_exposure_report.md` |
| Review queue | كل عناصر المراجعة البشرية/التحقق مرتّبة بالأولوية | `reports/review_queue.md` |

## Market Intelligence Taxonomy (Phase 2)

طبقة قيمة مضافة فوق بيانات تداول: المستودع لم يعد تصنيفًا فقط، بل يضيف
**طبقة ذكاء سوقي** تقدّر التعرّض الموضوعي المحتمل للفعاليات الكبرى:

- **Expo 2030 Riyadh** و **FIFA World Cup 2034 Saudi Arabia**.
- التعرّض مبني على **القطاع ونموذج العمل فقط** — `potential exposure / thematic linkage`.
- **ليس** ادعاء عقود أو استفادة مباشرة، وليس توصية استثمارية.

الملفات:

- `data/reference/mega_event_exposures.csv` — مصدر التعرّض القابل للتحرير (curated).
- `data/processed/companies_intelligence.csv` — التصنيف + طبقة التعرّض (يولّده `run.py`).
- `reports/mega_event_exposure_report.md` — تقرير بتنبيه ثابت وجداول التعرّض.

الضمانات:

- تغطية 259 صفًا محفوظة في `companies_intelligence.csv` (left join).
- التحقق من القيم ضمن المجموعات المسموحة (exposure / driver / confidence).
- `rationale` إلزامي لأي تعرّض `high`/`medium`.
- لغة ممنوعة محجوبة باختبار: `beneficiary` / `winner` / `guaranteed`.
- CI drift guard يتحقق أن المخرجات المولّدة مطابقة للمصدر.

## Review Queue Layer (Phase 3)

طبقة جودة/إبلاغ تجمع في تقرير واحد كل الشركات التي تحتاج مراجعة بشرية أو
تحققًا رسميًا، من المصادر والتقارير الموجودة فقط (لا تغيّر أي تصنيف).

الملف: `reports/review_queue.md` (يولّده `run.py`).

يجمع:

- الشركات المؤجلة من السوق الرئيسية.
- الشركات القابضة بحالة `needs_review`.
- تعرّض الفعاليات بثقة منخفضة.
- أي تعرّض `high`/`medium` بدون `rationale`.

الأولوية:

- `high` — تعرّض high/medium بدون rationale، أو شركة مؤجلة من السوق الرئيسية.
- `medium` — شركة قابضة needs_review، أو تعرّض high/medium بثقة منخفضة.
- `low` — عنصر مراجعة معلوماتي (تحقق مصدر رسمي لاحقًا).

الضمانات: تنبيه ثابت (ليس توصية استثمارية)، لا تكرار `(symbol, reason)`،
كل عنصر له أولوية، واكتشاف حالات rationale المفقود إن وُجدت.

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
- mega-event exposures: allowed values، rationale إلزامي لـ high/medium، لا لغة ممنوعة.

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
- Deterministic report ordering (stable tie-breaks) to remove CI drift.
- Phase 2 Market Intelligence Taxonomy added (mega-event potential exposure).
- Phase 3 Review Queue Layer added (aggregated review items by priority).
- Data quality tests added (24 tests).

## تنبيه

للبحث والتصنيف وتنظيم البيانات فقط. ليس نصيحة مالية ولا توصية بيع أو شراء.
