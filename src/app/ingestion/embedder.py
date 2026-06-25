"""Turn chunk text into embedding vectors using Gemini, with batching and retry."""

import time

from google import genai

from src.app.core.config import get_settings
from src.app.core.logging import get_logger

logger = get_logger(__name__)

BATCH_SIZE = 50          # how many texts to send per request
MAX_RETRIES = 5          # how many times to retry on rate-limit
RETRY_WAIT_SECONDS = 20  # how long to wait between retries


def embed_texts(texts: list[str]) -> list[list[float]]:
    settings = get_settings()
    client = genai.Client(
        vertexai=True,
        project=settings.gcp_project_id,
        location=settings.gcp_location,
    )

    logger.info("Embedding %d texts in batches of %d...", len(texts), BATCH_SIZE)

    all_vectors: list[list[float]] = []

    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]
        batch_num = start // BATCH_SIZE + 1

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = client.models.embed_content(
                    model=settings.gemini_embed_model,
                    contents=batch,
                )
                batch_vectors = [e.values for e in response.embeddings]
                all_vectors.extend(batch_vectors)
                logger.info("Batch %d done (%d vectors)", batch_num, len(batch_vectors))
                break
            except Exception as exc:
                if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                    logger.warning(
                        "Rate limit hit on batch %d, attempt %d. Waiting %ds...",
                        batch_num, attempt, RETRY_WAIT_SECONDS,
                    )
                    time.sleep(RETRY_WAIT_SECONDS)
                else:
                    raise
        else:
            raise RuntimeError(f"Batch {batch_num} failed after {MAX_RETRIES} retries")

    logger.info("Created %d vectors of dimension %d", len(all_vectors), len(all_vectors[0]))
    return all_vectors