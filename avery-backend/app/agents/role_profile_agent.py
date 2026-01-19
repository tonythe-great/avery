"""
Role Profile Agent

Purpose: Manage the cybersecurity role catalog, provide role details, and support comparison.

Inputs:
- role_id: Specific role to retrieve
- filters: Filtering criteria (salary range, experience level, etc.)

Outputs:
- role: CyberRole - Single role details
- roles: List[CyberRole] - Filtered list of roles
- role_comparison: RoleComparison - Side-by-side comparison

What it must NOT decide:
- Which role is "best" for a veteran (that's Scoring Agent's job)
- Whether a veteran "qualifies" for a role (that's Scoring Agent's job)
- Salary estimates (that's Salary Agent's job)
- Why a role fits (that's Explanations Agent's job)
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.cyber_role import CyberRole


class RoleProfileAgent:
    """Agent for managing cybersecurity role profiles."""

    def __init__(self, db: Session):
        self.db = db

    def get_role(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Return full details for a single role."""
        role = self.db.query(CyberRole).filter(CyberRole.id == role_id).first()

        if not role:
            return None

        return {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "min_years_preferred": role.min_years_preferred,
            "leadership_bonus": role.leadership_bonus,
            "trait_weights": {
                "openness": role.openness_weight,
                "conscientiousness": role.conscientiousness_weight,
                "extraversion": role.extraversion_weight,
                "agreeableness": role.agreeableness_weight,
                "stability": role.stability_weight,
            },
            "trait_ideals": {
                "openness": role.openness_ideal,
                "conscientiousness": role.conscientiousness_ideal,
                "extraversion": role.extraversion_ideal,
                "agreeableness": role.agreeableness_ideal,
                "stability": role.stability_ideal,
            },
        }

    def get_all_roles(self) -> List[Dict[str, Any]]:
        """Return all 10 cybersecurity roles."""
        roles = self.db.query(CyberRole).all()

        return [
            {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "min_years_preferred": role.min_years_preferred,
                "leadership_bonus": role.leadership_bonus,
            }
            for role in roles
        ]

    def get_role_requirements(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Return SCCT requirements, certs, and timeline for a role."""
        role = self.db.query(CyberRole).filter(CyberRole.id == role_id).first()

        if not role:
            return None

        # Map role characteristics to SCCT requirements
        # This is a simplified mapping; can be enhanced with additional role metadata
        return {
            "id": role.id,
            "name": role.name,
            "min_years": role.min_years_preferred,
            "leadership_required": role.leadership_bonus > 0,
            "se_requirements": {
                "technical": self._estimate_technical_requirement(role),
                "stress": role.stability_weight,
                "growth": role.openness_weight,
                "social": role.extraversion_weight,
            },
            "suggested_certs": self._get_suggested_certs(role.name),
            "timeline_months": self._estimate_timeline(role),
        }

    def compare_roles(self, role_ids: List[int]) -> Dict[str, Any]:
        """Generate side-by-side comparison of multiple roles."""
        roles = self.db.query(CyberRole).filter(CyberRole.id.in_(role_ids)).all()

        comparison = {
            "roles": [],
            "comparison_dimensions": [
                "min_years_preferred",
                "leadership_bonus",
                "openness_weight",
                "conscientiousness_weight",
                "extraversion_weight",
                "stability_weight",
            ],
        }

        for role in roles:
            comparison["roles"].append({
                "id": role.id,
                "name": role.name,
                "values": {
                    "min_years_preferred": role.min_years_preferred,
                    "leadership_bonus": role.leadership_bonus,
                    "openness_weight": role.openness_weight,
                    "conscientiousness_weight": role.conscientiousness_weight,
                    "extraversion_weight": role.extraversion_weight,
                    "stability_weight": role.stability_weight,
                },
            })

        return comparison

    def _estimate_technical_requirement(self, role: CyberRole) -> float:
        """Estimate technical requirement based on role traits."""
        # Higher openness and conscientiousness typically indicate more technical roles
        return (role.openness_weight + role.conscientiousness_weight) / 2

    def _estimate_timeline(self, role: CyberRole) -> int:
        """Estimate months to job-ready based on role requirements."""
        base_months = 3
        if role.min_years_preferred > 0:
            base_months += 3
        if role.leadership_bonus > 0:
            base_months += 6
        return base_months

    def _get_suggested_certs(self, role_name: str) -> List[str]:
        """Return suggested certifications for a role."""
        cert_map = {
            "Security Operations Center (SOC) Analyst": ["CompTIA Security+", "CySA+"],
            "Penetration Tester / Ethical Hacker": ["OSCP", "CEH", "CompTIA PenTest+"],
            "Incident Response Specialist": ["GCIH", "CompTIA Security+"],
            "Security Engineer": ["CISSP", "AWS Security Specialty"],
            "Cybersecurity Consultant": ["CISSP", "CISM"],
            "Threat Intelligence Analyst": ["CTIA", "GCTI"],
            "Security Awareness Training Specialist": ["CompTIA Security+"],
            "Chief Information Security Officer (CISO)": ["CISSP", "CISM", "CCISO"],
            "Digital Forensics Investigator": ["GCFE", "EnCE"],
            "Cloud Security Architect": ["CCSP", "AWS Security Specialty", "Azure Security Engineer"],
        }
        return cert_map.get(role_name, ["CompTIA Security+"])
