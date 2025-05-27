from typing import Dict, Any
class FeedbackGenerator:
    """Generate feedback for student answers"""
       
    def generate_feedback(self, query: str, student_answer: str, correct_answer: str, is_correct: bool) -> Dict[str, Any]:
        """Generate constructive feedback"""
        try:
            if is_correct:
                feedback = f"Great job! Your answer '{student_answer}' is correct for the query '{query}'."
            else:
                feedback = (
                    f"Your answer '{student_answer}' is incorrect for '{query}'. "
                    f"The correct answer is '{correct_answer}'. "
                    f"Please review the concept and try again."
                )
               
            return {
                "query": query,
                "student_answer": student_answer,
                "correct_answer": correct_answer,
                "feedback": feedback,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "query": query,
                "success": False,
                "error": str(e)
            }