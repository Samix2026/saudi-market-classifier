# تقرير التعرّض الموسمي (Seasonal Exposure)

> **تنبيه:** هذا التقرير يعرض **تعرّضًا موسميًا محتملًا / ربطًا موضوعيًا (thematic linkage)** بناءً على نموذج العمل فقط. لا يدّعي استفادة مضمونة أو عقودًا أو أثرًا إيراديًا، وليس توصية استثمارية.

الموسمان: الحج (HAJJ)، رمضان (RAMADAN). ربط موضوعي محافظ من نموذج العمل فقط.

## الملخص التنفيذي

| المؤشر | العدد |
|---|---:|
| إجمالي صفوف التعرّض | 25 |
| تعرّض high/medium | 23 |
| صفوف needs_verification | 2 |
| high/medium بدون rationale | 0 |

## التوزيع حسب season

| season | العدد |
|---|---:|
| HAJJ | 13 |
| RAMADAN | 12 |

## التوزيع حسب exposure_level

| exposure_level | العدد |
|---|---:|
| medium | 15 |
| high | 8 |
| low | 2 |

## التوزيع حسب primary_driver

| primary_driver | العدد |
|---|---:|
| food_retail | 5 |
| hospitality | 4 |
| advertising_media | 3 |
| real_estate_makkah_madinah | 3 |
| restaurants | 3 |
| telecom | 2 |
| transport | 2 |
| airlines | 1 |
| consumer_goods | 1 |
| ground_services | 1 |

## التوزيع حسب confidence

| confidence | العدد |
|---|---:|
| medium | 11 |
| low | 9 |
| high | 5 |

## تعرّض high/medium

| symbol | name_ar | season | exposure | primary_driver | confidence |
|---|---|---|---|---|---|
| 1810 | مجموعة سيرا القابضة | HAJJ | medium | hospitality | medium |
| 4010 | شركة دور للضيافة | HAJJ | high | hospitality | high |
| 4031 | الخدمات الأرضية | HAJJ | high | ground_services | medium |
| 4040 | الشركة السعودية للنقل الجماعي | HAJJ | medium | transport | medium |
| 4090 | شركة طيبة للإستثمار | HAJJ | medium | real_estate_makkah_madinah | low |
| 4100 | شركة مكة للإنشاء والتعمير | HAJJ | medium | real_estate_makkah_madinah | medium |
| 4161 | شركة بن داود القابضة | HAJJ | medium | food_retail | low |
| 4170 | شركة المشروعات السياحية | HAJJ | medium | hospitality | low |
| 4250 | شركة جبل عمر للتطوير | HAJJ | high | real_estate_makkah_madinah | high |
| 4264 | شركة طيران ناس | HAJJ | high | airlines | medium |
| 6004 | شركة كاتريون للتموين القابضة | HAJJ | medium | hospitality | low |
| 7010 | stc | HAJJ | medium | telecom | medium |
| 2050 | مجموعة صافولا | RAMADAN | high | consumer_goods | medium |
| 2280 | شركة المراعي | RAMADAN | high | food_retail | high |
| 4070 | شركة تهامة للإعلان والعلاقات العامة والتسويق | RAMADAN | medium | advertising_media | low |
| 4072 | شركة مجموعة إم بي سي | RAMADAN | high | advertising_media | high |
| 4161 | شركة بن داود القابضة | RAMADAN | high | food_retail | high |
| 4210 | المجموعة السعودية للأبحاث والإعلام | RAMADAN | medium | advertising_media | medium |
| 6002 | هرفي للأغذية | RAMADAN | medium | restaurants | medium |
| 6010 | نادك | RAMADAN | medium | food_retail | medium |
| 6012 | شركة ريدان الغذائية | RAMADAN | medium | restaurants | low |
| 6015 | شركة أمريكانا للمطاعم العالمية بي إل سي - شركة أجنبية | RAMADAN | medium | restaurants | low |
| 7010 | stc | RAMADAN | medium | telecom | medium |

## صفوف needs_verification

| symbol | name_ar | season | primary_driver |
|---|---|---|---|
| 4261 | شركة ذيب لتأجير السيارات | HAJJ | transport |
| 2270 | الشركة السعودية لمنتجات الألبان والأغذية | RAMADAN | food_retail |

## high/medium بدون rationale

- لا يوجد.

## ملاحظات منهجية

- المصدر القابل للتحرير: `data/reference/seasonal_exposures.csv`.
- التعرّض مشتق من نموذج العمل فقط، لا من عقود أو إفصاحات مالية.
- كل تعرّض high/medium يتطلب rationale؛ غير الكافي يُخفَّض أو يُعلَّم needs_verification.
- المجموعة الابتدائية محافظة: روابط موضوعية واضحة فقط، وليست تغطية شاملة.

