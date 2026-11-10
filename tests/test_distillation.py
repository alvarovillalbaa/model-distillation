import unittest
from model_distillation import Task, TeacherResponse, VerificationResult, verify_exact_match, build_preference_pair


class DistillationTests(unittest.TestCase):
    def setUp(self):
        self.task = Task("math-1", "math", "2+2?", 0.1, "4")
        self.chosen = TeacherResponse("math-1", "a", "4", "MIT", True)
        self.rejected = TeacherResponse("math-1", "b", "5", "MIT", True)

    def test_verification_and_pair(self):
        result = verify_exact_match(self.task, self.chosen)
        self.assertTrue(result.accepted)
        pair = build_preference_pair(self.task, self.chosen, self.rejected, result)
        self.assertEqual((pair.chosen, pair.rejected), ("4", "5"))

    def test_disallowed_output_fails_verification(self):
        response = TeacherResponse("math-1", "a", "4", "unknown", False)
        self.assertFalse(verify_exact_match(self.task, response).accepted)

    def test_missing_answer_and_mismatched_task_fail(self):
        task = Task("math-1", "math", "2+2?", 0.1)
        self.assertFalse(verify_exact_match(task, self.chosen).accepted)
        self.assertFalse(verify_exact_match(self.task, TeacherResponse("other", "a", "4", "MIT", True)).accepted)

    def test_pair_rejects_unbound_verification_and_ineligible_output(self):
        for result in (VerificationResult("math-1", "a", False, "exact_match", "failed"),
                       VerificationResult("other", "a", True, "exact_match", "wrong task"),
                       VerificationResult("math-1", "other", True, "exact_match", "wrong teacher")):
            with self.subTest(result=result), self.assertRaises(ValueError):
                build_preference_pair(self.task, self.chosen, self.rejected, result)
        bad = TeacherResponse("math-1", "b", "5", "unknown", False)
        with self.assertRaises(ValueError):
            build_preference_pair(self.task, self.chosen, bad, verify_exact_match(self.task, self.chosen))


if __name__ == "__main__":
    unittest.main()
