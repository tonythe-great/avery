from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.veteran import Veteran
from app.models.assessment import AssessmentResponse, Question
from app.models.cyber_role import CyberRole, RoleMatch
from app.models.scct import ConfidenceVector
from app.services.matching import get_top_role_matches, calculate_trait_scores
from app.agents.career_coach_agent import CareerCoachAgent


# LLM Response Models
class LLMRecommendation(BaseModel):
    role_id: int
    role_name: str
    match_score: float
    primary_reason: str
    fit_factors: List[str]
    concerns: List[str]
    avery_quote: str


class LLMResultsResponse(BaseModel):
    avery_intro: str
    recommendations: List[LLMRecommendation]
    fallback_used: bool = False


# Initialize the career coach agent
career_coach = CareerCoachAgent()

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


@router.get("/results/{veteran_id}/llm", response_model=LLMResultsResponse)
def get_llm_results(veteran_id: int, db: Session = Depends(get_db)):
    """
    Get LLM-powered career recommendations with Avery's voice.

    This endpoint uses Claude to generate personalized recommendations
    based on the veteran's profile and SCCT assessment results.
    Falls back to algorithmic matching if LLM is unavailable.
    """
    # Verify veteran exists
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")

    # Get confidence vector (SCCT assessment must be completed)
    vector = db.query(ConfidenceVector).filter(
        ConfidenceVector.veteran_id == veteran_id
    ).first()

    if not vector:
        raise HTTPException(
            status_code=400,
            detail="SCCT assessment not completed. Please complete the assessment first."
        )

    # Get all available cyber roles
    roles = db.query(CyberRole).all()
    if not roles:
        raise HTTPException(status_code=500, detail="No cyber roles available")

    # Prepare veteran profile dict
    veteran_profile = {
        "name": veteran.name,
        "rank": veteran.rank,
        "rating": veteran.rating,
        "security_clearance": veteran.security_clearance,
        "years_of_service": veteran.years_of_service,
    }

    # Prepare SCCT vector dict
    scct_vector = {
        "se_technical": vector.se_technical,
        "se_stress": vector.se_stress,
        "se_growth": vector.se_growth,
        "se_social": vector.se_social,
        "oe_salary_priority": vector.oe_salary_priority,
        "oe_stability_priority": vector.oe_stability_priority,
        "oe_meaning_priority": vector.oe_meaning_priority,
        "goals_timeline": vector.goals_timeline,
        "goals_level": vector.goals_level,
        "barriers_financial": vector.barriers_financial,
        "barriers_technical": vector.barriers_technical,
        "barriers_direction": vector.barriers_direction,
    }

    # Prepare roles list
    roles_list = [
        {"id": r.id, "name": r.name, "description": r.description}
        for r in roles
    ]

    # Try LLM-powered recommendations
    llm_result = career_coach.analyze_and_recommend(
        veteran=veteran_profile,
        scct_vector=scct_vector,
        roles=roles_list,
    )

    if llm_result:
        # LLM succeeded - return LLM-generated recommendations
        return LLMResultsResponse(
            avery_intro=llm_result["avery_intro"],
            recommendations=[
                LLMRecommendation(**rec) for rec in llm_result["recommendations"]
            ],
            fallback_used=False,
        )

    # Fallback to algorithmic matching
    algorithmic_matches = get_top_role_matches(db, veteran_id, top_n=3)

    if not algorithmic_matches:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate recommendations. Please try again."
        )

    # Generate fallback recommendations
    fallback_result = career_coach.generate_fallback_recommendations(
        veteran=veteran_profile,
        scct_vector=scct_vector,
        role_matches=[m.model_dump() for m in algorithmic_matches],
    )

    return LLMResultsResponse(
        avery_intro=fallback_result["avery_intro"],
        recommendations=[
            LLMRecommendation(**rec) for rec in fallback_result["recommendations"]
        ],
        fallback_used=True,
    )
