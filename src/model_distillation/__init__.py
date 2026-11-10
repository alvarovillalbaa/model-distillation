"""Data construction primitives, independent of training and evaluation services."""
from .distillation import Task, TeacherResponse, VerificationResult, PreferencePair, verify_exact_match, build_preference_pair, task_from_record

__all__ = ["Task", "TeacherResponse", "VerificationResult", "PreferencePair", "verify_exact_match", "build_preference_pair", "task_from_record"]
