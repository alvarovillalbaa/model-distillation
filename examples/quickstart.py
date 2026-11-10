from model_distillation import Task, TeacherResponse, verify_exact_match, build_preference_pair
task = Task("math-1", "math", "2+2?", 0.1, "4")
a = TeacherResponse("math-1", "fixture-a", "4", "MIT", True)
b = TeacherResponse("math-1", "fixture-b", "5", "MIT", True)
print(build_preference_pair(task, a, b, verify_exact_match(task, a)))
