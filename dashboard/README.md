# Saudi Market Intelligence Dashboard

> This dashboard is for research and data organization only, not investment advice.
> هذه اللوحة لأغراض البحث وتنظيم البيانات فقط، وليست توصية استثمارية.

لوحة محلية للقراءة فقط تستعرض مصفوفة الذكاء السوقي من حزمة البيانات العامة.

## How to run

من جذر المستودع:

```bash
pip install -r requirements.txt   # يتضمن streamlit
python3 run.py                    # لتوليد/تحديث public/ إن لزم
streamlit run dashboard/app.py
```

يفتح المتصفح على `http://localhost:8501`.

## Data source

- `public/datasets/market_intelligence_matrix.csv` — الصفوف المعروضة.
- `public/manifest.json` — ملخص الحزمة (schema_version، source_anchor_date، عدد المجموعات).

اللوحة **للقراءة فقط** ولا تكتب أو تعدّل أي بيانات، ولا تتصل بأي API أو قاعدة بيانات.

## Limitations

- تعرض البيانات المولّدة الموجودة فقط؛ شغّل `python3 run.py` أولًا لتحديثها.
- التعرّض للفعاليات والموسمية ربط موضوعي (thematic linkage) لا تعاقدي.
- عضوية المؤشرات محافظة (`needs_verification`) بانتظار لقطة رسمية.
- ليست أداة تداول ولا نصيحة مالية.
