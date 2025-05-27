import math
import re
from typing import Dict, Any

class BasicCalculator:
    """Advanced calculator with support for various mathematical operations"""
    
    def __init__(self):
        self.last_result = 0
        self.memory = 0
        
    def evaluate_expression(self, expression: str) -> Dict[str, Any]:
        """Safely evaluate mathematical expressions"""
        try:
            cleaned_expr = self._clean_expression(expression)
            cleaned_expr = self._handle_special_functions(cleaned_expr)
            result = eval(cleaned_expr, {"__builtins__": {}}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "sqrt": math.sqrt,
                "pi": math.pi, "e": math.e, "abs": abs, "pow": pow,
                "floor": math.floor, "ceil": math.ceil, "round": round
            })
            self.last_result = result
            return {
                "result": result,
                "expression": expression,
                "cleaned_expression": cleaned_expr,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "result": None,
                "expression": expression,
                "success": False,
                "error": str(e)
            }
    
    def _clean_expression(self, expr: str) -> str:
        """Clean and prepare expression for evaluation"""
        expr = expr.replace(" ", "").replace("×", "*").replace("÷", "/").replace("^", "**")
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)
        return expr
    
    def _handle_special_functions(self, expr: str) -> str:
        """Convert special function names to Python equivalents"""
        replacements = {
            'ln': 'log', 'lg': 'log10', 'arcsin': 'asin', 'arccos': 'acos', 'arctan': 'atan'
        }
        for old, new in replacements.items():
            expr = expr.replace(old, new)
        return expr
    
    def percentage(self, value: float, percentage: float) -> float:
        """Calculate percentage of a value"""
        return (value * percentage) / 100