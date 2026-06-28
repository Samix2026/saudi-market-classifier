from pathlib import Path
import pandas as pd

current_path = Path("data/reference/companies.csv")
incoming_path = Path("data/raw/main_market_companies.csv")

if not incoming_path.exists():
    print(f"Missing file: {incoming_path}")
    print("Create it with columns: symbol,name_ar,name_en,market,sector")
    raise SystemExit(1)

current = pd.read_csv(current_path)
incoming = pd.read_csv(incoming_path)

required = {"symbol", "name_ar", "name_en", "market", "sector"}
missing_columns = required - set(incoming.columns)

if missing_columns:
    print("Missing columns in incoming file:")
    for column in sorted(missing_columns):
        print(f"- {column}")
    raise SystemExit(1)

missing = incoming[~incoming["symbol"].isin(current["symbol"])].copy()
missing = missing.sort_values("symbol")

print(f"Current companies: {len(current)}")
print(f"Incoming companies: {len(incoming)}")
print(f"Missing companies: {len(missing)}")

if not missing.empty:
    print()
    print(missing.to_csv(index=False))
