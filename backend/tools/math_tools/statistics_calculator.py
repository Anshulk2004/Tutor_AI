from typing import Dict, Any, List
import statistics

class StatisticsCalculator:
    """Calculate statistical measures"""
    
    def calculate_stats(self, data: str) -> Dict[str, Any]:
        """Calculate mean, median, mode, and standard deviation"""
        try:
            numbers = [float(x) for x in data.split(",")]
            return {
                "data": numbers,
                "mean": statistics.mean(numbers),
                "median": statistics.median(numbers),
                "mode": statistics.mode(numbers) if len(set(numbers)) != len(numbers) else "No unique mode",
                "std_dev": statistics.stdev(numbers) if len(numbers) > 1 else 0,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "data": data,
                "success": False,
                "error": str(e)
            }