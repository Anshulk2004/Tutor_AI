import unittest
from agents.math_agent import MathAgent

class TestMathAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MathAgent()

    def test_arithmetic(self):
        result = self.agent.solve_math_query("15 + 23")
        self.assertTrue(result["success"])
        self.assertEqual(result["answer"], "Result: 38")
        self.assertEqual(result["tool_used"], "calculator")

    def test_linear_equation(self):
        result = self.agent.solve_math_query("2x + 4 = 10")
        self.assertTrue(result["success"])
        self.assertIn("x = 3", result["answer"])
        self.assertEqual(result["tool_used"], "equation_solver")

    def test_quadratic_equation(self):
        result = self.agent.solve_math_query("x^2 + 5x + 6 = 0")
        self.assertTrue(result["success"])
        self.assertIn("x = -2, x = -3", result["answer"])
        self.assertEqual(result["tool_used"], "equation_solver")

    def test_statistics(self):
        result = self.agent.solve_math_query("Find mean of 1,2,3,4,5")
        self.assertTrue(result["success"])
        self.assertIn("Mean: 3", result["answer"])
        self.assertEqual(result["tool_used"], "statistics_calculator")

    def test_geometry(self):
        result = self.agent.solve_math_query("Area of circle with radius 5")
        self.assertTrue(result["success"])
        self.assertIn("Area of circle: 78.53981633974483", result["answer"])
        self.assertEqual(result["tool_used"], "geometry_calculator")

    def test_theoretical(self):
        result = self.agent.solve_math_query("What is the quadratic formula?")
        self.assertEqual(result["tool_used"], "language_model")
        self.assertIn("quadratic formula", result["answer"].lower())

if __name__ == "__main__":
    unittest.main()