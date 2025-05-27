from typing import Dict, Any, Optional

class PhysicsConstants:
    """Comprehensive physics constants database"""
    
    def __init__(self):
        self.constants = {
            # Universal constants
            "speed_of_light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
            "planck_constant": {"value": 6.62607015e-34, "unit": "J⋅s", "symbol": "h"},
            "gravitational_constant": {"value": 6.67430e-11, "unit": "m³⋅kg⁻¹⋅s⁻²", "symbol": "G"},
            "elementary_charge": {"value": 1.602176634e-19, "unit": "C", "symbol": "e"},
            
            # Earth-specific
            "gravity_earth": {"value": 9.80665, "unit": "m/s²", "symbol": "g"},
            "earth_mass": {"value": 5.972e24, "unit": "kg", "symbol": "M_earth"},
            "earth_radius": {"value": 6.371e6, "unit": "m", "symbol": "R_earth"},
            
            # Electromagnetic
            "vacuum_permittivity": {"value": 8.8541878128e-12, "unit": "F/m", "symbol": "ε₀"},
            "vacuum_permeability": {"value": 1.25663706212e-6, "unit": "H/m", "symbol": "μ₀"},
            
            # Thermodynamic
            "boltzmann_constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k_B"},
            "avogadro_number": {"value": 6.02214076e23, "unit": "mol⁻¹", "symbol": "N_A"},
            "gas_constant": {"value": 8.314462618, "unit": "J⋅mol⁻¹⋅K⁻¹", "symbol": "R"},
            
            # Atomic
            "electron_mass": {"value": 9.1093837015e-31, "unit": "kg", "symbol": "m_e"},
            "proton_mass": {"value": 1.67262192369e-27, "unit": "kg", "symbol": "m_p"},
            "neutron_mass": {"value": 1.67492749804e-27, "unit": "kg", "symbol": "m_n"},
        }
    
    def get_constant(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a physics constant by name"""
        return self.constants.get(name.lower())
    
    def search_constants(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Search for constants by keyword"""
        results = {}
        query_lower = query.lower()
        
        for name, data in self.constants.items():
            if (query_lower in name.lower() or 
                query_lower in data["symbol"].lower() or
                query_lower in data["unit"].lower()):
                results[name] = data
                
        return results
    
    def list_all_constants(self) -> Dict[str, Dict[str, Any]]:
        """Return all available constants"""
        return self.constants
    
    def get_constant_info(self, name: str) -> str:
        """Get formatted information about a constant"""
        constant = self.get_constant(name)
        if constant:
            return f"{constant['symbol']} = {constant['value']} {constant['unit']}"
        return f"Constant '{name}' not found"

# Usage
if __name__ == "__main__":
    constants = PhysicsConstants()
    print(constants.get_constant("speed_of_light"))
    print(constants.search_constants("mass"))