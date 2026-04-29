from __future__ import annotations

from pathlib import Path

from multi_agent.agents.types import SolutionDraft, TaskPlan
from multi_agent.llm.base import LLMClient


def _load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "developer.md"
    return prompt_path.read_text(encoding="utf-8")


class DeveloperAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm
        self.system_prompt = _load_prompt()

    def develop(
        self,
        user_request: str,
        plan: TaskPlan,
        revision_requests: str = "",
    ) -> SolutionDraft:
        revision_block = (
            f"\nReviewer revision requests:\n{revision_requests}\n"
            if revision_requests.strip()
            else ""
        )
        user_prompt = (
            f"User request:\n{user_request}\n\n"
            f"Planner output:\n{plan.content}\n"
            f"{revision_block}\n"
            "Produce an improved implementation draft."
        )
        content = self.llm.generate(self.system_prompt, user_prompt)
        return SolutionDraft(content=content)

