from typing import Dict, Any
import math

class pHCalculator:
    """Calculate pH of solutions"""
       
    def calculate_ph(self, compound: str, concentration: float) -> Dict[str, Any]:
        """Calculate pH for strong acids/bases"""
        try:
            # Simplified: assumes strong acids (e.g., HCl) or bases (e.g., NaOH)
            if compound.lower() == "hcl":
                ph = -math.log10(concentration)
                steps = [
                    f"Strong acid (HCl), [H+] = {concentration} M",
                    f"pH = -log10({concentration}) = {ph}"
                ]
                return {
                    "compound": compound,
                    "concentration": concentration,
                    "ph": round(ph, 2),
                    "steps": steps,
                    "success": True,
                    "error": None
                }
            elif compound.lower() == "naoh":
                poh = -math.log10(concentration)
                ph = 14 - poh
                steps = [
                    f"Strong base (NaOH), [OH-] = {concentration} M",
                    f"pOH = -log10({concentration}) = {poh}",
                    f"pH = 14 - {poh} = {ph}"
                ]
                return {
                    "compound": compound,
                    "concentration": concentration,
                    "ph": round(ph, 2),
                    "steps": steps,
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "compound": compound,
                    "success": False,
                    "error": "Only HCl and NaOH supported for now"
                }
        except Exception as e:
            return {
                "compound": compound,
                "success": False,
                "error": str(e)
            }