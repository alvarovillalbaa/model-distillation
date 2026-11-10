"""A deterministic fixture demonstration; no teacher or model is called."""
import argparse
import json
from dataclasses import asdict

from . import Task, TeacherResponse, build_preference_pair
from verification_runtime import verify_exact_match


def demo_pair():
    task = Task("math-1", "math", "2+2?", 0.1, expected_answer="4")
    chosen = TeacherResponse(task.task_id, "fixture-a", "4", "MIT", True)
    rejected = TeacherResponse(task.task_id, "fixture-b", "5", "MIT", True)
    result = verify_exact_match(subject_id=task.task_id, candidate=chosen.response,
                                reference=task.expected_answer)
    return build_preference_pair(task, chosen, rejected, result)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("demo",))
    parser.parse_args(argv)
    print(json.dumps({"source": "authored_fixture", "pair": asdict(demo_pair())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
