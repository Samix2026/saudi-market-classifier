# توصيات معالجة الشركات القابضة (needs_review)

> تقرير توصيات فقط — لا يعدّل أي بيانات أو تصنيفات.
> المصدر: `reports/holding_companies_review.md`، `data/processed/companies_classified.csv`،
> `data/reference/companies.csv`، `data/reference/business_classes.csv`،
> `data/reference/vision2030_themes.csv`.

## آلية التصنيف المهمة

`business_class` **لا يُحرَّر مباشرة** — يُشتق من حقل `sector` في `companies.csv`
عبر جدول `business_classes.csv` (انظر `classify.py`). و `vision2030_theme` يأتي من
`vision2030_themes.csv` بمفتاح `symbol`.

لذلك أي توصية بتغيير `business_class` تعني عمليًا **تعديل حقل `sector`** في
`companies.csv` (وهو القطاع الرسمي من السوق المالية)، إضافة لتعديل الثيم في
`vision2030_themes.csv`. تغيير القطاع الرسمي يحتاج تحققًا من مصدر رسمي قبل التطبيق.

## الملخص

| المؤشر | العدد |
|---|---|
| حالات تمت مراجعتها | 8 |
| موصى بتغيير CSV | 2 (4161، 6004) |
| موصى بالإبقاء كما هو | 6 |

## التوصيات

### 2340 — شركة ارتيكس للاستثمار الصناعي

- current_sector: تجزئة وتوزيع السلع الكمالية
- current_business_class: consumer_retail
- current_vision2030_theme: quality_of_life_and_retail
- recommended_business_class: consumer_retail (دون تغيير)
- recommended_vision2030_theme: quality_of_life_and_retail (دون تغيير)
- confidence: medium
- reason: الاسم يوحي بـ "استثمار صناعي" لكن القطاع الرسمي في السوق المالية هو تجزئة
  وتوزيع السلع الكمالية. القطاع الرسمي يحكم التصنيف، والاسم وحده لا يكفي للتجاوز.
- whether_csv_change_is_recommended: no

### 4080 — شركة سناد القابضة

- current_sector: تجزئة وتوزيع السلع الكمالية
- current_business_class: consumer_retail
- current_vision2030_theme: quality_of_life_and_retail
- recommended_business_class: consumer_retail (دون تغيير)
- recommended_vision2030_theme: quality_of_life_and_retail (دون تغيير)
- confidence: medium
- reason: شركة قابضة متنوعة، لكن القطاع الرسمي يضعها ضمن تجزئة السلع الكمالية. لا يوجد
  دليل رسمي يبرر إعادة التصنيف، والإبقاء يتسق مع تصنيف السوق المالية.
- whether_csv_change_is_recommended: no

### 4130 — شركة درب السعودية الاستثمارية

- current_sector: الخدمات المالية
- current_business_class: financial_services
- current_vision2030_theme: financial_sector_development
- recommended_business_class: financial_services (دون تغيير)
- recommended_vision2030_theme: financial_sector_development (دون تغيير)
- confidence: high
- reason: شركة استثمارية والقطاع الرسمي خدمات مالية. التصنيف والثيم متسقان تمامًا مع
  طبيعة النشاط. لا حاجة لأي تغيير.
- whether_csv_change_is_recommended: no

### 4147 — شركة اتحاد جروننفلدر سعدي القابضة

- current_sector: تجزئة وتوزيع السلع الكمالية
- current_business_class: consumer_retail
- current_vision2030_theme: quality_of_life_and_retail
- recommended_business_class: consumer_retail (دون تغيير)
- recommended_vision2030_theme: quality_of_life_and_retail (دون تغيير)
- confidence: medium
- reason: قابضة، والقطاع الرسمي تجزئة سلع كمالية. بدون مصدر رسمي يحدد نشاطًا مهيمنًا
  مختلفًا، الإبقاء على التصنيف الرسمي هو الأسلم.
- whether_csv_change_is_recommended: no

### 4160 — شركة ثمار التنمية القابضة

- current_sector: الخدمات التجارية والمهنية
- current_business_class: commercial_services
- current_vision2030_theme: labor_market_and_services
- recommended_business_class: commercial_services (دون تغيير)
- recommended_vision2030_theme: labor_market_and_services (دون تغيير)
- confidence: medium
- reason: قابضة تنموية، والقطاع الرسمي خدمات تجارية ومهنية. التصنيف يتسق مع القطاع
  الرسمي ولا يوجد سبب موثق لتغييره.
- whether_csv_change_is_recommended: no

### 4161 — شركة بن داود القابضة

- current_sector: الخدمات التجارية والمهنية
- current_business_class: commercial_services
- current_vision2030_theme: labor_market_and_services
- recommended_business_class: consumer_defensive (عبر قطاع: تجزئة الأغذية)
- recommended_vision2030_theme: food_security_and_retail
- confidence: high
- reason: بن داود القابضة هي مشغّل رئيسي لمتاجر التجزئة الغذائية (أسواق بن داود ودانوب).
  تصنيفها كـ "خدمات تجارية ومهنية" لا يعكس النشاط الفعلي (تجزئة أغذية). القطاع الأدق هو
  تجزئة الأغذية → consumer_defensive، والثيم الأنسب food_security_and_retail.
- whether_csv_change_is_recommended: yes
  - الإجراء: تعديل `sector` في `companies.csv` إلى "تجزئة الأغذية"، وتحديث الثيم في
    `vision2030_themes.csv` إلى `food_security_and_retail`، بعد تأكيد القطاع الرسمي من
    السوق المالية.

### 4280 — شركة المملكة القابضة

- current_sector: الخدمات المالية
- current_business_class: financial_services
- current_vision2030_theme: financial_sector_development
- recommended_business_class: financial_services (دون تغيير)
- recommended_vision2030_theme: financial_sector_development (دون تغيير)
- confidence: medium
- reason: المملكة القابضة شركة استثمار متنوعة، والقطاع الرسمي خدمات مالية. رغم تنوع
  الأصول، تصنيف الخدمات المالية مقبول ومتسق مع تصنيف السوق المالية. لا يلزم تغيير.
- whether_csv_change_is_recommended: no

### 6004 — شركة كاتريون للتموين القابضة

- current_sector: المرافق العامة
- current_business_class: utilities
- current_vision2030_theme: utilities_and_infrastructure
- recommended_business_class: consumer_services (عبر قطاع: الخدمات الاستهلاكية)
- recommended_vision2030_theme: quality_of_life_and_retail
- confidence: high
- reason: كاتريون شركة تموين وضيافة (catering)، ووضعها ضمن "المرافق العامة" (utilities)
  غير دقيق بوضوح. النشاط خدمات استهلاكية، فالقطاع الأدق "الخدمات الاستهلاكية" →
  consumer_services، والثيم الأنسب quality_of_life_and_retail.
- whether_csv_change_is_recommended: yes
  - الإجراء: تعديل `sector` في `companies.csv` إلى "الخدمات الاستهلاكية"، وتحديث الثيم
    في `vision2030_themes.csv` إلى `quality_of_life_and_retail`، بعد تأكيد القطاع
    الرسمي من السوق المالية.

## خلاصة

- إصلاحان واضحان مرشّحان (4161، 6004) بثقة عالية، لكنهما يتطلبان تعديل القطاع الرسمي
  في `companies.csv` وبالتالي يجب تأكيدهما من مصدر رسمي قبل التطبيق.
- ست حالات يُوصى بإبقائها كما هي لاتساقها مع القطاع الرسمي للسوق المالية.
- لم تُعدَّل أي بيانات في هذا التقرير.
