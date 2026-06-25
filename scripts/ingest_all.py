"""Parse and save all three 10-K documents into Supabase."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.ingestion.parser import parse_document
from src.app.ingestion.storage import save_document
from src.app.core.logging import get_logger

logger = get_logger(__name__)

DOCUMENTS = [
    ("data/raw/apple_10k.pdf", "Apple"),
    ("data/raw/microsoft_10k.pdf", "Microsoft"),
    ("data/raw/nvidia_10k.pdf", "NVIDIA"),
]


def main() -> None:
    for file_path, company in DOCUMENTS:
        logger.info("=== Processing %s ===", company)
        parsed = parse_document(file_path)
        doc_id = save_document(parsed, company)
        logger.info("Done: %s -> database id %d", company, doc_id)


if __name__ == "__main__":
    main()