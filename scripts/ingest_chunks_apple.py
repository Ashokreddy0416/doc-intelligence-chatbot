"""Full pipeline for Apple: parse -> chunk -> embed -> store."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.ingestion.parser import parse_document
from src.app.ingestion.chunker import chunk_text
from src.app.ingestion.store_chunks import store_chunks
from src.app.core.logging import get_logger

logger = get_logger(__name__)

APPLE_DOCUMENT_ID = 1  # Apple's id in the documents table


def main() -> None:
    logger.info("Parsing Apple...")
    parsed = parse_document("data/raw/apple_10k.pdf")

    logger.info("Chunking...")
    chunks = chunk_text(parsed.text)

    logger.info("Embedding and storing %d chunks...", len(chunks))
    count = store_chunks(APPLE_DOCUMENT_ID, chunks)

    logger.info("DONE: stored %d Apple chunks", count)


if __name__ == "__main__":
    main()