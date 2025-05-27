import unittest
from agents.physics_agent import PhysicsAgent

class TestPhysicsAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PhysicsAgent()

    def test_kinematics(self):
        result = self.agent.solve_physics_query("Find final velocity with initial velocity 0 m/s, acceleration 2 m/s², time 5 s")
        self.assertTrue(result["details"]["success"])
        self.assertIn("Result: 10.0", result["answer"])
        self.assertEqual(result["tool_used"], "kinematics_calculator")

    def test_kinetic_energy(self):
        result = self.agent.solve_physics_query("Kinetic energy of mass 2 kg with velocity 5 m/s")
        self.assertTrue(result["details"]["success"])
        self.assertIn("Result: 25.0 J", result["answer"])
        self.assertEqual(result["tool_used"], "energy_calculator")

    def test_circuit_current(self):
        result = self.agent.solve_physics_query("Current in resistance 10 ohm with voltage 5 V")
        self.assertTrue(result["details"]["success"])
        self.assertIn("Result: 0.5 A", result["answer"])
        self.assertEqual(result["tool_used"], "circuit_calculator")

    def test_theoretical(self):
        result = self.agent.solve_physics_query("What is Newton’s second law?")
        self.assertEqual(result["tool_used"], "language_model")
        self.assertIn("newton", result["answer"].lower())

if __name__ == "__main__":
    unittest.main()