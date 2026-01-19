"""
SCCT Question Agent

Purpose: Manage the SCCT question bank, return appropriate questions, and validate responses.

Inputs:
- veteran_id: The veteran taking the assessment
- session_context: Previous responses in session (for adaptive questioning, future)

Outputs:
- questions: List[SCCTQuestion] - Ordered list of questions to present
- validation_result: ValidationResult - Whether a submitted response is valid

What it must NOT decide:
- Question weighting (that's Scoring Agent's job)
- Answer meaning (that's the Confidence Vector's job)
- Completion status (that's Orchestrator's job)
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.scct import SCCTQuestion, SCCTOption


class SCCTQuestionAgent:
    """Agent for managing SCCT questions and validating responses."""

    def __init__(self, db: Session):
        self.db = db

    def get_questions(self, veteran_id: int) -> List[Dict[str, Any]]:
        """
        Return the 10 SCCT questions in presentation order.
        """
        questions = self.db.query(SCCTQuestion).order_by(SCCTQuestion.order).all()

        result = []
        for q in questions:
            options = self.db.query(SCCTOption).filter(
                SCCTOption.question_id == q.id
            ).order_by(SCCTOption.option_key).all()

            result.append({
                "id": q.id,
                "question_key": q.question_key,
                "scct_construct": q.scct_construct,
                "question_text": q.question_text,
                "order": q.order,
                "options": [
                    {
                        "id": opt.id,
                        "option_key": opt.option_key,
                        "option_text": opt.option_text,
                    }
                    for opt in options
                ],
            })

        return result

    def validate_response(self, question_id: int, option_id: int) -> Dict[str, Any]:
        """
        Ensure the option belongs to the question and is valid.
        """
        question = self.db.query(SCCTQuestion).filter(
            SCCTQuestion.id == question_id
        ).first()

        if not question:
            return {
                "valid": False,
                "error": f"Question {question_id} not found",
            }

        option = self.db.query(SCCTOption).filter(
            SCCTOption.id == option_id,
            SCCTOption.question_id == question_id
        ).first()

        if not option:
            return {
                "valid": False,
                "error": f"Option {option_id} not valid for question {question_id}",
            }

        return {
            "valid": True,
            "question_key": question.question_key,
            "option_key": option.option_key,
        }

    def get_question_metadata(self, question_id: int) -> Optional[Dict[str, Any]]:
        """
        Return SCCT construct, help text, and option details for a question.
        """
        question = self.db.query(SCCTQuestion).filter(
            SCCTQuestion.id == question_id
        ).first()

        if not question:
            return None

        options = self.db.query(SCCTOption).filter(
            SCCTOption.question_id == question_id
        ).order_by(SCCTOption.option_key).all()

        return {
            "id": question.id,
            "question_key": question.question_key,
            "scct_construct": question.scct_construct,
            "question_text": question.question_text,
            "options": [
                {
                    "id": opt.id,
                    "option_key": opt.option_key,
                    "option_text": opt.option_text,
                }
                for opt in options
            ],
        }
