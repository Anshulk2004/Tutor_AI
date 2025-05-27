from typing import Dict, Any
import re
from difflib import SequenceMatcher

class AnswerComparator:
    """Compare student answers to correct answers"""
       
    def compare_answer(self, student_answer: str, correct_answer: str, query: str) -> Dict[str, Any]:
        """Compare answers and determine correctness"""
        try:
            student_answer = student_answer.strip().lower()
            correct_answer = correct_answer.strip().lower()
               
               # Numerical comparison (e.g., "5" vs "5.0")
            try:
                if float(student_answer) == float(correct_answer):
                    return {
                        "query": query,
                        "student_answer": student_answer,
                        "correct_answer": correct_answer,
                        "is_correct": True,
                        "similarity": 1.0,
                        "success": True,
                        "error": None
                       }
            except ValueError:
                pass
               
            # Text comparison
            similarity = SequenceMatcher(None, student_answer, correct_answer).ratio()
            is_correct = similarity > 0.85
               
            return {
                "query": query,
                "student_answer": student_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "similarity": round(similarity, 2),
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "query": query,
                "success": False,
                "error": str(e)
            }