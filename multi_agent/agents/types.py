from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TaskPlan:
    content: str


@dataclass
class SolutionDraft:
    content: str


@dataclass
class ReviewFeedback:
    approved: bool
    rationale: str
    revision_requests: str
    raw_content: str

