"""Call Gemini from Python via Vertex AI and print the answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from google import genai

from src.app.core.config import get_settings
from src.app.core.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    settings = get_settings()

    client = genai.Client(
        vertexai=True,
        project=settings.gcp_project_id,
        location=settings.gcp_location,
    )

    logger.info("Sending request to Gemini...")
    response = client.models.generate_content(
        model=settings.gemini_llm_model,
        contents="Say hello in one short sentence.",
    )

    logger.info("Gemini replied: %s", response.text)


if __name__ == "__main__":
    main()