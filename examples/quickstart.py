from model_distillation import Task, TeacherResponse, build_preference_pair
from verification_runtime import verify_exact_match

task = Task("math-1", "math", "2+2?", 0.1, "4")
a = TeacherResponse("math-1", "fixture-a", "4", "MIT", True)
b = TeacherResponse("math-1", "fixture-b", "5", "MIT", True)
result = verify_exact_match(subject_id=task.task_id, candidate=a.response, reference=task.expected_answer)
print(build_preference_pair(task, a, b, result))
