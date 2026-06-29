import sys
from pathlib import Path

import pandas as pd


EXPOSURES_CSV = "data/reference/mega_event_exposures.csv"

ALLOWED_EXPOSURE = {"high", "medium", "low", "none"}
ALLOWED_DRIVER = {
    "venue_construction", "urban_infrastructure", "transport_mobility",
    "hospitality_tourism", "food_catering", "digital_connectivity",
    "event_services", "media_advertising", "facilities_management",
    "security_operations", "none",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def _validate_mega_event_exposures(companies):
    """تحقق من ملف التعرّض للفعاليات: وجوده، الرموز، القيم المسموحة."""
    errors = []
    path = Path(EXPOSURES_CSV)
    if not path.exists():
        errors.append(f"Missing mega event exposures file: {EXPOSURES_CSV}")
        return errors

    exposures = pd.read_csv(path, dtype={"symbol": str})
    company_symbols = companies["symbol"].astype(str)

    unknown = exposures[~exposures["symbol"].isin(company_symbols)]
    if not unknown.empty:
        errors.append("Mega event exposure symbols not in companies.csv:")
        for _, row in unknown.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']}")

    dupes = exposures[exposures["symbol"].duplicated(keep=False)]
    if not dupes.empty:
        errors.append("Duplicate symbols in mega event exposures:")
        for sym in sorted(dupes["symbol"].unique()):
            errors.append(f"- {sym}")

    checks = [
        (["expo2030_exposure", "worldcup2034_exposure", "exposure_strength"], ALLOWED_EXPOSURE),
        (["primary_event_driver", "secondary_event_driver"], ALLOWED_DRIVER),
        (["confidence"], ALLOWED_CONFIDENCE),
    ]
    for cols, allowed in checks:
        for col in cols:
            bad = exposures[~exposures[col].isin(allowed)]
            for _, row in bad.iterrows():
                errors.append(
                    f"Invalid {col}='{row[col]}' for symbol {row['symbol']}"
                )

    return errors


def main():
    companies = pd.read_csv("data/reference/companies.csv")
    classes = pd.read_csv("data/reference/business_classes.csv")
    themes = pd.read_csv("data/reference/vision2030_themes.csv")
    source_quality = pd.read_csv("data/reference/source_quality.csv")
    official_sources = pd.read_csv("data/reference/official_sources.csv")

    errors = []

    missing_classes = companies[~companies["sector"].isin(classes["sector"])]
    if not missing_classes.empty:
        errors.append("Missing business_class mapping for sectors:")
        for sector in sorted(missing_classes["sector"].unique()):
            errors.append(f"- {sector}")

    missing_themes = companies[~companies["symbol"].isin(themes["symbol"])]
    if not missing_themes.empty:
        errors.append("Missing Vision 2030 theme mapping for companies:")
        for _, row in missing_themes.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    missing_source_quality = companies[~companies["symbol"].isin(source_quality["symbol"])]
    if not missing_source_quality.empty:
        errors.append("Missing source quality mapping for companies:")
        for _, row in missing_source_quality.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    missing_official_sources = companies[~companies["symbol"].isin(official_sources["symbol"])]
    if not missing_official_sources.empty:
        errors.append("Missing official source mapping for companies:")
        for _, row in missing_official_sources.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    duplicate_symbols = companies[companies["symbol"].duplicated(keep=False)]
    if not duplicate_symbols.empty:
        errors.append("Duplicate symbols found:")
        for _, row in duplicate_symbols.sort_values("symbol").iterrows():
            errors.append(f"- {row['symbol']} — {row['name_ar']}")

    errors.extend(_validate_mega_event_exposures(companies))

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
