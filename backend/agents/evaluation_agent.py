from crewai import Agent
from transformers import pipeline
from tools.general_tools.answer_comparator import AnswerComparator
from tools.general_tools.feedback_generator import FeedbackGenerator
from db.database import get_query_history, save_content
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
vector_store = setup_rag()

class EvaluationAgent:
    def __init__(self):
        self.answer_comparator = AnswerComparator()
        self.feedback_generator = FeedbackGenerator()

    def evaluate_answer(self, query: str, student_answer: str, correct_answer: str, user_id: str = "default") -> dict:
        """Evaluate student answer and provide feedback"""
        history = get_query_history(user_id, limit=3)
        context = "Recent queries: " + "; ".join([f"{h['query']} ({h['subject']})" for h in history])

        # Compare answers
        comparison_result = self.answer_comparator.compare_answer(student_answer, correct_answer, query)
        if not comparison_result["success"]:
            return {
                "agent": "evaluation",
                "query": query,
                "success": False,
                "error": comparison_result["error"]
            }

        # Generate feedback
        feedback_result = self.feedback_generator.generate_feedback(
            query, student_answer, correct_answer, comparison_result["is_correct"]
        )
        
        # Save evaluation to database
        save_content(user_id, "evaluation", feedback_result["feedback"])

        return {
            "agent": "evaluation",
            "query": query,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "is_correct": comparison_result["is_correct"],
            "feedback": feedback_result["feedback"],
            "similarity": comparison_result["similarity"],
            "confidence": 0.85,
            "success": True
        }

evaluation_agent = Agent(
    role="Evaluation Agent",
    goal="Evaluate student answers and provide feedback",
    backstory="An expert in assessing responses across math, physics, and chemistry",
    llm=lambda x, **kwargs: EvaluationAgent().evaluate_answer(
        kwargs.get("query", ""),
        kwargs.get("student_answer", ""),
        kwargs.get("correct_answer", ""),
        kwargs.get("user_id", "default")
    )["feedback"],
    tools=[
        AnswerComparator().compare_answer,
        FeedbackGenerator().generate_feedback
    ],
    verbose=True
)