import math
from typing import Dict, Any

class GeometryCalculator:
    """Calculate geometric properties"""
    
    def calculate_area(self, shape: str, params: Dict[str, float]) -> Dict[str, Any]:
        """Calculate area of shapes"""
        try:
            shape = shape.lower()
            if shape == "circle":
                radius = params.get("radius")
                area = math.pi * radius ** 2
                return {
                    "shape": "circle",
                    "radius": radius,
                    "area": area,
                    "success": True,
                    "error": None
                }
            elif shape == "rectangle":
                length = params.get("length")
                width = params.get("width")
                area = length * width
                return {
                    "shape": "rectangle",
                    "length": length,
                    "width": width,
                    "area": area,
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "shape": shape,
                    "success": False,
                    "error": "Unsupported shape"
                }
        except Exception as e:
            return {
                "shape": shape,
                "success": False,
                "error": str(e)
            }