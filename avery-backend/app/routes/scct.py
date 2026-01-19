"""
SCCT (Social Cognitive Career Theory) assessment routes.
Handles the 10-question SCCT onboarding flow.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.veteran import Veteran
from app.models.scct import (
    SCCTQuestion,
    SCCTOption,
    SCCTResponse,
    ConfidenceVector,
    SalaryBand,
    SCCTQuestionResponse,
    SCCTSubmission,
    SCCTSubmitResponse,
    ConfidenceVectorResponse,
)

router = APIRouter()


@router.get("/scct/questions", response_model=List[SCCTQuestionResponse])
def get_scct_questions(db: Session = Depends(get_db)):
    """
    Get all 10 SCCT assessment questions with their options.
    Questions are ordered and should be presented in sequence.
    Each question has 4-5 tappable options (no Likert scale).
    """
    questions = db.query(SCCTQuestion).order_by(SCCTQuestion.order).all()
    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No SCCT questions found. Please run the SCCT seed script."
        )

    # Load options for each question
    result = []
    for q in questions:
        options = db.query(SCCTOption).filter(
            SCCTOption.question_id == q.id
        ).order_by(SCCTOption.option_key).all()

        result.append(SCCTQuestionResponse(
            id=q.id,
            question_key=q.question_key,
            scct_construct=q.scct_construct,
            question_text=q.question_text,
            order=q.order,
            options=[{
                "id": opt.id,
                "option_key": opt.option_key,
                "option_text": opt.option_text,
            } for opt in options]
        ))

    return result


@router.post("/scct/submit", response_model=SCCTSubmitResponse)
def submit_scct_assessment(submission: SCCTSubmission, db: Session = Depends(get_db)):
    """
    Submit all SCCT assessment answers for a veteran.
    Each answer should have a question_id and option_id.
    This will compute and store the Career Confidence Vector.
    """
    # Verify veteran exists
    veteran = db.query(Veteran).filter(Veteran.id == submission.veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")

    # Verify all questions and options exist
    for answer in submission.answers:
        question = db.query(SCCTQuestion).filter(SCCTQuestion.id == answer.question_id).first()
        if not question:
            raise HTTPException(status_code=400, detail=f"Invalid question ID: {answer.question_id}")

        option = db.query(SCCTOption).filter(
            SCCTOption.id == answer.option_id,
            SCCTOption.question_id == answer.question_id
        ).first()
        if not option:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid option ID {answer.option_id} for question {answer.question_id}"
            )

    # Delete any existing SCCT responses for this veteran (allow retakes)
    db.query(SCCTResponse).filter(SCCTResponse.veteran_id == submission.veteran_id).delete()

    # Delete existing confidence vector
    db.query(ConfidenceVector).filter(ConfidenceVector.veteran_id == submission.veteran_id).delete()

    # Save new responses
    for answer in submission.answers:
        response = SCCTResponse(
            veteran_id=submission.veteran_id,
            question_id=answer.question_id,
            option_id=answer.option_id,
        )
        db.add(response)

    db.commit()

    # Compute and store confidence vector
    vector = compute_confidence_vector(db, submission.veteran_id)

    return SCCTSubmitResponse(
        message=f"SCCT assessment completed successfully for {veteran.name}",
        veteran_id=veteran.id,
        answers_recorded=len(submission.answers),
    )


@router.get("/scct/status/{veteran_id}")
def get_scct_status(veteran_id: int, db: Session = Depends(get_db)):
    """Check if a veteran has completed the SCCT assessment."""
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")

    response_count = db.query(SCCTResponse).filter(
        SCCTResponse.veteran_id == veteran_id
    ).count()

    total_questions = db.query(SCCTQuestion).count()

    has_vector = db.query(ConfidenceVector).filter(
        ConfidenceVector.veteran_id == veteran_id
    ).first() is not None

    return {
        "veteran_id": veteran_id,
        "veteran_name": veteran.name,
        "questions_answered": response_count,
        "total_questions": total_questions,
        "completed": response_count >= total_questions,
        "vector_computed": has_vector,
    }


@router.get("/scct/vector/{veteran_id}", response_model=ConfidenceVectorResponse)
def get_confidence_vector(veteran_id: int, db: Session = Depends(get_db)):
    """Get the computed Career Confidence Vector for a veteran."""
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")

    vector = db.query(ConfidenceVector).filter(
        ConfidenceVector.veteran_id == veteran_id
    ).first()

    if not vector:
        raise HTTPException(
            status_code=400,
            detail="Confidence vector not yet computed. Complete the SCCT assessment first."
        )

    return vector


def compute_confidence_vector(db: Session, veteran_id: int) -> ConfidenceVector:
    """
    Compute the 12-dimensional Career Confidence Vector from SCCT responses.
    This is deterministic: same inputs always produce same outputs.
    """
    # Get all responses for this veteran
    responses = db.query(SCCTResponse).filter(
        SCCTResponse.veteran_id == veteran_id
    ).all()

    if not responses:
        raise HTTPException(
            status_code=400,
            detail="No SCCT responses found for this veteran."
        )

    # Initialize accumulator
    vector_data = {
        "se_technical": 0.0,
        "se_stress": 0.0,
        "se_growth": 0.0,
        "se_social": 0.0,
        "oe_salary_priority": 0.0,
        "oe_stability_priority": 0.0,
        "oe_meaning_priority": 0.0,
        "goals_timeline": 0.0,
        "goals_level": 0.0,
        "barriers_financial": 0.0,
        "barriers_technical": 0.0,
        "barriers_direction": 0.0,
    }

    # Accumulate weights from each response's selected option
    for response in responses:
        option = db.query(SCCTOption).filter(SCCTOption.id == response.option_id).first()
        if option:
            vector_data["se_technical"] += option.se_technical
            vector_data["se_stress"] += option.se_stress
            vector_data["se_growth"] += option.se_growth
            vector_data["se_social"] += option.se_social
            vector_data["oe_salary_priority"] += option.oe_salary_priority
            vector_data["oe_stability_priority"] += option.oe_stability_priority
            vector_data["oe_meaning_priority"] += option.oe_meaning_priority
            vector_data["goals_timeline"] += option.goals_timeline
            vector_data["goals_level"] += option.goals_level
            vector_data["barriers_financial"] += option.barriers_financial
            vector_data["barriers_technical"] += option.barriers_technical
            vector_data["barriers_direction"] += option.barriers_direction

    # Normalize to 0-1 range using sigmoid-like scaling
    # This ensures extreme values are bounded but preserve relative ordering
    def normalize(value: float, min_val: float = -2.0, max_val: float = 2.0) -> float:
        """Normalize value to 0-1 range."""
        # Clamp to expected range
        clamped = max(min_val, min(max_val, value))
        # Scale to 0-1
        return (clamped - min_val) / (max_val - min_val)

    for key in vector_data:
        vector_data[key] = normalize(vector_data[key])

    # Create and store the confidence vector
    vector = ConfidenceVector(
        veteran_id=veteran_id,
        version="1.0.0",
        **vector_data
    )
    db.add(vector)
    db.commit()
    db.refresh(vector)

    return vector
