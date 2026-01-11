from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.veteran import Veteran
from app.models.assessment import AssessmentResponse, Question
from app.models.cyber_role import RoleMatch
from app.services.matching import get_top_role_matches, calculate_trait_scores

router = APIRouter()


@router.get("/results/{veteran_id}", response_model=List[RoleMatch])
def get_results(veteran_id: int, db: Session = Depends(get_db)):
    """
    Get the top 3 cybersecurity role recommendations for a veteran.
    The veteran must have completed the personality assessment first.
    """
    # Verify veteran exists
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")
    
    # Check if assessment is complete
    response_count = db.query(AssessmentResponse).filter(
        AssessmentResponse.veteran_id == veteran_id
    ).count()
    
    if response_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Assessment not completed. Please complete the personality assessment first."
        )
    
    # Get top 3 matches
    matches = get_top_role_matches(db, veteran_id, top_n=3)
    
    if not matches:
        raise HTTPException(
            status_code=500,
            detail="Unable to calculate matches. Please try again."
        )
    
    return matches


@router.get("/results/{veteran_id}/full")
def get_full_results(veteran_id: int, db: Session = Depends(get_db)):
    """
    Get detailed results including trait scores and all role matches.
    """
    # Verify veteran exists
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")
    
    # Check if assessment is complete
    response_count = db.query(AssessmentResponse).filter(
        AssessmentResponse.veteran_id == veteran_id
    ).count()
    
    if response_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Assessment not completed. Please complete the personality assessment first."
        )
    
    # Get trait scores
    trait_scores = calculate_trait_scores(db, veteran_id)
    
    # Get all matches (not just top 3)
    all_matches = get_top_role_matches(db, veteran_id, top_n=10)
    
    return {
        "veteran": {
            "id": veteran.id,
            "name": veteran.name,
            "branch": veteran.branch,
            "rank": veteran.rank,
            "years_of_service": veteran.years_of_service,
        },
        "trait_scores": trait_scores,
        "top_matches": [m.model_dump() for m in all_matches[:3]],
        "all_matches": [m.model_dump() for m in all_matches],
    }
