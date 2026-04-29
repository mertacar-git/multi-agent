from __future__ import annotations

from pathlib import Path

from multi_agent.agents.types import ReviewFeedback, SolutionDraft, TaskPlan
from multi_agent.llm.base import LLMClient


def _load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "reviewer.md"
    return prompt_path.read_text(encoding="utf-8")


def _extract_section(raw: str, header: str, next_headers: list[str]) -> str:
    start = raw.find(header)
    if start == -1:
        return ""
    start += len(header)
    tail = raw[start:]
    end_positions = [pos for h in next_headers if (pos := tail.find(h)) != -1]
    end = min(end_positions) if end_positions else len(tail)
    return tail[:end].strip()


def _parse_review(raw: str) -> ReviewFeedback:
    lowered = raw.lower()
    approved = "approved: yes" in lowered
    rationale = _extract_section(raw, "RATIONALE:", ["REVISION_REQUESTS:"])
    revision_requests = _extract_section(raw, "REVISION_REQUESTS:", [])
    return ReviewFeedback(
        approved=approved,
        rationale=rationale,
        revision_requests=revision_requests,
        raw_content=raw,
    )


class ReviewerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm
        self.system_prompt = _load_prompt()

    def review(self, user_request: str, plan: TaskPlan, draft: SolutionDraft) -> ReviewFeedback:
        user_prompt = (
            f"User request:\n{user_request}\n\n"
            f"Planner output:\n{plan.content}\n\n"
            f"Developer draft:\n{draft.content}\n\n"
            "Review this draft following the required strict format."
        )
        raw = self.llm.generate(self.system_prompt, user_prompt)
        return _parse_review(raw)

