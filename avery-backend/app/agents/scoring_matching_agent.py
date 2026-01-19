"""
Scoring & Matching Agent

Purpose: Compute match scores between a veteran's confidence vector and all role profiles.
Rank and filter results.

Inputs:
- confidence_vector: ConfidenceVector - Veteran's computed SCCT vector
- veteran: Veteran - For experience/rank bonuses
- roles: List[CyberRole] - Roles to score against

Outputs:
- scored_roles: List[RoleMatchScore] - All roles with scores and breakdowns
- top_matches: List[RoleMatchScore] - Top 3 recommendations
- score_explanation: Dict - Component-by-component breakdown

What it must NOT decide:
- Salary estimates (that's Salary Agent's job)
- Natural language explanations (that's Explanations Agent's job)
- Whether to change role profiles (that's admin function)
- What certifications to recommend (that's a separate pathway agent, post-MVP)
"""
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.scct import ConfidenceVector, SCCTResponse, SCCTOption
from app.models.veteran import Veteran
from app.models.cyber_role import CyberRole


# Rank level mapping for leadership bonus calculation
RANK_LEVELS = {
    # Navy Enlisted
    "E-1": 1, "Seaman Recruit": 1, "SR": 1,
    "E-2": 2, "Seaman Apprentice": 2, "SA": 2,
    "E-3": 3, "Seaman": 3, "SN": 3,
    "E-4": 4, "Petty Officer Third Class": 4, "PO3": 4,
    "E-5": 5, "Petty Officer Second Class": 5, "PO2": 5,
    "E-6": 6, "Petty Officer First Class": 6, "PO1": 6,
    "E-7": 7, "Chief Petty Officer": 7, "CPO": 7,
    "E-8": 8, "Senior Chief Petty Officer": 8, "SCPO": 8,
    "E-9": 9, "Master Chief Petty Officer": 9, "MCPO": 9,
    # Navy Officers
    "O-1": 15, "Ensign": 15, "ENS": 15,
    "O-2": 16, "Lieutenant Junior Grade": 16, "LTJG": 16,
    "O-3": 17, "Lieutenant": 17, "LT": 17,
    "O-4": 18, "Lieutenant Commander": 18, "LCDR": 18,
    "O-5": 19, "Commander": 19, "CDR": 19,
    "O-6": 20, "Captain": 20, "CAPT": 20,
    # Flag Officers
    "O-7": 21, "Rear Admiral (Lower Half)": 21, "RDML": 21,
    "O-8": 22, "Rear Admiral": 22, "RADM": 22,
    "O-9": 23, "Vice Admiral": 23, "VADM": 23,
    "O-10": 24, "Admiral": 24, "ADM": 24,
    # Warrant Officers
    "W-1": 10, "Warrant Officer 1": 10, "WO1": 10,
    "W-2": 11, "Chief Warrant Officer 2": 11, "CWO2": 11,
    "W-3": 12, "Chief Warrant Officer 3": 12, "CWO3": 12,
    "W-4": 13, "Chief Warrant Officer 4": 13, "CWO4": 13,
    "W-5": 14, "Chief Warrant Officer 5": 14, "CWO5": 14,
}

# Civilian level mapping based on rank
RANK_TO_CIVILIAN_LEVEL = {
    1: "entry", 2: "entry", 3: "entry",          # E-1 to E-3 -> Entry
    4: "mid", 5: "mid", 6: "mid",                # E-4 to E-6 -> Mid
    7: "senior", 8: "senior", 9: "lead",         # E-7 to E-9 -> Senior/Lead
    10: "mid", 11: "mid", 12: "senior",          # W-1 to W-3 -> Mid/Senior
    13: "senior", 14: "lead",                    # W-4 to W-5 -> Senior/Lead
    15: "mid", 16: "senior", 17: "senior",       # O-1 to O-3 -> Mid/Senior
    18: "lead", 19: "director", 20: "director",  # O-4 to O-6 -> Lead/Director
    21: "director", 22: "director",              # O-7 to O-8 -> Director
    23: "director", 24: "director",              # O-9 to O-10 -> Director
}


