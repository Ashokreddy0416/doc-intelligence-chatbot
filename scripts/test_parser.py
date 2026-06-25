"""Parse the Apple 10-K and show what Docling extracted."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.ingestion.parser import parse_document
from src.app.core.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    result = parse_document("data/raw/apple_10k.pdf")

    logger.info("=== RESULT ===")
    logger.info("Text length: %d characters", len(result.text))
    logger.info("Tables found: %d", result.num_tables)
    logger.info("Images found: %d", result.num_images)

    print("\n--- First 500 characters of text ---")
    print(result.text[:500])

    if result.tables_markdown:
        print("\n--- First table ---")
        print(result.tables_markdown[0][:500])


if __name__ == "__main__":
    main()