from src.saudi_market_classifier.validate import main as validate_main
from src.saudi_market_classifier.classify import main as classify_main
from src.saudi_market_classifier.report import main as report_main


def main():
    validate_main()
    classify_main()
    report_main()


if __name__ == "__main__":
    main()
