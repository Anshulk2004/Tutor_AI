import unittest
from agents.evaluation_agent import EvaluationAgent

class TestEvaluationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EvaluationAgent()

    def test_correct_answer(self):
        result = self.agent.evaluate_answer(
            query="What is 2 + 2?",
            student_answer="4",
            correct_answer="4",
            user_id="test_user"
        )
        self.assertTrue(result["success"])
        self.assertTrue(result["is_correct"])
        self.assertIn("Great job", result["feedback"])

    def test_incorrect_answer(self):
        result = self.agent.evaluate_answer(
            query="What is 2 + 2?",
            student_answer="5",
            correct_answer="4",
            user_id="test_user"
        )
        self.assertTrue(result["success"])
        self.assertFalse(result["is_correct"])
        self.assertIn("incorrect", result["feedback"])

    def test_text_answer(self):
        result = self.agent.evaluate_answer(
            query="What is a covalent bond?",
            student_answer="A bond where electrons are shared",
            correct_answer="A bond where electrons are shared between atoms",
            user_id="test_user"
        )
        self.assertTrue(result["success"])
        self.assertTrue(result["is_correct"])
        self.assertIn("Great job", result["feedback"])

if __name__ == "__main__":
    unittest.main()