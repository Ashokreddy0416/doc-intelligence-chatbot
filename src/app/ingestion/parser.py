"""Parse a document (PDF/HTML) into structured text, tables, and images using Docling."""

import os

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from dataclasses import dataclass, field
from pathlib import Path

from docling.document_converter import DocumentConverter

from src.app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ParsedDocument:
    source_path: str
    text: str
    num_tables: int
    num_images: int
    tables_markdown: list[str] = field(default_factory=list)


def parse_document(file_path: str | Path) -> ParsedDocument:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    logger.info("Parsing document: %s", path.name)

    converter = DocumentConverter()
    result = converter.convert(str(path))
    doc = result.document

    full_text = doc.export_to_markdown()

    tables_markdown = [table.export_to_markdown() for table in doc.tables]

    num_images = len(doc.pictures)

    logger.info(
        "Parsed %s -> %d chars text, %d tables, %d images",
        path.name,
        len(full_text),
        len(tables_markdown),
        num_images,
    )

    return ParsedDocument(
        source_path=str(path),
        text=full_text,
        num_tables=len(tables_markdown),
        num_images=num_images,
        tables_markdown=tables_markdown,
    )