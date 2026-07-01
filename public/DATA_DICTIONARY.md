# Data Dictionary — Saudi Market Classifier Public Data

> This dataset is provided for research, market-mapping and data-quality purposes only. It is NOT investment advice and contains no buy/sell recommendations, guaranteed-benefit, contract, or revenue-impact claims.

_source_anchor_date (newest last_reviewed): 2026-06-28_

## `datasets/companies_classified.csv` (259 rows)

التصنيف الأساسي: قطاع، تصنيف نشاط، ثيم رؤية 2030، جودة المصدر.

| column |
|---|
| `symbol` |
| `name_ar` |
| `name_en` |
| `market` |
| `sector` |
| `industry` |
| `business_class` |
| `vision2030_theme` |
| `source_quality` |
| `source_note` |
| `last_reviewed` |
| `official_profile_url` |
| `source_type` |

## `datasets/companies_intelligence.csv` (259 rows)

التصنيف + طبقة التعرّض المحتمل للفعاليات الكبرى.

| column |
|---|
| `symbol` |
| `name_ar` |
| `name_en` |
| `market` |
| `sector` |
| `industry` |
| `business_class` |
| `vision2030_theme` |
| `source_quality` |
| `source_note` |
| `last_reviewed` |
| `official_profile_url` |
| `source_type` |
| `expo2030_exposure` |
| `worldcup2034_exposure` |
| `primary_event_driver` |
| `secondary_event_driver` |
| `exposure_strength` |
| `confidence` |
| `rationale` |
| `event_exposure_overall` |

## `datasets/companies_index_membership.csv` (259 rows)

عضوية مؤشرات السوق (بنية سوق محافظة).

| column |
|---|
| `symbol` |
| `name_ar` |
| `index_code` |
| `index_name` |
| `membership_status` |
| `effective_date` |
| `review_cycle` |
| `source_url` |
| `last_reviewed` |
| `confidence` |
| `notes` |

## `datasets/companies_seasonal_exposure.csv` (25 rows)

التعرّض الموسمي المحتمل (حج/رمضان).

| column |
|---|
| `symbol` |
| `name_ar` |
| `season` |
| `exposure_level` |
| `primary_driver` |
| `confidence` |
| `rationale` |
| `evidence_status` |
| `source_url` |
| `last_reviewed` |
| `notes` |

## `datasets/market_intelligence_matrix.csv` (259 rows)

المصفوفة الرئيسية: صف واحد لكل شركة يدمج كل الطبقات.

| column |
|---|
| `symbol` |
| `name_ar` |
| `name_en` |
| `sector` |
| `business_class` |
| `vision2030_theme` |
| `event_exposure_overall` |
| `primary_event_driver` |
| `event_confidence` |
| `seasonal_hajj_exposure` |
| `seasonal_ramadan_exposure` |
| `seasonal_primary_drivers` |
| `index_membership_summary` |
| `source_type` |
| `source_freshness_status` |
| `review_priority` |
| `classification_risk` |

