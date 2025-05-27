from crewai import Agent
from transformers import pipeline
from tools.chemistry_tools.chemical_equation_balancer import ChemicalEquationBalancer
from tools.chemistry_tools.molar_mass_calculator import MolarMassCalculator
from tools.chemistry_tools.ph_calculator import pHCalculator
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

class ChemistryAgent:
    def __init__(self):
        self.equation_balancer = ChemicalEquationBalancer()
        self.molar_mass_calculator = MolarMassCalculator()
        self.ph_calculator = pHCalculator()

    def solve_chemistry_query(self, query: str, user_id: str = "default") -> dict:
        """Route chemistry query to appropriate tool or model"""
        query_lower = query.lower().replace(" ", "")
        history = get_query_history(user_id, limit=3)
        context = "Recent queries: " + "; ".join([f"{h['query']} ({h['subject']})" for h in history])
        rag_context = retrieve_context(query, vector_store)

        # Check for equation balancing
        if "->" in query_lower or "balance" in query_lower:
            balance_result = self.equation_balancer.balance_equation(query)
            if balance_result["success"]:
                return {
                    "agent": "chemistry",
                    "tool_used": "equation_balancer",
                    "query": query,
                    "answer": f"Balanced equation: {balance_result['balanced_equation']}",
                    "details": balance_result,
                    "confidence": 0.90
                }

        # Check for molar mass calculations
        if "molar mass" in query_lower:
            compound = re.search(r"of\s+([A-Za-z0-9]+)", query_lower)
            if compound:
                compound = compound.group(1)
                mass_result = self.molar_mass_calculator.calculate_molar_mass(compound)
                if mass_result["success"]:
                    return {
                        "agent": "chemistry",
                        "tool_used": "molar_mass_calculator",
                        "query": query,
                        "answer": f"Molar mass of {compound}: {mass_result['molar_mass']} g/mol\nSteps:\n" + "\n".join(mass_result["steps"]),
                        "details": mass_result,
                        "confidence": 0.90
                    }

        # Check for pH calculations
        if "ph of" in query_lower:
            compound_match = re.search(r"ph of\s+([a-zA-Z0-9]+)\s+(\d*\.?\d*)\s*m", query_lower)
            if compound_match:
                compound, concentration = compound_match.groups()
                concentration = float(concentration)
                ph_result = self.ph_calculator.calculate_ph(compound, concentration)
                if ph_result["success"]:
                    return {
                        "agent": "chemistry",
                        "tool_used": "ph_calculator",
                        "query": query,
                        "answer": f"pH of {compound} ({concentration} M): {ph_result['ph']}\nSteps:\n" + "\n".join(ph_result["steps"]),
                        "details": ph_result,
                        "confidence": 0.90
                    }

        # Fallback to language model for theoretical questions
        return self._use_language_model(query, context, rag_context)

    def _use_language_model(self, query: str, context: str, rag_context: str) -> dict:
        """Use language model for chemistry explanations"""
        prompt = (
            f"You are a chemistry expert. Given the context: {context}\n"
            f"Relevant knowledge: {rag_context}\n"
            f"Query: {query}\n"
            f"For calculations, solve step-by-step and provide the final answer. "
            f"For theoretical questions, explain clearly with examples if applicable. "
            f"Keep the response concise and accurate."
        )
        response = chem_pipeline(prompt, max_length=300, num_return_sequences=1, temperature=0.7)[0]["generated_text"]
        return {
            "agent": "chemistry",
            "tool_used": "language_model",
            "query": query,
            "answer": response,
            "confidence": 0.75
        }

chemistry_agent = Agent(
    role="Chemistry Agent",
    goal="Answer chemistry-related questions and perform calculations",
    backstory="An expert in organic, inorganic, and physical chemistry",
    llm=lambda x, **kwargs: ChemistryAgent().solve_chemistry_query(x, kwargs.get("user_id", "default"))["answer"],
    tools=[
        ChemicalEquationBalancer().balance_equation,
        MolarMassCalculator().calculate_molar_mass,
        pHCalculator().calculate_ph
    ],
    verbose=True
)