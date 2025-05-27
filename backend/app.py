from flask import Flask, request, jsonify
from agents.math_agent import math_agent
from agents.chemistry_agent import chemistry_agent
from agents.physics_agent import physics_agent
from agents.evaluation_agent import evaluation_agent
from agents.tutor_agent import tutor_agent
from crewai import Crew, Task
from db.database import init_db, save_query
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
classifier_model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
init_db()

def classify_query(query: str) -> str:
    """Classify query into subject using Gemini API"""
    prompt = (
        f"Classify the following query into one of these categories: math, chemistry, physics, evaluation, or general.\n"
        f"Query: {query}\n"
        f"Return only the category name (e.g., 'math', 'chemistry', 'physics', 'evaluation', 'general')."
    )
    try:
        response = classifier_model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 50,
                "temperature": 0.3,
            }
        )
        category = response.text.strip().lower()
        return category if category in ["math", "chemistry", "physics", "evaluation", "general"] else "general"
    except Exception as e:
        print(f"Classification error: {e}")
        return "general"

@app.route("/query", methods=["POST"])
def handle_query():
    """Handle user queries and route to appropriate agent"""
    data = request.json
    query = data.get("query")
    user_id = data.get("user_id", "default")
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    # Classify query
    subject = classify_query(query)
    
    # Save query to database
    save_query(user_id, query, subject)
    
    # Route to appropriate agent
    agent_map = {
        "math": math_agent,
        "chemistry": chemistry_agent,
        "physics": physics_agent,
        "evaluation": evaluation_agent,
        "general": tutor_agent
    }
    agent = agent_map.get(subject, tutor_agent)
    
    # Create task and execute
    task = Task(description=query, agent=agent, context={"user_id": user_id})
    crew = Crew(agents=[agent], tasks=[task])
    try:
        response = crew.kickoff()
        return jsonify({"response": response, "subject": subject})
    except Exception as e:
        return jsonify({"error": str(e), "subject": subject}), 500

@app.route("/evaluate", methods=["POST"])
def evaluate_answer():
    """Handle evaluation requests"""
    data = request.json
    query = data.get("query")
    student_answer = data.get("student_answer")
    correct_answer = data.get("correct_answer")
    user_id = data.get("user_id", "default")
    
    if not all([query, student_answer, correct_answer]):
        return jsonify({"error": "Query, student_answer, and correct_answer are required"}), 400
    
    # Save query to database
    save_query(user_id, query, "evaluation")
    
    # Execute evaluation task
    task = Task(
        description="Evaluate answer",
        agent=evaluation_agent,
        context={
            "query": query,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "user_id": user_id
        }
    )
    crew = Crew(agents=[evaluation_agent], tasks=[task])
    try:
        response = crew.kickoff()
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Check backend status"""
    return jsonify({"status": "Backend is running"})

if __name__ == "__main__":
    app.run(debug=True)
