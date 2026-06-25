"""Run the evaluation set and print baseline scores."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.retrieval.search import search_chunks
from src.app.generation.answer import generate_answer
from src.app.evaluation.judge import judge_answer
from src.app.core.logging import get_logger

logger = get_logger(__name__)

APPLE_DOCUMENT_ID = 1


def main() -> None:
    questions = json.loads(Path("data/eval/apple_questions.json").read_text())

    total_faith = 0
    total_rel = 0

    for i, item in enumerate(questions, 1):
        question = item["question"]
        logger.info("[%d/%d] %s", i, len(questions), question)

        results = search_chunks(question, APPLE_DOCUMENT_ID, top_k=5)
        context = "\n\n".join(r.content for r in results)
        answer = generate_answer(question, results)

        score = judge_answer(question, context, answer.text)
        total_faith += score.faithfulness
        total_rel += score.relevance

        print(f"\nQ{i}: {question}")
        print(f"   Faithfulness: {score.faithfulness}/5 | Relevance: {score.relevance}/5")

    n = len(questions)
    print(f"\n{'='*50}")
    print(f"BASELINE SCORES (over {n} questions)")
    print(f"  Avg Faithfulness: {total_faith/n:.2f}/5")
    print(f"  Avg Relevance:    {total_rel/n:.2f}/5")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()