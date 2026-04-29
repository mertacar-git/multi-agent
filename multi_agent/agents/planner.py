from __future__ import annotations

from pathlib import Path

from multi_agent.agents.types import TaskPlan
from multi_agent.llm.base import LLMClient


def _load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "planner.md"
    return prompt_path.read_text(encoding="utf-8")


class PlannerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm
        self.system_prompt = _load_prompt()

    def plan(self, user_request: str) -> TaskPlan:
        user_prompt = f"User request:\n{user_request}\n\nCreate a high quality actionable plan."
        content = self.llm.generate(self.system_prompt, user_prompt)
        return TaskPlan(content=content)

