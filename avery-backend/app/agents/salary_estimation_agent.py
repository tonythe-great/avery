"""
Salary Estimation Agent

Purpose: Estimate salary ranges based on role, veteran profile, and (future) location.
Provide transparent sourcing.

Inputs:
- role_id: The role to estimate
- veteran: Veteran - For civilian level calculation
- location: Optional[str] - Metro area (future)

Outputs:
- salary_estimate: SalaryEstimate - Range with p10/p25/p50/p75/p90
- estimate_reasoning: str - Why this range
- data_sources: List[str] - Where the data came from

What it must NOT decide:
- Role recommendations (that's Scoring Agent's job)
- Career advice (that's Explanations Agent's job)
- Whether salary is "good enough" (that's veteran's decision)
- Future salary trajectory (post-MVP feature)
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.models.scct import SalaryBand
from app.models.veteran import Veteran
from app.models.cyber_role import CyberRole


# Rank to civilian level mapping
RANK_LEVELS = {
    "E-1": 1, "E-2": 2, "E-3": 3, "E-4": 4, "E-5": 5, "E-6": 6,
    "E-7": 7, "E-8": 8, "E-9": 9,
    "O-1": 15, "O-2": 16, "O-3": 17, "O-4": 18, "O-5": 19, "O-6": 20,
    "O-7": 21, "O-8": 22, "O-9": 23, "O-10": 24,
    "W-1": 10, "W-2": 11, "W-3": 12, "W-4": 13, "W-5": 14,
    # Navy-specific ranks
    "Seaman Recruit": 1, "Seaman Apprentice": 2, "Seaman": 3,
    "Petty Officer Third Class": 4, "Petty Officer Second Class": 5, "Petty Officer First Class": 6,
    "Chief Petty Officer": 7, "Senior Chief Petty Officer": 8, "Master Chief Petty Officer": 9,
    "Ensign": 15, "Lieutenant Junior Grade": 16, "Lieutenant": 17,
    "Lieutenant Commander": 18, "Commander": 19, "Captain": 20,
}

RANK_TO_CIVILIAN_LEVEL = {
    1: "entry", 2: "entry", 3: "entry",
    4: "mid", 5: "mid", 6: "mid",
    7: "senior", 8: "senior", 9: "lead",
    10: "mid", 11: "mid", 12: "senior", 13: "senior", 14: "lead",
    15: "mid", 16: "senior", 17: "senior",
    18: "lead", 19: "director", 20: "director",
    21: "director", 22: "director", 23: "director", 24: "director",
}


class SalaryEstimationAgent:
    """Agent for estimating salary ranges based on role and veteran profile."""

    def __init__(self, db: Session):
        self.db = db

    def estimate_salary(
        self,
        role_id: int,
        veteran: Veteran,
        location: str = "national"
    ) -> Dict[str, Any]:
        """
        Return salary range estimate with confidence.
        """
        # Get role
        role = self.db.query(CyberRole).filter(CyberRole.id == role_id).first()
        if not role:
            return self._default_estimate()

        # Get civilian level from rank
        civilian_level = self.get_civilian_level(veteran.rank)

        # Get salary band for role + level
        salary_band = self._get_salary_band(role_id, civilian_level)

        if not salary_band:
            # Fallback to closest available level
            salary_band = self._get_fallback_salary_band(role_id)

        if not salary_band:
            return self._default_estimate()

        # Position within band based on years of service
        low, mid, high = self._calculate_position(salary_band, veteran.years_of_service)

        # Apply location adjustment (future feature)
        adjustment = self._get_metro_adjustment(location)
        low = int(low * adjustment)
        mid = int(mid * adjustment)
        high = int(high * adjustment)

        return {
            "low": low,
            "mid": mid,
            "high": high,
            "confidence": 0.85,
            "source": salary_band.data_source,
            "disclaimer": "Estimates based on industry data. Actual offers may vary.",
            "reasoning": self._explain_estimate(civilian_level, veteran.years_of_service, role.name),
        }

    def get_civilian_level(self, rank: str) -> str:
        """Map military rank to civilian experience level."""
        rank_level = RANK_LEVELS.get(rank, 5)
        return RANK_TO_CIVILIAN_LEVEL.get(rank_level, "mid")

    def get_salary_band(self, role_id: int, level: str) -> Optional[Dict[str, Any]]:
        """Retrieve raw salary band data for role + level."""
        band = self._get_salary_band(role_id, level)
        if not band:
            return None

        return {
            "experience_level": band.experience_level,
            "p10": band.p10,
            "p25": band.p25,
            "p50": band.p50,
            "p75": band.p75,
            "p90": band.p90,
            "data_source": band.data_source,
        }

    def explain_estimate(self, estimate: Dict[str, Any], veteran: Veteran) -> str:
        """Return human-readable explanation of salary calculation."""
        civilian_level = self.get_civilian_level(veteran.rank)
        years = veteran.years_of_service

        explanation = f"{veteran.rank} with {years} years maps to {civilian_level}-level positions. "

        if years < 5:
            explanation += "Early career positioning (p25-p50 range)."
        elif years < 10:
            explanation += "Mid-career positioning (p50-p75 range)."
        elif years < 15:
            explanation += "Experienced positioning (p75 range)."
        else:
            explanation += "Senior positioning (p75-p90 range)."

        return explanation

    def get_all_salary_bands_for_role(self, role_id: int) -> List[Dict[str, Any]]:
        """Get all salary bands for a role across experience levels."""
        bands = self.db.query(SalaryBand).filter(
            SalaryBand.role_id == role_id
        ).order_by(SalaryBand.experience_level).all()

        return [
            {
                "experience_level": band.experience_level,
                "p10": band.p10,
                "p25": band.p25,
                "p50": band.p50,
                "p75": band.p75,
                "p90": band.p90,
            }
            for band in bands
        ]

    def _get_salary_band(self, role_id: int, level: str) -> Optional[SalaryBand]:
        """Get salary band for specific role and level."""
        return self.db.query(SalaryBand).filter(
            SalaryBand.role_id == role_id,
            SalaryBand.experience_level == level
        ).first()

    def _get_fallback_salary_band(self, role_id: int) -> Optional[SalaryBand]:
        """Get any salary band for the role as fallback."""
        return self.db.query(SalaryBand).filter(
            SalaryBand.role_id == role_id
        ).first()

    def _calculate_position(self, band: SalaryBand, years_of_service: int) -> tuple:
        """Determine position within salary band based on years."""
        if years_of_service < 5:
            return band.p10, band.p25, band.p50
        elif years_of_service < 10:
            return band.p25, band.p50, band.p75
        elif years_of_service < 15:
            return band.p50, band.p75, band.p90
        else:
            return band.p75, band.p75, band.p90

    def _get_metro_adjustment(self, location: str) -> float:
        """Get location-based salary adjustment (future feature)."""
        # National average = 1.0
        # Future: Add metro-specific adjustments
        adjustments = {
            "national": 1.0,
            "san_francisco": 1.4,
            "new_york": 1.3,
            "washington_dc": 1.25,
            "seattle": 1.2,
            "austin": 1.1,
            "denver": 1.05,
        }
        return adjustments.get(location.lower().replace(" ", "_"), 1.0)

    def _explain_estimate(self, level: str, years: int, role_name: str) -> str:
        """Generate explanation for salary estimate."""
        return (
            f"Based on {level}-level positioning for {role_name} "
            f"with {years} years of military experience. "
            f"Industry data reflects 2024-2025 compensation trends."
        )

    def _default_estimate(self) -> Dict[str, Any]:
        """Return default estimate when no data available."""
        return {
            "low": 65000,
            "mid": 85000,
            "high": 110000,
            "confidence": 0.5,
            "source": "industry_average",
            "disclaimer": "Estimates based on industry averages. Specific role data not available.",
            "reasoning": "Using cybersecurity industry average due to limited role-specific data.",
        }
