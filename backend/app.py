from flask import Flask, request, jsonify
from agents.math_agent import math_agent
from crewai import Crew, Task
from db.database import init_db

app = Flask(__name__)
init_db()

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.json
    query = data.get("query")
    user_id = data.get("user_id", "default")
    task = Task(description=query, agent=math_agent, context={"user_id": user_id})
    crew = Crew(agents=[math_agent], tasks=[task])
    response = crew.kickoff()
    return jsonify({"response": response})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Backend is running"})

if __name__ == "__main__":
    app.run(debug=True)