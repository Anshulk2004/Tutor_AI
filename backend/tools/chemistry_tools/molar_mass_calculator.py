from typing import Dict, Any
import re

class MolarMassCalculator:
    """Calculate molar mass of chemical compounds"""
       
    # Atomic masses (g/mol)
    ATOMIC_MASSES = {
        "H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007, "S": 32.06,
        "Na": 22.990, "Cl": 35.453, "Ca": 40.078
    }
       
    def calculate_molar_mass(self, compound: str) -> Dict[str, Any]:
        """Calculate molar mass of a compound (e.g., H2SO4)"""
        try:
            elements = self._parse_compound(compound)
            total_mass = 0.0
            steps = []
               
            for element, count in elements.items():
                mass = self.ATOMIC_MASSES.get(element, 0) * count
                total_mass += mass
                steps.append(f"{element}: {count} x {self.ATOMIC_MASSES.get(element, 0)} = {mass} g/mol")
               
            steps.append(f"Total molar mass: {total_mass} g/mol")
               
            return {
                "compound": compound,
                "molar_mass": round(total_mass, 3),
                "steps": steps,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "compound": compound,
                "success": False,
                "error": str(e)
            }
       
    def _parse_compound(self, compound: str) -> Dict[str, int]:
        """Parse compound into elements and counts"""
        elements = {}
        pattern = r"([A-Z][a-z]?)(\d*)"
        for element, count in re.findall(pattern, compound):
            count = int(count) if count else 1
            elements[element] = elements.get(element, 0) + count
        return elements