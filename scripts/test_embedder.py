"""Embed a few sample texts and show the vectors."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.ingestion.embedder import embed_texts
from src.app.core.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    samples = [
        "Apple faces supply chain risks.",
        "Dangers to Apple's manufacturing operations.",
        "Apple's quarterly revenue grew strongly.",
    ]

    vectors = embed_texts(samples)

    logger.info("Vector dimension: %d", len(vectors[0]))
    print("\nFirst 5 numbers of each vector:")
    for sample, vec in zip(samples, vectors):
        print(f"{sample[:40]:42} -> {[round(x, 3) for x in vec[:5]]}")


if __name__ == "__main__":
    main()