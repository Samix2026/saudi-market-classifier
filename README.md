# مصنف السوق السعودي

مصنف مفتوح للشركات المدرجة في السوق السعودي.

يهدف المشروع إلى بناء طبقة مرجعية منظمة تساعد على فهم الشركات السعودية حسب القطاع، نوع النشاط، ثيمات رؤية 2030، وجودة مصدر البيانات.

## ما هو المشروع؟

هذا المشروع ينظم بيانات الشركات المدرجة في السوق السعودي في ملفات مرجعية قابلة للتطوير.

الفكرة ليست توقع أسعار الأسهم، وليست توصيات شراء أو بيع.

الفكرة هي بناء قاعدة تصنيف واضحة يمكن استخدامها لاحقًا في:

- تحليل السوق السعودي
- مقارنة القطاعات
- بناء خرائط للشركات المدرجة
- دعم أدوات بحث أو ذكاء اصطناعي عن السوق السعودي
- بناء تقارير قطاعية منظمة

## ماذا يصنف المشروع؟

يصنف المشروع الشركات حسب:

- السوق
- القطاع
- الصناعة
- تصنيف النشاط
- ثيم رؤية 2030
- جودة مصدر البيانات
- تاريخ آخر مراجعة

## ما الذي لا يفعله المشروع؟

هذا المشروع لا يقدم توصيات استثمارية.

لا يقدم:

- توصية شراء
- توصية بيع
- أهداف سعرية
- توقعات ربحية
- قرارات تداول

المشروع مخصص للتصنيف والبحث وتنظيم البيانات فقط.

## النسخة الحالية

تغطي النسخة الحالية:

- 64 شركة سعودية مدرجة
- 15 قطاعًا
- 15 تصنيف نشاط
- 14 ثيمًا مرتبطًا برؤية 2030
- تقرير نظرة عامة على السوق
- تقرير تغطية البيانات
- طبقة جودة مصادر البيانات

## هيكل المشروع

```text
data/
  reference/
    companies.csv
    business_classes.csv
    vision2030_themes.csv
    source_quality.csv

  processed/
    companies_classified.csv

reports/
  market_overview.md
  coverage_report.md

src/
  saudi_market_classifier/
    classify.py
    coverage.py
    report.py
    validate.py

run.py
ROADMAP.md
LICENSE
```

## طريقة التشغيل

ثبت المتطلبات:

```bash
python3 -m pip install -r requirements.txt
```

شغل المشروع كاملًا:

```bash
python3 run.py
```

هذا الأمر يقوم بالآتي:

1. التحقق من اكتمال ملفات البيانات المرجعية
2. تصنيف الشركات
3. إنشاء ملف `data/processed/companies_classified.csv`
4. إنشاء تقرير `reports/market_overview.md`
5. إنشاء تقرير `reports/coverage_report.md`

## التقارير

ينتج المشروع تقريرين:

### `reports/market_overview.md`

يعرض نظرة عامة على الشركات المصنفة، مع تجميع الشركات حسب القطاع، وتصنيف النشاط، وثيمات رؤية 2030.

### `reports/coverage_report.md`

يعرض مستوى تغطية البيانات، ونسبة التغطية التقريبية، وجودة مصادر البيانات، والشركات التي تحتاج إلى تحقق رسمي لاحقًا.

## جودة البيانات

يستخدم المشروع ملف:

```text
data/reference/source_quality.csv
```

لتوضيح جودة مصدر البيانات لكل شركة.

القيم الحالية تبدأ بـ:

```text
manual
```

وهذا يعني أن البيانات أضيفت يدويًا وتحتاج لاحقًا إلى مراجعة مقابل مصدر رسمي.

## خارطة الطريق

راجع ملف:

```text
ROADMAP.md
```

## تنبيه

هذا المشروع لأغراض البحث والتصنيف وتنظيم البيانات فقط.

لا يعد نصيحة مالية أو توصية استثمارية.

---

## English Summary

Saudi Market Classifier is an open classification layer for Saudi listed companies.

It organizes companies by market, sector, industry, business class, Vision 2030 theme, and source quality.

The project is intended for research, market mapping, and future Saudi market intelligence tools.

It is not an investment recommendation tool and does not provide buy, sell, or hold recommendations.
