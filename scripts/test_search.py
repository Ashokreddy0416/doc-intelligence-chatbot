"""Ask a question and see which Apple chunks match."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.retrieval.search import search_chunks
from src.app.core.logging import get_logger

logger = get_logger(__name__)

APPLE_DOCUMENT_ID = 1


def main() -> None:
    question = "What are Apple's main business risks?"
    results = search_chunks(question, APPLE_DOCUMENT_ID, top_k=5)

    print(f"\nQuestion: {question}\n")
    for i, r in enumerate(results, 1):
        print(f"--- Result {i} (similarity: {r.similarity:.3f}) ---")
        print(r.content[:300])
        print()


if __name__ == "__main__":
    main()