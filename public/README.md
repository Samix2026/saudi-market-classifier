# Saudi Market Classifier — Public Data Package

> This dataset is provided for research, market-mapping and data-quality purposes only. It is NOT investment advice and contains no buy/sell recommendations, guaranteed-benefit, contract, or revenue-impact claims.

> هذه البيانات لأغراض البحث ورسم خريطة السوق وجودة البيانات فقط. ليست توصية استثمارية ولا تتضمن توصيات شراء/بيع أو ادعاء استفادة أو عقود أو أثر إيرادي.

- Schema version: `1.0`
- source_anchor_date (newest last_reviewed): `2026-06-28`
- Datasets: 5 (see `manifest.json`)

## Contents

| file | rows | description |
|---|---:|---|
| `datasets/companies_classified.csv` | 259 | التصنيف الأساسي: قطاع، تصنيف نشاط، ثيم رؤية 2030، جودة المصدر. |
| `datasets/companies_intelligence.csv` | 259 | التصنيف + طبقة التعرّض المحتمل للفعاليات الكبرى. |
| `datasets/companies_index_membership.csv` | 259 | عضوية مؤشرات السوق (بنية سوق محافظة). |
| `datasets/companies_seasonal_exposure.csv` | 25 | التعرّض الموسمي المحتمل (حج/رمضان). |
| `datasets/market_intelligence_matrix.csv` | 259 | المصفوفة الرئيسية: صف واحد لكل شركة يدمج كل الطبقات. |

See `manifest.json` (machine-readable) and `DATA_DICTIONARY.md` (columns).

