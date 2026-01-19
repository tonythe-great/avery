"""
JARVIS-Style Explanations Agent

Purpose: Generate natural language explanations in Avery's voice.
Transform data into emotionally resonant, Navy-authentic narratives.

Inputs:
- recommendation: RoleMatchScore - The match to explain
- veteran: Veteran - For personalization
- confidence_vector: ConfidenceVector - For understanding their profile
- salary_estimate: SalaryEstimate - For salary narrative

Outputs:
- primary_explanation: str - The main "why this role" narrative
- match_reasons: List[str] - Bullet-point reasons
- concerns: List[str] - Honest gaps or challenges
- next_steps: str - What to do next
- avery_voice_quote: str - JARVIS-style closing statement

What it must NOT decide:
- Match scores (that's Scoring Agent's job)
- Salary estimates (that's Salary Agent's job)
- Which role is best (that's Scoring Agent's job)
- Career strategy (that's the veteran's decision)

Voice Guidelines:
- Direct, confident, no hedging
- Navy-authentic language (watchstation, CO, liberty, etc.)
- Respectful of rank and service
- Never condescending
- Honest about challenges
"""
from typing import List, Dict, Any, Optional
from app.models.veteran import Veteran


# Rank titles for respectful address
SENIOR_RANKS = {
    "E-7": "Chief", "Chief Petty Officer": "Chief", "CPO": "Chief",
    "E-8": "Senior Chief", "Senior Chief Petty Officer": "Senior Chief", "SCPO": "Senior Chief",
    "E-9": "Master Chief", "Master Chief Petty Officer": "Master Chief", "MCPO": "Master Chief",
    "O-4": "Commander", "Lieutenant Commander": "Commander", "LCDR": "Commander",
    "O-5": "Commander", "CDR": "Commander",
    "O-6": "Captain", "CAPT": "Captain",
}


