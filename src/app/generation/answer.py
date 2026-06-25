"""Generate a grounded, cited answer from retrieved chunks using Gemini."""

from dataclasses import dataclass

from google import genai

from src.app.core.config import get_settings
from src.app.core.logging import get_logger
from src.app.retrieval.search import SearchResult

logger = get_logger(__name__)


@dataclass
class Answer:
    text: str
    sources_used: list[int]


PROMPT_TEMPLATE = """You are a helpful assistant answering questions about a company's 10-K filing.

Use ONLY the excerpts below to answer the question. Each excerpt is numbered.
If the answer is not in the excerpts, say "I cannot find this in the document."
When you use information from an excerpt, cite it like [1] or [2].

EXCERPTS:
{excerpts}

QUESTION: {question}

ANSWER (with citations):"""


def generate_answer(question: str, results: list[SearchResult]) -> Answer:
    settings = get_settings()
    client = genai.Client(
        vertexai=True,
        project=settings.gcp_project_id,
        location=settings.gcp_location,
    )

    excerpts = "\n\n".join(
        f"[{i}] {r.content}" for i, r in enumerate(results, 1)
    )

    prompt = PROMPT_TEMPLATE.format(excerpts=excerpts, question=question)

    logger.info("Asking Gemini to answer with %d excerpts...", len(results))
    response = client.models.generate_content(
        model=settings.gemini_llm_model,
        contents=prompt,
    )

    answer_text = response.text
    sources_used = [i for i in range(1, len(results) + 1) if f"[{i}]" in answer_text]

    logger.info("Answer generated, cited sources: %s", sources_used)
    return Answer(text=answer_text, sources_used=sources_used)