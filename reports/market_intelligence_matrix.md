# مصفوفة الذكاء السوقي (Market Intelligence Matrix)

> **تنبيه:** مصفوفة ذكاء سوقي وجودة بيانات فقط. ليست توصية استثمارية ولا نصيحة مالية، ولا تتضمن لغة شراء/بيع أو ادعاء استفادة أو عقود أو أثر إيرادي.

صف واحد لكل شركة يدمج التصنيف مع طبقات: الفعاليات، عضوية المؤشرات، التعرّض الموسمي، وحداثة المصدر.

## الملخص التنفيذي

| المؤشر | العدد |
|---|---:|
| إجمالي الشركات | 259 |
| مخاطر تصنيف high/medium | 25 |

## التوزيع حسب classification_risk

| القيمة | العدد |
|---|---:|
| low | 234 |
| medium | 25 |

## التوزيع حسب review_priority

| القيمة | العدد |
|---|---:|
| none | 234 |
| medium | 25 |

## التوزيع حسب vision2030_theme

| القيمة | العدد |
|---|---:|
| industrial_development | 65 |
| financial_sector_development | 47 |
| quality_of_life_and_retail | 43 |
| food_security_and_industry | 24 |
| healthcare_quality | 15 |
| housing_and_real_estate | 15 |
| logistics_and_transport | 12 |
| digital_transformation | 11 |
| energy | 10 |
| labor_market_and_services | 9 |
| healthcare_access | 3 |
| food_security_and_retail | 2 |
| utilities_and_infrastructure | 2 |
| renewable_energy_and_utilities | 1 |

## التوزيع حسب event_exposure_overall

| القيمة | العدد |
|---|---:|
| none | 205 |
| medium | 37 |
| high | 17 |

## التوزيع حسب seasonal_hajj_exposure

| القيمة | العدد |
|---|---:|
| none | 246 |
| medium | 8 |
| high | 4 |
| low | 1 |

## التوزيع حسب seasonal_ramadan_exposure

| القيمة | العدد |
|---|---:|
| none | 247 |
| medium | 7 |
| high | 4 |
| low | 1 |

## التوزيع حسب source_freshness_status

| القيمة | العدد |
|---|---:|
| current | 259 |

## جدول مخاطر التصنيف high/medium

| symbol | name_ar | classification_risk | review_priority | event_exposure_overall | source_freshness_status |
|---|---|---|---|---|---|
| 1301 | أسلاك | medium | medium | medium | current |
| 1304 | شركة اليمامة للصناعات الحديدية | medium | medium | medium | current |
| 1320 | الشركة السعودية لأنابيب الصلب | medium | medium | medium | current |
| 1321 | شركة أنابيب الشرق المتكاملة للصناعة | medium | medium | medium | current |
| 1833 | الموارد | medium | medium | medium | current |
| 1835 | شركة تمكين للموارد البشرية | medium | medium | medium | current |
| 2040 | الخزف السعودي | medium | medium | medium | current |
| 2270 | الشركة السعودية لمنتجات الألبان والأغذية | medium | medium | none | current |
| 3010 | شركة الأسمنت العربية | medium | medium | medium | current |
| 3030 | شركة الأسمنت السعودية | medium | medium | medium | current |
| 3050 | شركة أسمنت المنطقة الجنوبية | medium | medium | medium | current |
| 4070 | شركة تهامة للإعلان والعلاقات العامة والتسويق | medium | medium | medium | current |
| 4090 | شركة طيبة للإستثمار | medium | medium | medium | current |
| 4100 | شركة مكة للإنشاء والتعمير | medium | medium | medium | current |
| 4145 | شركة العبيكان للزجاج | medium | medium | medium | current |
| 4161 | شركة بن داود القابضة | medium | medium | none | current |
| 4170 | شركة المشروعات السياحية | medium | medium | high | current |
| 4260 | الشركة المتحدة الدولية للمواصلات | medium | medium | medium | current |
| 4261 | شركة ذيب لتأجير السيارات | medium | medium | medium | current |
| 4320 | الأندلس | medium | medium | medium | current |
| 4323 | شركة سمو العقارية | medium | medium | medium | current |
| 6004 | شركة كاتريون للتموين القابضة | medium | medium | high | current |
| 6012 | شركة ريدان الغذائية | medium | medium | medium | current |
| 6015 | شركة أمريكانا للمطاعم العالمية بي إل سي - شركة أجنبية | medium | medium | medium | current |
| 7204 | شركة العرض المتقن للخدمات التجارية | medium | medium | medium | current |

## ملاحظات منهجية

- المصدر: `companies_classified` + طبقات الذكاء (left join، 259 صفًا محفوظة).
- القيم المفقودة تصبح محايدة: `none` / `not_available` / `needs_verification`.
- `source_freshness_status` يعتمد أحدث `last_reviewed` كمرساة (لا ساعة نظام).
- `review_priority` و `classification_risk` محسوبان بتحفّظ من البيانات المرجعية.
- طبقة جودة بيانات وذكاء سوق — ليست توصية استثمارية.

