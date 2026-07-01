from src.saudi_market_classifier.validate import main as validate_main
from src.saudi_market_classifier.classify import main as classify_main
from src.saudi_market_classifier.report import main as report_main
from src.saudi_market_classifier.coverage import main as coverage_main
from src.saudi_market_classifier.intelligence import main as intelligence_main
from src.saudi_market_classifier.event_report import main as event_report_main
from src.saudi_market_classifier.review_queue import main as review_queue_main
from src.saudi_market_classifier.source_freshness import main as source_freshness_main
from src.saudi_market_classifier.index_membership import main as index_membership_main


def main():
    validate_main()
    classify_main()
    report_main()
    coverage_main()
    intelligence_main()
    event_report_main()
    review_queue_main()
    source_freshness_main()
    index_membership_main()


if __name__ == "__main__":
    main()
