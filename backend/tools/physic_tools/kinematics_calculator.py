from typing import Dict, Any
import re

class KinematicsCalculator:
    """Calculate kinematics quantities"""
       
    def calculate_kinematics(self, query: str) -> Dict[str, Any]:
        """Solve kinematics problems (e.g., v = u + at)"""
        try:
            # Parse query for known variables
            initial_velocity = re.search(r"initial velocity\s*(\d+\.?\d*)", query.lower())
            acceleration = re.search(r"acceleration\s*(\d+\.?\d*)", query.lower())
            time = re.search(r"time\s*(\d+\.?\d*)", query.lower())
            final_velocity = re.search(r"final velocity\s*(\d+\.?\d*)", query.lower())
               
            steps = []
            result = None
               
            # Example: v = u + at
            if initial_velocity and acceleration and time and "final velocity" in query.lower():
                u = float(initial_velocity.group(1))
                a = float(acceleration.group(1))
                t = float(time.group(1))
                v = u + a * t
                steps = [
                    f"Using v = u + at",
                    f"u = {u} m/s, a = {a} m/s², t = {t} s",
                    f"v = {u} + {a} * {t} = {v} m/s"
                ]
                result = v
               
            if result is not None:
                return {
                    "query": query,
                    "result": round(result, 2),
                    "steps": steps,
                    "success": True,
                    "error": None
                }
            return {
                "query": query,
                "success": False,
                "error": "Insufficient or invalid parameters"
            }
        except Exception as e:
            return {
                "query": query,
                "success": False,
                "error": str(e)
            }