class ScoringMatchingAgent:
    """Agent for computing match scores between veterans and roles."""

    def __init__(self, db: Session):
        self.db = db

    def compute_vector(self, veteran_id: int) -> Dict[str, float]:
        """Transform SCCT responses into confidence vector."""
        responses = self.db.query(SCCTResponse).filter(
            SCCTResponse.veteran_id == veteran_id
        ).all()

        if not responses:
            raise ValueError(f"No SCCT responses found for veteran {veteran_id}")

        # Initialize accumulator
        vector = {
            "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
            "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
            "goals_timeline": 0.0, "goals_level": 0.0,
            "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
        }

        for response in responses:
            option = self.db.query(SCCTOption).filter(SCCTOption.id == response.option_id).first()
            if option:
                vector["se_technical"] += option.se_technical
                vector["se_stress"] += option.se_stress
                vector["se_growth"] += option.se_growth
                vector["se_social"] += option.se_social
                vector["oe_salary_priority"] += option.oe_salary_priority
                vector["oe_stability_priority"] += option.oe_stability_priority
                vector["oe_meaning_priority"] += option.oe_meaning_priority
                vector["goals_timeline"] += option.goals_timeline
                vector["goals_level"] += option.goals_level
                vector["barriers_financial"] += option.barriers_financial
                vector["barriers_technical"] += option.barriers_technical
                vector["barriers_direction"] += option.barriers_direction

        # Normalize to 0-1 range
        for key in vector:
            vector[key] = self._normalize(vector[key])

        return vector

    def score_all_roles(self, vector: Dict[str, float], veteran: Veteran) -> List[Dict[str, Any]]:
        """Score veteran against all roles, sorted by match score."""
        roles = self.db.query(CyberRole).all()

        scored_roles = []
        for role in roles:
            score, breakdown = self._calculate_role_match(vector, veteran, role)
            scored_roles.append({
                "role_id": role.id,
                "role_name": role.name,
                "role_description": role.description,
                "match_score": score,
                "score_breakdown": breakdown,
            })

        # Sort by match score descending
        scored_roles.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_roles

    def get_top_matches(self, vector: Dict[str, float], veteran: Veteran, n: int = 3) -> List[Dict[str, Any]]:
        """Return top N matches with full breakdowns."""
        all_matches = self.score_all_roles(vector, veteran)
        return all_matches[:n]

    def explain_score(self, score_breakdown: Dict[str, float]) -> str:
        """Return human-readable explanation of why this score."""
        components = []

        if score_breakdown.get("self_efficacy", 0) > 20:
            components.append("Strong self-efficacy alignment")
        if score_breakdown.get("outcome_alignment", 0) > 15:
            components.append("Good outcome expectations match")
        if score_breakdown.get("goals_feasibility", 0) > 10:
            components.append("Feasible career goals alignment")
        if score_breakdown.get("experience_bonus", 0) > 2:
            components.append(f"Experience bonus applied (+{score_breakdown['experience_bonus']:.1f}%)")
        if score_breakdown.get("leadership_bonus", 0) > 2:
            components.append(f"Leadership bonus applied (+{score_breakdown['leadership_bonus']:.1f}%)")

        return "; ".join(components) if components else "Standard match based on profile"

    def get_rank_level(self, rank: str) -> int:
        """Map military rank to numeric level."""
        return RANK_LEVELS.get(rank, 5)  # Default to mid-level if unknown

    def get_civilian_level(self, rank: str) -> str:
        """Map military rank to civilian experience level."""
        rank_level = self.get_rank_level(rank)
        return RANK_TO_CIVILIAN_LEVEL.get(rank_level, "mid")

    def _calculate_role_match(self, vector: Dict[str, float], veteran: Veteran, role: CyberRole) -> Tuple[float, Dict[str, float]]:
        """Calculate match score for a single role."""

        # COMPONENT 1: Self-Efficacy Alignment (40% of total)
        # Map role traits to SCCT self-efficacy dimensions
        se_technical_required = (role.openness_weight + role.conscientiousness_weight) / 2
        se_stress_required = role.stability_weight
        se_growth_required = role.openness_weight
        se_social_required = role.extraversion_weight

        se_score = (
            (1 - abs(vector["se_technical"] - se_technical_required)) * 0.30 +
            (1 - abs(vector["se_stress"] - se_stress_required)) * 0.30 +
            (1 - abs(vector["se_growth"] - se_growth_required)) * 0.20 +
            (1 - abs(vector["se_social"] - se_social_required)) * 0.20
        )

        # COMPONENT 2: Outcome Alignment (30% of total)
        # Estimate role characteristics
        salary_potential = 0.7 if role.min_years_preferred >= 4 else 0.5
        stability_score = 0.8 if role.min_years_preferred <= 2 else 0.6
        meaning_score = 0.7  # All cybersecurity roles have meaning

        total_priority = (
            vector["oe_salary_priority"] +
            vector["oe_stability_priority"] +
            vector["oe_meaning_priority"] + 0.001
        )

        oe_score = (
            vector["oe_salary_priority"] * salary_potential +
            vector["oe_stability_priority"] * stability_score +
            vector["oe_meaning_priority"] * meaning_score
        ) / total_priority

        # COMPONENT 3: Goals Feasibility (20% of total)
        timeline_fit = 1.0 if vector["goals_timeline"] >= 0.3 or role.min_years_preferred <= 2 else 0.5
        level_fit = 1.0 if vector["goals_level"] <= 0.6 or role.leadership_bonus > 0 else 0.7
        goals_score = (timeline_fit + level_fit) / 2

        # COMPONENT 4: Barrier Compatibility (10% of total)
        barrier_score = (
            (1 - vector["barriers_financial"]) * 0.4 +
            (1 - vector["barriers_technical"]) * 0.4 +
            (1 - vector["barriers_direction"]) * 0.2
        )

        # WEIGHTED TOTAL
        base_score = (
            se_score * 0.40 +
            oe_score * 0.30 +
            goals_score * 0.20 +
            barrier_score * 0.10
        ) * 100

        # BONUSES
        experience_bonus = self._calculate_experience_bonus(
            veteran.years_of_service, role.min_years_preferred
        )
        leadership_bonus = self._calculate_leadership_bonus(
            veteran.rank, role.leadership_bonus
        )

        final_score = min(base_score + experience_bonus + leadership_bonus, 99.0)

        breakdown = {
            "self_efficacy": se_score * 40,
            "outcome_alignment": oe_score * 30,
            "goals_feasibility": goals_score * 20,
            "barrier_compatibility": barrier_score * 10,
            "experience_bonus": experience_bonus,
            "leadership_bonus": leadership_bonus,
            "base_score": base_score,
            "final_score": final_score,
        }

        return final_score, breakdown

    def _calculate_experience_bonus(self, years_of_service: int, min_years_preferred: int) -> float:
        """Calculate experience bonus (max 5%)."""
        if years_of_service >= min_years_preferred:
            years_over = years_of_service - min_years_preferred
            return min(years_over * 0.5, 5.0)
        return 0.0

    def _calculate_leadership_bonus(self, rank: str, role_leadership_bonus: float) -> float:
        """Calculate leadership bonus based on rank level (max 10%)."""
        rank_level = self.get_rank_level(rank)

        # E-7+ or O-1+ qualifies for leadership bonus
        if rank_level >= 7:
            multiplier = min(rank_level / 10, 1.0)
            return role_leadership_bonus * multiplier * 10
        return 0.0

    def _normalize(self, value: float, min_val: float = -2.0, max_val: float = 2.0) -> float:
        """Normalize value to 0-1 range."""
        clamped = max(min_val, min(max_val, value))
        return (clamped - min_val) / (max_val - min_val)
