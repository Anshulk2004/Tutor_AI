from crewai import Agent
import google.generativeai as genai
from db.database import get_query_history
from rag import setup_rag, retrieve_context
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
vector_store = setup_rag()

class TutorAgent:
    def __init__(self):
        pass  # No specific tools needed for general queries

    def handle_general_query(self, query: str, user_id: str = "default") -> dict:
        """Handle general queries using Gemini API"""
        history = get_query_history(user_id, limit=3)
        context = "Recent queries: " + "; ".join([f"{h['query']} ({h['subject']})" for h in history])
        rag_context = retrieve_context(query, vector_store)

        prompt = (
            f"You are a knowledgeable tutor. Given the context: {context}\n"
            f"Relevant knowledge: {rag_context}\n"
            f"Query: {query}\n"
            f"Provide a clear, concise, and accurate response. "
            f"For questions requiring explanation, include examples if applicable. "
            f"If the query is unclear, ask for clarification."
        )
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 300,
                    "temperature": 0.7,
                }
            )
            answer = response.text
            return {
                "agent": "tutor",
                "tool_used": "language_model",
                "query": query,
                "answer": answer,
                "confidence": 0.75
            }
        except Exception as e:
            return {
                "agent": "tutor",
                "tool_used": "language_model",
                "query": query,
                "answer": f"Error: {str(e)}",
                "confidence": 0.0
            }

tutor_agent = Agent(
    role="Tutor Agent",
    goal="Answer general questions and provide educational support",
    backstory="A versatile educator skilled in various subjects, ready to assist with any query",
    llm=lambda x, **kwargs: TutorAgent().handle_general_query(x, kwargs.get("user_id", "default"))["answer"],
    tools=[],
    verbose=True
)
