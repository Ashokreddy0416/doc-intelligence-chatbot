"""Search for the most relevant chunks given a user question."""

from dataclasses import dataclass

from src.app.core.database import get_supabase
from src.app.core.logging import get_logger
from src.app.ingestion.embedder import embed_texts

logger = get_logger(__name__)


@dataclass
class SearchResult:
    chunk_index: int
    content: str
    similarity: float


def search_chunks(question: str, document_id: int, top_k: int = 5) -> list[SearchResult]:
    logger.info("Searching for: %s", question)

    question_vector = embed_texts([question])[0]

    supabase = get_supabase()
    response = supabase.rpc(
        "match_chunks",
        {
            "query_embedding": question_vector,
            "match_count": top_k,
            "filter_document_id": document_id,
        },
    ).execute()

    results = [
        SearchResult(
            chunk_index=row["chunk_index"],
            content=row["content"],
            similarity=row["similarity"],
        )
        for row in response.data
    ]

    logger.info("Found %d relevant chunks", len(results))
    return results