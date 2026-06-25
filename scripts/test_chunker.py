"""Parse Apple, chunk it, and show what the chunks look like."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.ingestion.parser import parse_document
from src.app.ingestion.chunker import chunk_text
from src.app.core.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    parsed = parse_document("data/raw/apple_10k.pdf")
    chunks = chunk_text(parsed.text)

    logger.info("Total chunks: %d", len(chunks))

    print("\n--- Chunk 0 ---")
    print(chunks[0].text)
    print("\n--- Chunk 1 ---")
    print(chunks[1].text)


if __name__ == "__main__":
    main()