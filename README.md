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
- Source freshness layer: tracks official-source coverage and staleness
- Index membership layer: conservative market-structure mapping
- Seasonal exposure layer: Hajj/Ramadan thematic linkage
- Market intelligence matrix: one master row per company across all layers
- Public data package: portable, self-contained dataset bundle
- Local Streamlit dashboard: read-only exploration of the matrix
- 72 data quality tests passing

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
    index_memberships.csv      # Phase 5: عضوية المؤشرات
    seasonal_exposures.csv     # Phase 6: التعرّض الموسمي (حج/رمضان)
  processed/        # مخرجات يولّدها run.py
    companies_classified.csv
    companies_intelligence.csv # Phase 2: التصنيف + طبقة التعرّض
    companies_index_membership.csv # Phase 5: عضوية المؤشرات المُثراة
    companies_seasonal_exposure.csv # Phase 6: التعرّض الموسمي المُثرى
    market_intelligence_matrix.csv # Phase 7: المصفوفة الرئيسية

reports/            # تقارير Markdown مولّدة وموثّقة
  market_overview.md
  coverage_report.md
  excluded_or_deferred_companies.md
  holding_companies_review.md
  holding_companies_fix_recommendations.md
  mega_event_exposure_report.md
  review_queue.md
  source_freshness_report.md
  index_membership_report.md
  seasonal_exposure_report.md
  market_intelligence_matrix.md

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
    source_freshness.py        # Phase 4: توليد source_freshness_report.md
    index_membership.py        # Phase 5: توليد طبقة عضوية المؤشرات
    seasonal_exposure.py       # Phase 6: توليد طبقة التعرّض الموسمي
    market_matrix.py           # Phase 7: توليد المصفوفة الرئيسية
    public_package.py          # Phase 8: توليد حزمة البيانات العامة
public/             # Phase 8: حزمة بيانات محمولة (manifest + datasets + قاموس)
dashboard/          # Phase 9: لوحة Streamlit محلية للقراءة فقط
  app.py
  README.md
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
| Source freshness | حداثة المصادر وتغطية المصادر الرسمية | `reports/source_freshness_report.md` |
| Index membership | عضوية مؤشرات السوق (بنية سوق محافظة) | `reports/index_membership_report.md` |
| Seasonal exposure | التعرّض الموسمي المحتمل (حج/رمضان) | `reports/seasonal_exposure_report.md` |
| Market intelligence matrix | مصفوفة رئيسية تدمج كل الطبقات لكل شركة | `reports/market_intelligence_matrix.md` |
| Public data package | تقرير محتوى حزمة البيانات المحمولة | `reports/public_data_package_report.md` |

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

## Source Freshness Layer (Phase 4)

طبقة جودة بيانات تتتبع حداثة المصادر وتغطية المصادر الرسمية. المصدر:
`data/reference/companies.csv` (مع ضمّ حقول المصدر من ملفات المرجع).

الملف: `reports/source_freshness_report.md` (يولّده `run.py`).

يعرض:

- إجمالي الشركات، والتوزيع حسب `source_type`.
- عدد الشركات بدون `official_profile_url`.
- عدد السجلات بدون `last_reviewed`.
- عدد السجلات الأقدم من 90 يومًا، وجداول السجلات القديمة والروابط المفقودة.

التاريخ المرجعي مُشتق من **أحدث `last_reviewed`** في البيانات (وليس ساعة النظام)،
لإبقاء التقرير حتميًا وتفادي CI drift. تنبيه ثابت: تقرير جودة بيانات لا توصية استثمارية.

## Index Membership Layer (Phase 5)

طبقة بنية سوق محافظة تربط الشركات بعضوية مؤشرات السوق السعودي — **بدون تخمين
المكوّنات**. المكوّنات غير المؤكدة تُعلَّم `needs_verification` بدل الافتراض.

الملفات:

- `data/reference/index_memberships.csv` — مصدر العضوية القابل للتحرير.
- `data/processed/companies_index_membership.csv` — العضوية مُثراة بالاسم (يولّده `run.py`).
- `reports/index_membership_report.md` — توزيع وجداول التحقق.

- قيم `index_code` المسموحة: `TASI`، `MT30`، `TASI50`، `LARGE_CAP`، `MID_CAP`، `SMALL_CAP`.
- قيم `membership_status` المسموحة: `member`، `not_member`، `needs_verification`.
- الوضع الابتدائي محافظ: صف TASI لكل شركة بحالة `needs_verification` بانتظار لقطة رسمية مؤرخة.
- تنبيه ثابت: عضوية المؤشرات ليست توصية استثمارية.

## Seasonal Exposure Layer (Phase 6)

