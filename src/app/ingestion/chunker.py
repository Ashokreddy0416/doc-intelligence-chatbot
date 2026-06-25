"""Split a document's text into overlapping chunks for searching."""

from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.app.core.logging import get_logger

logger = get_logger(__name__)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


@dataclass
class Chunk:
    index: int
    text: str
    char_count: int


def chunk_text(text: str) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    pieces = splitter.split_text(text)

    chunks = [
        Chunk(index=i, text=piece, char_count=len(piece))
        for i, piece in enumerate(pieces)
    ]

    logger.info("Split text into %d chunks", len(chunks))
    return chunks