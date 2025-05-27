import unittest
from agents.chemistry_agent import ChemistryAgent

class TestChemistryAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ChemistryAgent()

    def test_balance_equation(self):
        result = self.agent.solve_chemistry_query("C6H12O6 + O2 -> CO2 + H2O")
        self.assertTrue(result["details"]["success"])
        self.assertEqual(result["answer"], "Balanced equation: C6H12O6 + 6O2 -> 6CO2 + 6H2O")
        self.assertEqual(result["tool_used"], "equation_balancer")

    def test_molar_mass(self):
        result = self.agent.solve_chemistry_query("What is the molar mass of H2SO4?")
        self.assertTrue(result["details"]["success"])
        self.assertIn("Molar mass of H2SO4: 98.078 g/mol", result["answer"])
        self.assertEqual(result["tool_used"], "molar_mass_calculator")

    def test_ph_calculation(self):
        result = self.agent.solve_chemistry_query("pH of HCl 0.1 M")
        self.assertTrue(result["details"]["success"])
        self.assertIn("pH of HCl (0.1 M): 1.0", result["answer"])
        self.assertEqual(result["tool_used"], "ph_calculator")

    def test_theoretical(self):
        result = self.agent.solve_chemistry_query("What is a covalent bond?")
        self.assertEqual(result["tool_used"], "language_model")
        self.assertIn("covalent bond", result["answer"].lower())

if __name__ == "__main__":
    unittest.main()