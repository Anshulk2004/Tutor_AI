from typing import Dict, Any
import re

class CircuitCalculator:
    """Calculate circuit quantities"""
       
    def calculate_circuit(self, query: str) -> Dict[str, Any]:
        """Compute current, voltage, or resistance (Ohm's Law)"""
        try:
            voltage = re.search(r"voltage\s*(\d+\.?\d*)", query.lower())
            resistance = re.search(r"resistance\s*(\d+\.?\d*)", query.lower())
               
            steps = []
            result = None
               
            # Ohm's Law: I = V / R
            if "current" in query.lower() and voltage and resistance:
                v = float(voltage.group(1))
                r = float(resistance.group(1))
                i = v / r
                steps = [
                    f"Using I = V / R",
                    f"V = {v} V, R = {r} Ω",
                    f"I = {v} / {r} = {i} A"
                ]
                result = i
               
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