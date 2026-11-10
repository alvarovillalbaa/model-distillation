from dataclasses import replace
import unittest

from model_distillation import Task, TeacherResponse, build_preference_pair
from verification_runtime import verify_exact_match


class DistillationTests(unittest.TestCase):
    def setUp(self):
        self.task = Task("math-1", "math", "2+2?", 0.1, "4")
        self.chosen = TeacherResponse("math-1", "a", "4", "MIT", True)
        self.rejected = TeacherResponse("math-1", "b", "5", "MIT", True)
        self.result = verify_exact_match(subject_id=self.task.task_id,
                                         candidate=self.chosen.response,
                                         reference=self.task.expected_answer)

    def test_verified_pair(self):
        pair = build_preference_pair(self.task, self.chosen, self.rejected, self.result)
        self.assertEqual((pair.chosen, pair.rejected), ("4", "5"))

    def test_correct_but_ineligible_responses_still_fail_pair_policy(self):
        self.assertTrue(self.result.accepted)
        for chosen, rejected in ((replace(self.chosen, allowed_for_distillation=False), self.rejected),
                                 (self.chosen, replace(self.rejected, allowed_for_distillation=False))):
            with self.assertRaises(ValueError):
                build_preference_pair(self.task, chosen, rejected, self.result)

    def test_changed_response_reference_or_subject_rejects_stale_verification(self):
        for task, chosen, rejected, result in (
            (self.task, replace(self.chosen, response="5"), self.rejected, self.result),
            (replace(self.task, expected_answer="5"), self.chosen, self.rejected, self.result),
            (self.task, self.chosen, self.rejected, replace(self.result, subject_id="other")),
            (self.task, self.chosen, replace(self.rejected, task_id="other"), self.result),
            (self.task, self.chosen, self.rejected, replace(self.result, accepted=False)),
        ):
            with self.subTest(task=task, chosen=chosen, result=result), self.assertRaises(ValueError):
                build_preference_pair(task, chosen, rejected, result)

    def test_verification_has_one_external_owner(self):
        import model_distillation
        self.assertFalse(hasattr(model_distillation, "VerificationResult"))
        self.assertFalse(hasattr(model_distillation, "verify_exact_match"))


if __name__ == "__main__":
    unittest.main()