طبقة ربط موضوعي محافظة لموسمي **الحج (HAJJ)** و**رمضان (RAMADAN)** فقط،
من نموذج العمل — **لا** ادعاء باستفادة مضمونة أو عقود أو أثر إيرادي.

الملفات:

- `data/reference/seasonal_exposures.csv` — مصدر التعرّض القابل للتحرير (curated).
- `data/processed/companies_seasonal_exposure.csv` — التعرّض مُثرى بالاسم (يولّده `run.py`).
- `reports/seasonal_exposure_report.md` — توزيعات وجداول high/medium و needs_verification.

- `season`: `HAJJ`، `RAMADAN`. `exposure_level`: `high`/`medium`/`low`/`none`.
- `evidence_status`: `thematic_only` … `needs_verification` (لا إفصاح مالي مُدّعى).
- كل تعرّض `high`/`medium` يتطلب `rationale`؛ المجموعة الابتدائية روابط واضحة فقط.
- تنبيه ثابت: التعرّض الموسمي ليس توصية استثمارية.

## Market Intelligence Matrix (Phase 7)

مصفوفة رئيسية حتمية بصف واحد لكل شركة تدمج التصنيف مع كل طبقات الذكاء
(الفعاليات، عضوية المؤشرات، التعرّض الموسمي، حداثة المصدر) عبر `left join`،
مع الحفاظ على 259 شركة.

الملفات:

- `data/processed/market_intelligence_matrix.csv` — المصفوفة الكاملة (يولّدها `run.py`).
- `reports/market_intelligence_matrix.md` — توزيعات وجدول مخاطر high/medium.

- القيم المفقودة تصبح محايدة: `none` / `not_available` / `needs_verification`.
- `source_freshness_status` (`current`/`stale`/`missing`) يعتمد أحدث `last_reviewed` كمرساة — لا ساعة نظام.
- `review_priority` (`high`/`medium`/`low`/`none`) و `classification_risk` (`high`/`medium`/`low`)
  محسوبان بتحفّظ من البيانات المرجعية فقط.
- طبقة ذكاء سوق وجودة بيانات — ليست توصية استثمارية.

## Public Data Package (Phase 8)

حزمة بيانات محمولة قابلة للمشاركة داخل `public/`، تجمّع المخرجات المصنّفة
وطبقات الذكاء مع بيان (manifest) وقاموس بيانات وتنبيه ثابت.

المحتوى:

- `public/datasets/` — نسخ محمولة من 5 مجموعات بيانات (تصنيف، ذكاء، مؤشرات، موسمي، مصفوفة).
- `public/manifest.json` — بيان قابل للقراءة آليًا (datasets، أعمدة، عدد صفوف، تنبيه).
- `public/DATA_DICTIONARY.md` و `public/README.md` — توثيق الأعمدة والحزمة.
- `reports/public_data_package_report.md` — تقرير محتوى الحزمة.

- حتمي بالكامل: يستخدم `source_anchor_date` (أحدث `last_reviewed`) بدل `generated_at` — لا ساعة نظام.
- تنبيه ثابت: حزمة بحث وجودة بيانات — ليست توصية استثمارية.

## Dashboard (Phase 9)

لوحة **Streamlit محلية للقراءة فقط** تستعرض مصفوفة الذكاء السوقي — بدون نشر
ولا API ولا قاعدة بيانات. مصدر البيانات هو حزمة `public/`.

```bash
pip install -r requirements.txt   # يتضمن streamlit
streamlit run dashboard/app.py
```

- تقرأ `public/datasets/market_intelligence_matrix.csv` و `public/manifest.json`.
- بطاقات KPI، فلاتر، رسوم توزيع بسيطة، جدول، وملف تعريف لكل شركة.
- ليست مربوطة بـ `run.py` (ليست ناتجًا مولّدًا)؛ شغّل `run.py` أولًا لتحديث `public/`.
- تنبيه ثابت: للبحث وتنظيم البيانات فقط — ليست توصية استثمارية.
- التفاصيل في `dashboard/README.md`.

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
- Phase 4 Source Freshness Layer added (source coverage and staleness).
- Phase 5 Index Membership Layer added (conservative market structure).
- Phase 6 Seasonal Exposure Layer added (Hajj/Ramadan thematic linkage).
- Phase 7 Market Intelligence Matrix added (master row per company across all layers).
- Phase 8 Public Data Package added (portable bundle, deterministic source_anchor_date).
- Phase 9 local Streamlit dashboard added (read-only exploration of the matrix).
- Data quality tests added (72 tests).

## تنبيه

للبحث والتصنيف وتنظيم البيانات فقط. ليس نصيحة مالية ولا توصية بيع أو شراء.
