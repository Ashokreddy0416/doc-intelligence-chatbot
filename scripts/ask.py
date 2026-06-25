"""Ask a question about Apple's 10-K and get a cited answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.retrieval.search import search_chunks
from src.app.generation.answer import generate_answer
from src.app.core.logging import get_logger

logger = get_logger(__name__)

APPLE_DOCUMENT_ID = 1


def main() -> None:
    question = "What are Apple's main business risks?"

    results = search_chunks(question, APPLE_DOCUMENT_ID, top_k=5)
    answer = generate_answer(question, results)

    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}\n")
    print(answer.text)
    print(f"\n{'='*60}")
    print(f"Sources used: {answer.sources_used}")


if __name__ == "__main__":
    main()