from __future__ import annotations

import argparse
from pathlib import Path

from multi_agent.agents import DeveloperAgent, PlannerAgent, ReviewerAgent
from multi_agent.config import Settings, load_settings
from multi_agent.llm import LLMClient, OllamaClient, OpenAICompatibleClient


def _make_client(settings: Settings) -> LLMClient:
    if settings.provider in {"lmstudio", "openai"}:
        if settings.provider == "openai" and not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when PROVIDER=openai.")
        return OpenAICompatibleClient(
            base_url=settings.openai_base_url,
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            timeout_seconds=settings.timeout_seconds,
        )

    if settings.provider == "ollama":
        return OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_seconds=settings.timeout_seconds,
        )

    raise ValueError("Unsupported PROVIDER. Use lmstudio, openai, or ollama.")


def _load_input(input_text: str | None, input_file: str | None) -> str:
    if input_text and input_text.strip():
        return input_text.strip()
    if input_file:
        return Path(input_file).read_text(encoding="utf-8").strip()
    raise ValueError("Provide --input or --input-file.")


def run_workflow(user_request: str, max_iterations: int = 2) -> None:
    settings = load_settings()
    llm = _make_client(settings)

    planner = PlannerAgent(llm)
    developer = DeveloperAgent(llm)
    reviewer = ReviewerAgent(llm)

    print("\n=== USER REQUEST ===")
    print(user_request)

    plan = planner.plan(user_request)
    print("\n=== PLANNER OUTPUT ===")
    print(plan.content)

    revision_requests = ""
    final_draft_content = ""
    final_review = None

    for i in range(1, max_iterations + 1):
        draft = developer.develop(
            user_request=user_request,
            plan=plan,
            revision_requests=revision_requests,
        )
        print(f"\n=== DEVELOPER DRAFT (iteration {i}) ===")
        print(draft.content)

        review = reviewer.review(user_request=user_request, plan=plan, draft=draft)
        print(f"\n=== REVIEWER FEEDBACK (iteration {i}) ===")
        print(review.raw_content)

        final_draft_content = draft.content
        final_review = review

        if review.approved:
            break
        revision_requests = review.revision_requests or "Improve quality and completeness."

    print("\n=== FINAL OUTPUT ===")
    if final_review and not final_review.approved:
        print("Reviewer did not approve within max iterations. Returning best draft.")
    print(final_draft_content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Multi-Agent workflow.")
    parser.add_argument("--input", type=str, help="Direct user request text.")
    parser.add_argument("--input-file", type=str, help="Path to a text file with user request.")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=2,
        help="Max developer-reviewer loops before returning best draft.",
    )
    args = parser.parse_args()

    request = _load_input(args.input, args.input_file)
    run_workflow(user_request=request, max_iterations=max(1, args.max_iterations))


if __name__ == "__main__":
    main()

