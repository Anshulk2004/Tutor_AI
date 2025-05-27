from crewai import Agent
import google.generativeai as genai
from transformers import pipeline
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from tools.math_tools.calculator import BasicCalculator
from tools.math_tools.equation_solver import EquationSolver
from tools.math_tools.statistics_calculator import StatisticsCalculator
from tools.math_tools.geometry_calculator import GeometryCalculator
from db.database import get_query_history
from rag import retrieve_context, setup_rag
import os
from dotenv import load_dotenv
import re
# import torch

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
vector_store = setup_rag()

class MathAgent:
    def __init__(self):
        self.calculator = BasicCalculator()
        self.equation_solver = EquationSolver()
        self.stats_calculator = StatisticsCalculator()
        self.geometry_calculator = GeometryCalculator()

    def solve_math_query(self, query: str, user_id: str = "default") -> dict:
        """Route query to appropriate tool or model"""
        query_lower = query.lower().replace(" ", "")
        history = get_query_history(user_id, limit=3)
        context = "Recent queries: " + "; ".join([f"{h['query']} ({h['subject']})" for h in history])
        rag_context = retrieve_context(query, vector_store)

        # Check for arithmetic calculations
        if any(op in query_lower for op in ['+', '-', '*', '/', '(', ')', '^']):
            calc_result = self.calculator.evaluate_expression(query)
            if calc_result["success"]:
                return {
                    "agent": "math",
                    "tool_used": "calculator",
                    "query": query,
                    "answer": f"Result: {calc_result['result']}",
                    "details": calc_result,
                    "confidence": 0.95
                }

        # Check for linear equations
        if '=' in query_lower and any(var in query_lower for var in ['x', 'y', 'z']):
            eq_result = self.equation_solver.solve_linear_equation(query)
            if eq_result["success"]:
                return {
                    "agent": "math",
                    "tool_used": "equation_solver",
                    "query": query,
                    "answer": f"Solution: {eq_result['variable']} = {eq_result['solution']}\nSteps:\n" + "\n".join(eq_result["steps"]),
                    "details": eq_result,
                    "confidence": 0.90
                }

        # Check for quadratic equations (e.g., "Solve x^2 + 5x + 6 = 0")
        quadratic_match = re.match(r'(\d*)x\^2\s*([+-]?\s*\d*)x\s*([+-]?\s*\d*)\s*=\s*0', query_lower)
        if quadratic_match:
            a = int(quadratic_match.group(1) or 1)
            b = int((quadratic_match.group(2).replace(" ", "") or "+0").replace("+", ""))
            c = int((quadratic_match.group(3).replace(" ", "") or "+0").replace("+", ""))
            quad_result = self.equation_solver.solve_quadratic_equation(a, b, c)
            if quad_result["success"]:
                return {
                    "agent": "math",
                    "tool_used": "equation_solver",
                    "query": query,
                    "answer": f"Solutions: {', '.join(quad_result['solutions'])}\nSteps:\n" + "\n".join(quad_result["steps"]),
                    "details": quad_result,
                    "confidence": 0.90
                }

        # Check for statistics queries (e.g., "Find mean of 1,2,3,4,5")
        if any(keyword in query_lower for keyword in ['mean', 'median', 'mode', 'standard deviation']):
            stats_result = self.stats_calculator.calculate_stats(query.split("of")[-1].strip())
            if stats_result["success"]:
                return {
                    "agent": "math",
                    "tool_used": "statistics_calculator",
                    "query": query,
                    "answer": f"Mean: {stats_result['mean']}, Median: {stats_result['median']}, Mode: {stats_result['mode']}, Std Dev: {stats_result['std_dev']}",
                    "details": stats_result,
                    "confidence": 0.90
                }

        # Check for geometry queries (e.g., "Area of circle with radius 5")
        if 'area' in query_lower and any(shape in query_lower for shape in ['circle', 'rectangle']):
            shape = 'circle' if 'circle' in query_lower else 'rectangle'
            params = {}
            if shape == 'circle':
                radius_match = re.search(r'radius\s*(\d+)', query_lower)
                if radius_match:
                    params["radius"] = float(radius_match.group(1))
            elif shape == 'rectangle':
                length_match = re.search(r'length\s*(\d+)', query_lower)
                width_match = re.search(r'width\s*(\d+)', query_lower)
                if length_match and width_match:
                    params["length"] = float(length_match.group(1))
                    params["width"] = float(width_match.group(1))
            geo_result = self.geometry_calculator.calculate_area(shape, params)
            if geo_result["success"]:
                return {
                    "agent": "math",
                    "tool_used": "geometry_calculator",
                    "query": query,
                    "answer": f"Area of {shape}: {geo_result['area']}",
                    "details": geo_result,
                    "confidence": 0.90
                }

        # Fallback to language model for theoretical questions
        return self._use_language_model(query, context, rag_context)

    def _use_language_model(self, query: str, context: str, rag_context: str) -> dict:
        """Use language model for complex math explanations"""
        prompt = (
            f"You are a math expert. Given the context: {context}\n"
            f"Relevant knowledge: {rag_context}\n"
            f"Query: {query}\n"
            f"For numerical questions, solve step-by-step and provide the final answer. "
            f"For theoretical questions, explain clearly with examples if applicable. "
            f"Keep the response concise and accurate."
        )
        response = math_pipeline(prompt, max_length=300, num_return_sequences=1, temperature=0.7)[0]["generated_text"]
        return {
            "agent": "math",
            "tool_used": "language_model",
            "query": query,
            "answer": response,
            "confidence": 0.75
        }

math_agent = Agent(
    role="Math Agent",
    goal="Answer mathematics-related questions and perform calculations",
    backstory="An expert in algebra, calculus, statistics, and geometry",
    llm=lambda x, **kwargs: MathAgent().solve_math_query(x, kwargs.get("user_id", "default"))["answer"],
    tools=[BasicCalculator().evaluate_expression, EquationSolver().solve_linear_equation, 
           EquationSolver().solve_quadratic_equation, StatisticsCalculator().calculate_stats,
           GeometryCalculator().calculate_area],
    verbose=True
)