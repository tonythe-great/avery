"""
Matching service for calculating cybersecurity role recommendations.
Uses Big Five personality traits and military experience to determine best fits.
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
from app.models.veteran import Veteran
from app.models.assessment import Question, AssessmentResponse
from app.models.cyber_role import CyberRole, CyberRoleResponse, RoleMatch


# Rank hierarchy for leadership bonus calculation
RANK_LEVELS = {
    # Enlisted
    "E-1": 1, "E-2": 2, "E-3": 3, "E-4": 4, "E-5": 5, "E-6": 6, "E-7": 7, "E-8": 8, "E-9": 9,
    # Warrant Officers
    "W-1": 10, "W-2": 11, "W-3": 12, "W-4": 13, "W-5": 14,
    # Officers
    "O-1": 15, "O-2": 16, "O-3": 17, "O-4": 18, "O-5": 19, "O-6": 20, "O-7": 21, "O-8": 22, "O-9": 23, "O-10": 24,
    # Navy-specific ranks (alternate names)
    "Seaman Recruit": 1, "Seaman Apprentice": 2, "Seaman": 3, "Petty Officer Third Class": 4,
    "Petty Officer Second Class": 5, "Petty Officer First Class": 6, "Chief Petty Officer": 7,
    "Senior Chief Petty Officer": 8, "Master Chief Petty Officer": 9,
    "Ensign": 15, "Lieutenant Junior Grade": 16, "Lieutenant": 17, "Lieutenant Commander": 18,
    "Commander": 19, "Captain": 20, "Rear Admiral": 21, "Vice Admiral": 22, "Admiral": 23,
}


def calculate_trait_scores(db: Session, veteran_id: int) -> Dict[str, float]:
    """
    Calculate average scores for each Big Five trait based on assessment responses.
    Returns a dict like {"openness": 4.2, "conscientiousness": 3.8, ...}
    """
    # Get all responses for this veteran with their associated questions
    responses = (
        db.query(AssessmentResponse, Question)
        .join(Question, AssessmentResponse.question_id == Question.id)
        .filter(AssessmentResponse.veteran_id == veteran_id)
        .all()
    )
    
    if not responses:
        return {}
    
    # Group scores by trait
    trait_scores: Dict[str, List[int]] = {}
    for response, question in responses:
        trait = question.trait
        if trait not in trait_scores:
            trait_scores[trait] = []
        trait_scores[trait].append(response.answer_value)
    
    # Calculate averages
    return {trait: sum(scores) / len(scores) for trait, scores in trait_scores.items()}


def get_rank_level(rank: str) -> int:
    """Get numerical level for a military rank. Higher = more senior."""
    # Try exact match first
    if rank in RANK_LEVELS:
        return RANK_LEVELS[rank]
    
    # Try case-insensitive match
    rank_lower = rank.lower()
    for key, value in RANK_LEVELS.items():
        if key.lower() == rank_lower:
            return value
    
    # Try partial match (e.g., "E5" matches "E-5")
    rank_normalized = rank.upper().replace("-", "").replace(" ", "")
    for key, value in RANK_LEVELS.items():
        if key.replace("-", "").replace(" ", "").upper() == rank_normalized:
            return value
    
    return 5  # Default to mid-level if unknown


def calculate_role_match(
    trait_scores: Dict[str, float],
    veteran: Veteran,
    role: CyberRole
) -> Tuple[float, List[str]]:
    """
    Calculate how well a veteran matches a cybersecurity role.
    Returns (match_percentage, list_of_reasons).
    """
    if not trait_scores:
        return 0.0, ["Assessment not completed"]
    
    match_reasons = []
    total_weight = 0.0
    weighted_score = 0.0
    
    # Define trait mappings
    traits = [
        ("openness", role.openness_weight, role.openness_ideal),
        ("conscientiousness", role.conscientiousness_weight, role.conscientiousness_ideal),
        ("extraversion", role.extraversion_weight, role.extraversion_ideal),
        ("agreeableness", role.agreeableness_weight, role.agreeableness_ideal),
        ("stability", role.stability_weight, role.stability_ideal),
    ]
    
    for trait_name, weight, ideal in traits:
        if trait_name not in trait_scores:
            continue
            
        actual = trait_scores[trait_name]
        # Calculate how close the actual score is to ideal (max distance is 4)
        distance = abs(actual - ideal)
        trait_match = max(0, 1 - (distance / 4))  # 0 to 1 scale
        
        weighted_score += trait_match * weight
        total_weight += weight
        
        # Add reason if it's a strong match (within 0.5 of ideal) and weight is significant
        if distance <= 0.75 and weight >= 0.6:
            trait_label = trait_name.replace("_", " ").title()
            match_reasons.append(f"Strong {trait_label.lower()} alignment")
    
    # Calculate base percentage
    if total_weight > 0:
        base_percentage = (weighted_score / total_weight) * 100
    else:
        base_percentage = 50.0
    
    # Apply experience bonus
    experience_bonus = 0.0
    if veteran.years_of_service >= role.min_years_preferred:
        years_over = veteran.years_of_service - role.min_years_preferred
        experience_bonus = min(years_over * 0.5, 5.0)  # Max 5% bonus
        if experience_bonus > 2:
            match_reasons.append(f"Strong experience match ({veteran.years_of_service} years)")
    
    # Apply leadership bonus based on rank
    leadership_bonus = 0.0
    if role.leadership_bonus > 0:
        rank_level = get_rank_level(veteran.rank)
        if rank_level >= 7:  # E-7 and above or O-1 and above
            leadership_bonus = role.leadership_bonus * min(rank_level / 10, 1.0) * 10  # Scale up to 10%
            if leadership_bonus > 3:
                match_reasons.append("Leadership experience valued")
    
    # Calculate final percentage (cap at 99%)
    final_percentage = min(base_percentage + experience_bonus + leadership_bonus, 99.0)
    
    return round(final_percentage, 1), match_reasons


def get_top_role_matches(
    db: Session,
    veteran_id: int,
    top_n: int = 3
) -> List[RoleMatch]:
    """
    Get the top N cybersecurity role matches for a veteran.
    """
    # Get veteran
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        return []
    
    # Calculate trait scores
    trait_scores = calculate_trait_scores(db, veteran_id)
    if not trait_scores:
        return []
    
    # Get all roles and calculate matches
    roles = db.query(CyberRole).all()
    role_matches = []
    
    for role in roles:
        percentage, reasons = calculate_role_match(trait_scores, veteran, role)
        role_matches.append(
            RoleMatch(
                role=CyberRoleResponse(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                ),
                match_percentage=percentage,
                match_reasons=reasons if reasons else ["General compatibility"],
            )
        )
    
    # Sort by match percentage descending and return top N
    role_matches.sort(key=lambda x: x.match_percentage, reverse=True)
    return role_matches[:top_n]
