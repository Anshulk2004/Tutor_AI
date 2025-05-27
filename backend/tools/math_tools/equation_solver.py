import sympy as sp
from typing import Dict, Any, List

class EquationSolver:
    """Solve various types of mathematical equations"""
    
    def __init__(self):
        self.variables = {}
    
    def solve_linear_equation(self, equation: str) -> Dict[str, Any]:
        """Solve linear equations like '2x + 5 = 11'"""
        try:
            left, right = equation.replace(" ", "").split('=')
            x = sp.Symbol('x')
            left_expr = sp.sympify(left)
            right_expr = sp.sympify(right)
            equation_obj = sp.Eq(left_expr, right_expr)
            solution = sp.solve(equation_obj, x)
            steps = self._get_solution_steps(left_expr, right_expr, solution)
            return {
                "equation": equation,
                "solution": str(solution[0]) if solution else None,
                "steps": steps,
                "success": True,
                "variable": "x"
            }
        except Exception as e:
            return {
                "equation": equation,
                "solution": None,
                "success": False,
                "error": str(e)
            }
    
    def solve_quadratic_equation(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """Solve quadratic equations ax² + bx + c = 0"""
        try:
            discriminant = b**2 - 4*a*c
            steps = [
                f"Quadratic equation: {a}x² + {b}x + {c} = 0",
                f"Discriminant: b² - 4ac = {b}² - 4*{a}*{c} = {discriminant}"
            ]
            if discriminant > 0:
                x1 = (-b + sp.sqrt(discriminant)) / (2*a)
                x2 = (-b - sp.sqrt(discriminant)) / (2*a)
                steps.append(f"Roots: x = (-{b} ± √{discriminant})/(2*{a})")
                steps.append(f"x1 = {x1}, x2 = {x2}")
                return {
                    "equation": f"{a}x² + {b}x + {c} = 0",
                    "solutions": [str(x1), str(x2)],
                    "discriminant": discriminant,
                    "nature": "Two real roots",
                    "success": True,
                    "steps": steps
                }
            elif discriminant == 0:
                x = -b / (2*a)
                steps.append(f"Root: x = -{b}/(2*{a}) = {x}")
                return {
                    "equation": f"{a}x² + {b}x + {c} = 0",
                    "solutions": [str(x)],
                    "discriminant": discriminant,
                    "nature": "One real root",
                    "success": True,
                    "steps": steps
                }
            else:
                real_part = -b / (2*a)
                imag_part = sp.sqrt(-discriminant) / (2*a)
                steps.append(f"Complex roots: x = {real_part} ± {imag_part}i")
                return {
                    "equation": f"{a}x² + {b}x + {c} = 0",
                    "solutions": [f"{real_part} + {imag_part}i", f"{real_part} - {imag_part}i"],
                    "discriminant": discriminant,
                    "nature": "Complex roots",
                    "success": True,
                    "steps": steps
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps": []
            }
    
    def _get_solution_steps(self, left_expr, right_expr, solution) -> List[str]:
        """Generate step-by-step solution"""
        steps = [
            f"Original equation: {left_expr} = {right_expr}",
            f"Rearrange: {left_expr - right_expr} = 0"
        ]
        if solution:
            steps.append(f"Solution: x = {solution[0]}")
        return steps