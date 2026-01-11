from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.veteran import Veteran
from app.models.assessment import (
    Question,
    AssessmentResponse,
    QuestionResponse,
    AssessmentSubmission,
    AssessmentSubmitResponse,
)

router = APIRouter()


@router.get("/assessment/questions", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    """
    Get all personality assessment questions.
    Questions are ordered and should be presented in sequence.
    Answers should be on a 1-5 scale:
    1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree
    """
    questions = db.query(Question).order_by(Question.order).all()
    if not questions:
        raise HTTPException(
            status_code=404, 
            detail="No questions found. Please run the seed script."
        )
    return questions


@router.post("/assessment/submit", response_model=AssessmentSubmitResponse)
def submit_assessment(submission: AssessmentSubmission, db: Session = Depends(get_db)):
    """
    Submit all personality assessment answers for a veteran.
    Each answer should have a question_id and answer_value (1-5).
    """
    # Verify veteran exists
    veteran = db.query(Veteran).filter(Veteran.id == submission.veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")
    
    # Verify all questions exist
    question_ids = [a.question_id for a in submission.answers]
    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    if len(questions) != len(question_ids):
        raise HTTPException(status_code=400, detail="One or more invalid question IDs")
    
    # Delete any existing responses for this veteran (allow retakes)
    db.query(AssessmentResponse).filter(
        AssessmentResponse.veteran_id == submission.veteran_id
    ).delete()
    
    # Save new responses
    for answer in submission.answers:
        response = AssessmentResponse(
            veteran_id=submission.veteran_id,
            question_id=answer.question_id,
            answer_value=answer.answer_value,
        )
        db.add(response)
    
    db.commit()
    
    return AssessmentSubmitResponse(
        message=f"Assessment completed successfully for {veteran.name}",
        veteran_id=veteran.id,
        answers_recorded=len(submission.answers),
    )


@router.get("/assessment/status/{veteran_id}")
def get_assessment_status(veteran_id: int, db: Session = Depends(get_db)):
    """Check if a veteran has completed the assessment."""
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")
    
    response_count = db.query(AssessmentResponse).filter(
        AssessmentResponse.veteran_id == veteran_id
    ).count()
    
    total_questions = db.query(Question).count()
    
    return {
        "veteran_id": veteran_id,
        "veteran_name": veteran.name,
        "questions_answered": response_count,
        "total_questions": total_questions,
        "completed": response_count >= total_questions,
    }
