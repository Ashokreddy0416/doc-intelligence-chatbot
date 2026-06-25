"""Use Gemini as a judge to score answer faithfulness and relevance."""

from dataclasses import dataclass

from google import genai

from src.app.core.config import get_settings
from src.app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Score:
    faithfulness: int
    relevance: int


JUDGE_PROMPT = """You are evaluating a question-answering system.

QUESTION: {question}

CONTEXT GIVEN TO THE SYSTEM:
{context}

SYSTEM'S ANSWER:
{answer}

Score the answer on two criteria, each from 1 (worst) to 5 (best):
1. FAITHFULNESS: Is the answer supported by the context? (5 = fully grounded, 1 = made up)
2. RELEVANCE: Does the answer address the question? (5 = directly, 1 = off-topic)

Respond ONLY in this exact format:
FAITHFULNESS: <number>
RELEVANCE: <number>"""


def judge_answer(question: str, context: str, answer: str) -> Score:
    settings = get_settings()
    client = genai.Client(
        vertexai=True,
        project=settings.gcp_project_id,
        location=settings.gcp_location,
    )

    prompt = JUDGE_PROMPT.format(question=question, context=context, answer=answer)
    response = client.models.generate_content(
        model=settings.gemini_llm_model,
        contents=prompt,
    )

    text = response.text
    faithfulness = _extract_score(text, "FAITHFULNESS")
    relevance = _extract_score(text, "RELEVANCE")
    return Score(faithfulness=faithfulness, relevance=relevance)


def _extract_score(text: str, label: str) -> int:
    for line in text.splitlines():
        if label in line:
            digits = "".join(c for c in line if c.isdigit())
            if digits:
                return int(digits[0])
    return 0