class JARVISExplanationsAgent:
    """Agent for generating JARVIS-style explanations in Avery's voice."""

    def generate_recommendation_narrative(
        self,
        recommendation: Dict[str, Any],
        veteran: Veteran,
        vector: Dict[str, float],
        salary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate full explanation package."""
        address = self._get_respectful_address(veteran)
        role_name = recommendation.get("role_name", "this role")
        match_score = recommendation.get("match_score", 75)

        primary_explanation = self._generate_primary_explanation(
            address, role_name, match_score, vector, veteran
        )
        match_reasons = self._generate_match_reasons(recommendation, vector)
        concerns = self._generate_concerns(recommendation, vector)
        next_steps = self._generate_next_steps(recommendation, vector)
        avery_quote = self._generate_avery_quote(address, role_name, veteran, vector)

        return {
            "primary_explanation": primary_explanation,
            "match_reasons": match_reasons,
            "concerns": concerns,
            "next_steps": next_steps,
            "avery_quote": avery_quote,
        }

    def generate_match_reasons(
        self,
        recommendation: Dict[str, Any],
        vector: Dict[str, float]
    ) -> List[str]:
        """Generate 3-5 specific match reasons."""
        return self._generate_match_reasons(recommendation, vector)

    def generate_concerns(
        self,
        recommendation: Dict[str, Any],
        vector: Dict[str, float]
    ) -> List[str]:
        """Generate honest concerns or gaps."""
        return self._generate_concerns(recommendation, vector)

    def generate_avery_quote(
        self,
        veteran: Veteran,
        role_name: str,
        vector: Dict[str, float]
    ) -> str:
        """Generate JARVIS-style closing statement."""
        address = self._get_respectful_address(veteran)
        return self._generate_avery_quote(address, role_name, veteran, vector)

    def _get_respectful_address(self, veteran: Veteran) -> str:
        """Get appropriate form of address based on rank."""
        # Check for senior ranks that get special titles
        if veteran.rank in SENIOR_RANKS:
            return SENIOR_RANKS[veteran.rank]

        # For officers O-1 to O-3, use their name
        if veteran.rank.startswith("O-") or veteran.rank in ["Ensign", "Lieutenant Junior Grade", "Lieutenant"]:
            return veteran.name.split()[0]  # First name

        # For junior enlisted, use first name
        return veteran.name.split()[0]

    def _generate_primary_explanation(
        self,
        address: str,
        role_name: str,
        match_score: float,
        vector: Dict[str, float],
        veteran: Veteran
    ) -> str:
        """Generate the main explanation narrative."""
        confidence_level = "strong" if match_score >= 80 else "solid" if match_score >= 70 else "good"

        explanation = f"{address}, based on your profile, I've identified {role_name} as a {confidence_level} match at {match_score:.0f}%. "

        # Add personalized insight based on strongest vector dimensions
        if vector.get("se_stress", 0) > 0.6:
            explanation += "Your ability to perform under pressure is a significant asset for this role. "
        elif vector.get("se_technical", 0) > 0.6:
            explanation += "Your technical problem-solving aptitude aligns well with this position. "
        elif vector.get("se_social", 0) > 0.6:
            explanation += "Your communication strengths are valued in this role. "
        elif vector.get("se_growth", 0) > 0.6:
            explanation += "Your learning agility positions you well for rapid advancement. "

        explanation += f"Your {veteran.years_of_service} years of service have prepared you for this transition."

        return explanation

    def _generate_match_reasons(
        self,
        recommendation: Dict[str, Any],
        vector: Dict[str, float]
    ) -> List[str]:
        """Generate specific match reasons."""
        reasons = []
        breakdown = recommendation.get("score_breakdown", {})

        # Self-efficacy alignment
        if breakdown.get("self_efficacy", 0) > 25:
            if vector.get("se_stress", 0) > 0.6:
                reasons.append("Your stress tolerance and composure under pressure directly translate to this role's demands")
            if vector.get("se_technical", 0) > 0.6:
                reasons.append("Your technical problem-solving approach matches the analytical requirements")
            if vector.get("se_growth", 0) > 0.6:
                reasons.append("Your self-directed learning style aligns with the continuous skill development required")

        # Experience bonus
        if breakdown.get("experience_bonus", 0) > 2:
            reasons.append(f"Your years of service exceed the typical experience threshold for this role")

        # Leadership bonus
        if breakdown.get("leadership_bonus", 0) > 2:
            reasons.append("Your leadership experience adds significant value to this career path")

        # Outcome alignment
        if breakdown.get("outcome_alignment", 0) > 20:
            if vector.get("oe_salary_priority", 0) > 0.6:
                reasons.append("This role offers strong earning potential aligned with your financial goals")
            if vector.get("oe_stability_priority", 0) > 0.6:
                reasons.append("This career path offers the stability and work-life balance you're seeking")
            if vector.get("oe_meaning_priority", 0) > 0.6:
                reasons.append("This role involves meaningful work protecting critical systems and data")

        # Ensure at least 2 reasons
        if len(reasons) < 2:
            reasons.append("Your military background provides a strong foundation for this transition")
            reasons.append("The core competencies required align with skills developed during your service")

        return reasons[:5]  # Cap at 5 reasons

    def _generate_concerns(
        self,
        recommendation: Dict[str, Any],
        vector: Dict[str, float]
    ) -> List[str]:
        """Generate honest concerns or gaps."""
        concerns = []

        # Technical barriers
        if vector.get("barriers_technical", 0) > 0.4:
            concerns.append(
                "You indicated limited technical background. This role may require additional training in "
                "scripting or system administration before applying to mid-level positions."
            )

        # Financial constraints
        if vector.get("barriers_financial", 0) > 0.5:
            concerns.append(
                "Given your timeline constraints, focus on roles with shorter paths to employment "
                "while building toward this position."
            )

        # Direction uncertainty
        if vector.get("barriers_direction", 0) > 0.5:
            concerns.append(
                "Consider connecting with professionals in this field to validate this path "
                "before committing to training investments."
            )

        # Low stress tolerance for high-stress role
        if vector.get("se_stress", 0) < 0.3 and "Incident Response" in recommendation.get("role_name", ""):
            concerns.append(
                "This role involves high-pressure crisis situations. Consider building stress "
                "management strategies or starting in a lower-intensity environment."
            )

        # Low social for high-social role
        if vector.get("se_social", 0) < 0.3 and any(
            x in recommendation.get("role_name", "")
            for x in ["Consultant", "Training", "CISO"]
        ):
            concerns.append(
                "This role requires significant stakeholder interaction. Consider developing "
                "presentation skills through practice or training."
            )

        return concerns

    def _generate_next_steps(
        self,
        recommendation: Dict[str, Any],
        vector: Dict[str, float]
    ) -> str:
        """Generate actionable next steps."""
        role_name = recommendation.get("role_name", "")

        # Determine priority based on barriers
        if vector.get("barriers_technical", 0) > 0.4:
            return (
                "Start with foundational training. CompTIA Security+ is the industry standard entry point. "
                "Many programs are available through the GI Bill. Once certified, entry-level positions "
                "will become accessible within 3-6 months."
            )
        elif vector.get("barriers_direction", 0) > 0.5:
            return (
                "Connect with professionals in this field. LinkedIn has active cybersecurity communities, "
                "and veteran-focused groups like VetSec can provide mentorship. A 30-minute conversation "
                "can validate this path before you commit."
            )
        elif vector.get("barriers_financial", 0) > 0.5:
            return (
                "Focus on quick-entry positions while building toward this role. Many organizations hire "
                "entry-level analysts with Security+ certification. Use VA education benefits to train "
                "while maintaining income."
            )
        else:
            return (
                f"You're well-positioned for this transition. Begin by researching {role_name} job postings "
                "to understand current requirements. Start networking with professionals in the field, "
                "and consider which certifications will accelerate your path."
            )

    def _generate_avery_quote(
        self,
        address: str,
        role_name: str,
        veteran: Veteran,
        vector: Dict[str, float]
    ) -> str:
        """Generate JARVIS-style closing statement."""
        years = veteran.years_of_service

        # Select quote based on profile
        if vector.get("se_stress", 0) > 0.6:
            return (
                f"{address}, your {years} years of watchstanding discipline maps directly to the "
                f"vigilance required in cybersecurity. You've already done harder."
            )
        elif vector.get("se_technical", 0) > 0.7:
            return (
                f"{address}, your technical aptitude is your advantage. The Navy taught you to "
                f"master complex systems under pressure. Cybersecurity is the next system to master."
            )
        elif vector.get("se_social", 0) > 0.7:
            return (
                f"{address}, your ability to communicate and lead will set you apart. "
                f"Technical skills can be learned. Your presence and influence cannot be taught."
            )
        elif vector.get("se_growth", 0) > 0.7:
            return (
                f"{address}, you learn fast and adapt faster. That's exactly what this field demands. "
                f"Your {years} years taught you discipline. Now apply it to mastering cyber."
            )
        else:
            return (
                f"{address}, you have the foundation. Your {years} years of service built it. "
                f"Now let's build the bridge to your next mission."
            )
