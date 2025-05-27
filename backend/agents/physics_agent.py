from crewai import Agent
from transformers import pipeline
from tools.physic_tools.kinematics_calculator import KinematicsCalculator
from tools.physic_tools.energy_calculator import EnergyCalculator
from tools.physic_tools.circuit_calculator import CircuitCalculator
from db.database import get_query_history
from rag import setup_rag, retrieve_context
import os
from dotenv import load_dotenv
import re
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
vector_store = setup_rag()

class PhysicsAgent:
    def __init__(self):
        self.kinematics_calculator = KinematicsCalculator()
        self.energy_calculator = EnergyCalculator()
        self.circuit_calculator = CircuitCalculator()

    def solve_physics_query(self, query: str, user_id: str = "default") -> dict:
        """Route physics query to appropriate tool or model"""
        query_lower = query.lower().replace(" ", "")
        history = get_query_history(user_id, limit=3)
        context = "Recent queries: " + "; ".join([f"{h['query']} ({h['subject']})" for h in history])
        rag_context = retrieve_context(query, vector_store)

        # Check for kinematics queries
        if any(keyword in query_lower for keyword in ["velocity", "acceleration", "displacement"]):
            kinematics_result = self.kinematics_calculator.calculate_kinematics(query)
            if kinematics_result["success"]:
                return {
                    "agent": "physics",
                    "tool_used": "kinematics_calculator",
                    "query": query,
                    "answer": f"Result: {kinematics_result['result']}\nSteps:\n" + "\n".join(kinematics_result["steps"]),
                    "details": kinematics_result,
                    "confidence": 0.90
                }

        # Check for energy queries
        if any(keyword in query_lower for keyword in ["kinetic", "potential", "energy"]):
            energy_result = self.energy_calculator.calculate_energy(query)
            if energy_result["success"]:
                return {
                    "agent": "physics",
                    "tool_used": "energy_calculator",
                    "query": query,
                    "answer": f"Result: {energy_result['result']} J\nSteps:\n" + "\n".join(energy_result["steps"]),
                    "details": energy_result,
                    "confidence": 0.90
                }

        # Check for circuit queries
        if any(keyword in query_lower for keyword in ["current", "voltage", "resistance"]):
            circuit_result = self.circuit_calculator.calculate_circuit(query)
            if circuit_result["success"]:
                return {
                    "agent": "physics",
                    "tool_used": "circuit_calculator",
                    "query": query,
                    "answer": f"Result: {circuit_result['result']} A\nSteps:\n" + "\n".join(circuit_result["steps"]),
                    "details": circuit_result,
                    "confidence": 0.90
                }

        # Fallback to language model
        return self._use_language_model(query, context, rag_context)

    def _use_language_model(self, query: str, context: str, rag_context: str) -> dict:
        """Use language model for physics explanations"""
        prompt = (
            f"You are a physics expert. Given the context: {context}\n"
            f"Relevant knowledge: {rag_context}\n"
            f"Query: {query}\n"
            f"For calculations, solve step-by-step and provide the final answer. "
            f"For theoretical questions, explain clearly with examples if applicable. "
            f"Keep the response concise and accurate."
        )
        response = physics_pipeline(prompt, max_length=300, num_return_sequences=1, temperature=0.7)[0]["generated_text"]
        return {
            "agent": "physics",
            "tool_used": "language_model",
            "query": query,
            "answer": response,
            "confidence": 0.75
        }

physics_agent = Agent(
    role="Physics Agent",
    goal="Answer physics-related questions and perform calculations",
    backstory="An expert in mechanics, electromagnetism, and thermodynamics",
    llm=lambda x, **kwargs: PhysicsAgent().solve_physics_query(x, kwargs.get("user_id", "default"))["answer"],
    tools=[
        KinematicsCalculator().calculate_kinematics,
        EnergyCalculator().calculate_energy,
        CircuitCalculator().calculate_circuit
    ],
    verbose=True
)