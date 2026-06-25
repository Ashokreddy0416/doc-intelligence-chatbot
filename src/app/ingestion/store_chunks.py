"""Save chunks with their embeddings into the Supabase 'chunks' table."""

from src.app.core.database import get_supabase
from src.app.core.logging import get_logger
from src.app.ingestion.chunker import Chunk
from src.app.ingestion.embedder import embed_texts

logger = get_logger(__name__)


def store_chunks(document_id: int, chunks: list[Chunk]) -> int:
    supabase = get_supabase()

    texts = [chunk.text for chunk in chunks]
    vectors = embed_texts(texts)

    rows = [
        {
            "document_id": document_id,
            "chunk_index": chunk.index,
            "content": chunk.text,
            "embedding": vector,
        }
        for chunk, vector in zip(chunks, vectors)
    ]

    logger.info("Inserting %d chunks into database...", len(rows))
    supabase.table("chunks").insert(rows).execute()
    logger.info("Stored %d chunks for document_id=%d", len(rows), document_id)
    return len(rows)