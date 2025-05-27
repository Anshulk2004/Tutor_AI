from typing import Dict, Any
import re

class EnergyCalculator:
    """Calculate energy quantities"""
       
    def calculate_energy(self, query: str) -> Dict[str, Any]:
        """Compute kinetic or potential energy"""
        try:
            mass = re.search(r"mass\s*(\d+\.?\d*)", query.lower())
            velocity = re.search(r"velocity\s*(\d+\.?\d*)", query.lower())
            height = re.search(r"height\s*(\d+\.?\d*)", query.lower())
               
            steps = []
            result = None
               
            # Kinetic Energy: KE = 0.5 * m * v^2
            if "kinetic" in query.lower() and mass and velocity:
                m = float(mass.group(1))
                v = float(velocity.group(1))
                ke = 0.5 * m * v * v
                steps = [
                    f"Using KE = 0.5 * m * v²",
                    f"m = {m} kg, v = {v} m/s",
                    f"KE = 0.5 * {m} * {v}² = {ke} J"
                ]
                result = ke
               
            # Potential Energy: PE = m * g * h (g = 9.81 m/s²)
            elif "potential" in query.lower() and mass and height:
                m = float(mass.group(1))
                h = float(height.group(1))
                g = 9.81
                pe = m * g * h
                steps = [
                    f"Using PE = m * g * h",
                    f"m = {m} kg, g = {g} m/s², h = {h} m",
                    f"PE = {m} * {g} * {h} = {pe} J"
                ]
                result = pe
               
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