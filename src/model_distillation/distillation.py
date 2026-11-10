"""Teacher eligibility and preference-data construction over external verification."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from verification_runtime import VerificationResult as _VerificationResult, text_sha256


@dataclass(frozen=True)
class Task:
    task_id: str
    domain: str
    prompt: str
    difficulty: float
    expected_answer: str | None = None


@dataclass(frozen=True)
class TeacherResponse:
    task_id: str
    teacher_id: str
    response: str
    license: str
    allowed_for_distillation: bool


@dataclass(frozen=True)
class PreferencePair:
    task_id: str
    chosen: str
    rejected: str
    source: str


def build_preference_pair(
    task: Task,
    accepted: TeacherResponse,
    rejected: TeacherResponse,
    accepted_result: _VerificationResult,
) -> PreferencePair:
    if not accepted_result.accepted:
        raise ValueError("accepted_result must be accepted before building a preference pair")
    reference_hash = text_sha256(task.expected_answer) if task.expected_answer is not None else None
    if (accepted_result.subject_id != task.task_id
            or accepted_result.candidate_sha256 != text_sha256(accepted.response)
            or accepted_result.reference_sha256 != reference_hash):
        raise ValueError("verification must belong to the chosen response bytes, task and reference")
    if not accepted.allowed_for_distillation or not rejected.allowed_for_distillation:
        raise ValueError("both responses must be eligible for distillation")
    if accepted.task_id != task.task_id or rejected.task_id != task.task_id:
        raise ValueError("responses must belong to the task")
    return PreferencePair(
        task_id=task.task_id,
        chosen=accepted.response,
        rejected=rejected.response,
        source=f"{accepted.teacher_id}_over_{rejected.teacher_id}",
    )


def task_from_record(record: dict[str, Any]) -> Task:
    return Task(
        task_id=str(record["task_id"]),
        domain=str(record["domain"]),
        prompt=str(record["prompt"]),
        difficulty=float(record.get("difficulty", 0.0)),
        expected_answer=record.get("expected_answer"),
    )
