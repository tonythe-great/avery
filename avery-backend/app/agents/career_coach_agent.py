"""
Career Coach Agent

LLM-powered career recommendations with Avery's JARVIS-like voice.
Analyzes veteran profile, SCCT vector, and available roles to provide
personalized recommendations with Navy-authentic language.

Voice Guidelines:
- Calm, confident, direct tone with subtle dry wit
- Uses Navy-authentic language (watchstation, shipmate, squared away)
- Addresses veterans by rank-appropriate titles
- Honest about gaps but frames them constructively
- Weighs security clearance heavily (major differentiator in cyber)
- Translates rate skills to cyber roles (e.g., CTN → SOC analyst)
"""
import json
import logging
from typing import Dict, List, Optional, Any
from anthropic import Anthropic

from app.config import settings

logger = logging.getLogger(__name__)


# Rate to cyber skill translations
RATE_TRANSLATIONS = {
    "IT - Information Systems Technician": {
        "skills": ["network administration", "system administration", "troubleshooting"],
        "cyber_fit": "SOC Analyst, Security Engineer",
    },
    "CTN - Cryptologic Technician Networks": {
        "skills": ["network defense", "intrusion detection", "SIGINT", "cyber operations"],
        "cyber_fit": "SOC Analyst, Incident Response, Threat Intelligence",
    },
    "CTR - Cryptologic Technician Collection": {
        "skills": ["SIGINT collection", "signal analysis", "intelligence gathering"],
        "cyber_fit": "Threat Intelligence Analyst, Security Analyst",
    },
    "CTI - Cryptologic Technician Interpretive": {
        "skills": ["language analysis", "intelligence interpretation", "cryptanalysis"],
        "cyber_fit": "Threat Intelligence Analyst, Cybersecurity Consultant",
    },
    "IS - Intelligence Specialist": {
        "skills": ["intelligence analysis", "briefing", "strategic planning"],
        "cyber_fit": "Threat Intelligence Analyst, Security Consultant",
    },
    "ET - Electronics Technician": {
        "skills": ["electronics repair", "troubleshooting", "technical systems"],
        "cyber_fit": "Security Engineer, Digital Forensics",
    },
    "FC - Fire Controlman": {
        "skills": ["weapons systems", "precision operations", "technical maintenance"],
        "cyber_fit": "Security Engineer, Penetration Tester",
    },
    "OS - Operations Specialist": {
        "skills": ["radar operations", "tactical coordination", "situational awareness"],
        "cyber_fit": "SOC Analyst, Incident Response",
    },
}

# Clearance value for cyber roles
CLEARANCE_VALUE = {
    "none": 0,
    "secret": 1,
    "top_secret": 2,
    "ts_sci": 3,
}

# Rank titles for respectful address
SENIOR_RANKS = {
    "E-7 Chief Petty Officer": "Chief",
    "E-8 Senior Chief Petty Officer": "Senior Chief",
    "E-9 Master Chief Petty Officer": "Master Chief",
    "O-4 Lieutenant Commander": "Commander",
    "O-5 Commander": "Commander",
    "O-6 Captain": "Captain",
}


SYSTEM_PROMPT = """You are Avery, a JARVIS-like AI career coach for Navy veterans transitioning to cybersecurity careers.

Your voice and personality:
- Calm, confident, and direct with subtle dry wit
- Use Navy-authentic language naturally (watchstation, shipmate, squared away, liberty, CO)
- Address veterans appropriately based on their rank
- Be honest about challenges but frame them constructively
- Never condescending - these are accomplished professionals

Key factors in your analysis:
1. Security clearance is a MAJOR differentiator in cyber. TS/SCI holders have access to 40% more positions and often start $20-30K higher
2. Rate (Navy job) skills translate directly to cyber roles - highlight these connections
3. Years of service indicate discipline, leadership, and resilience
4. SCCT vector dimensions reveal confidence levels and priorities

You must return valid JSON in exactly this format:
{
  "avery_intro": "A 2-3 sentence personalized introduction using the veteran's appropriate title",
  "recommendations": [
    {
      "role_id": <integer>,
      "role_name": "<string>",
      "match_score": <float 0-100>,
      "primary_reason": "<1 sentence explaining the core match>",
      "fit_factors": ["<list of 2-3 specific advantages>"],
      "concerns": ["<list of 0-2 honest gaps or challenges>"],
      "avery_quote": "<A memorable 1-2 sentence quote in your voice connecting their service to this role>"
    }
  ]
}

Always provide exactly 3 recommendations ranked by fit. Be specific about how their Navy experience translates."""


class CareerCoachAgent:
    """LLM-powered career recommendations with Avery's JARVIS-like voice."""

    def __init__(self):
        self.client = None
        if settings.anthropic_api_key:
            self.client = Anthropic(api_key=settings.anthropic_api_key)

    def _get_respectful_address(self, rank: str, name: str) -> str:
        """Get appropriate form of address based on rank."""
        if rank in SENIOR_RANKS:
            return SENIOR_RANKS[rank]

        # For officers O-1 to O-3, use first name
        if any(x in rank for x in ["Ensign", "Lieutenant Junior Grade", "Lieutenant", "O-1", "O-2", "O-3"]):
            return name.split()[0]

        # For junior enlisted, use first name
        return name.split()[0]

    def _build_user_prompt(
        self,
        veteran: Dict[str, Any],
        scct_vector: Dict[str, float],
        roles: List[Dict[str, Any]],
    ) -> str:
        """Build the user prompt with all veteran context."""
        address = self._get_respectful_address(veteran.get("rank", ""), veteran.get("name", ""))

        # Get rate translation info
        rate = veteran.get("rating", "")
        rate_info = RATE_TRANSLATIONS.get(rate, {"skills": [], "cyber_fit": "Various cyber roles"})

        # Clearance value
        clearance = veteran.get("security_clearance", "none")
        clearance_level = CLEARANCE_VALUE.get(clearance, 0)
        clearance_label = {
            "none": "No active clearance",
            "secret": "Secret",
            "top_secret": "Top Secret",
            "ts_sci": "TS/SCI",
        }.get(clearance, "Unknown")

        prompt = f"""Analyze this veteran's profile and recommend the top 3 cybersecurity roles.

VETERAN PROFILE:
- Name: {veteran.get("name", "Unknown")} (address as "{address}")
- Rank: {veteran.get("rank", "Unknown")}
- Rate: {rate}
- Rate Skills: {", ".join(rate_info.get("skills", []))}
- Suggested Cyber Fit from Rate: {rate_info.get("cyber_fit", "Various")}
- Security Clearance: {clearance_label} (value: {clearance_level}/3)
- Years of Service: {veteran.get("years_of_service", 0)}

SCCT CAREER CONFIDENCE VECTOR:
- Technical Confidence: {scct_vector.get("se_technical", 0.5):.2f}
- Stress Tolerance: {scct_vector.get("se_stress", 0.5):.2f}
- Growth/Learning Aptitude: {scct_vector.get("se_growth", 0.5):.2f}
- Social/Communication Confidence: {scct_vector.get("se_social", 0.5):.2f}
- Salary Priority: {scct_vector.get("oe_salary_priority", 0.5):.2f}
- Stability Priority: {scct_vector.get("oe_stability_priority", 0.5):.2f}
- Meaning/Purpose Priority: {scct_vector.get("oe_meaning_priority", 0.5):.2f}
- Timeline Horizon: {scct_vector.get("goals_timeline", 0.5):.2f} (0=immediate, 1=long-term)
- Ambition Level: {scct_vector.get("goals_level", 0.5):.2f} (0=entry, 1=executive)
- Financial Constraints: {scct_vector.get("barriers_financial", 0.5):.2f}
- Technical Training Needed: {scct_vector.get("barriers_technical", 0.5):.2f}
- Direction Uncertainty: {scct_vector.get("barriers_direction", 0.5):.2f}

AVAILABLE CYBER ROLES (select from these):
"""
        for role in roles:
            prompt += f"- ID {role['id']}: {role['name']} - {role.get('description', '')[:100]}...\n"

        prompt += """
IMPORTANT CONSIDERATIONS:
1. Security clearance is a major differentiator - weight it heavily
2. Connect their rate skills to specific role requirements
3. Consider their SCCT profile for role fit (stress tolerance for IR, social confidence for consulting, etc.)
4. Be honest about any gaps but frame constructively
5. Use Navy-authentic language in avery_intro and avery_quote

Return your analysis as valid JSON."""

        return prompt

    def analyze_and_recommend(
        self,
        veteran: Dict[str, Any],
        scct_vector: Dict[str, float],
        roles: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze veteran profile and return LLM-powered recommendations.

        Args:
            veteran: Dict with name, rank, rate, security_clearance, years_of_service
            scct_vector: 12-dimension confidence vector from SCCT assessment
            roles: List of available cyber roles with id, name, description

        Returns:
            Dict with avery_intro and 3 recommendations, or None if LLM unavailable
        """
        if not self.client:
            logger.warning("Anthropic client not configured - falling back to algorithmic matching")
            return None

        try:
            user_prompt = self._build_user_prompt(veteran, scct_vector, roles)

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                system=SYSTEM_PROMPT,
            )

            # Extract the response text
            response_text = response.content[0].text

            # Parse JSON from response
            # Handle potential markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())

            # Validate structure
            if "avery_intro" not in result or "recommendations" not in result:
                logger.error("Invalid LLM response structure")
                return None

            if len(result["recommendations"]) != 3:
                logger.warning(f"Expected 3 recommendations, got {len(result['recommendations'])}")

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            return None

    def generate_fallback_recommendations(
        self,
        veteran: Dict[str, Any],
        scct_vector: Dict[str, float],
        role_matches: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate recommendations without LLM using algorithmic matching.

        Used as fallback when LLM is unavailable or fails.
        """
        address = self._get_respectful_address(
            veteran.get("rank", ""),
            veteran.get("name", "Unknown")
        )
        years = veteran.get("years_of_service", 0)
        clearance = veteran.get("security_clearance", "none")

        # Build intro based on profile
        if clearance in ["top_secret", "ts_sci"]:
            intro = f"{address}, your {clearance.replace('_', '/').upper()} clearance and {years} years of service put you in a strong position for cyber roles. Let me show you what matches your profile."
        else:
            intro = f"{address}, with {years} years of Navy experience, you've built a foundation that translates well to cybersecurity. Here are the roles that match your profile."

        recommendations = []
        for match in role_matches[:3]:
            role = match.get("role", {})
            recommendations.append({
                "role_id": role.get("id", 0),
                "role_name": role.get("name", "Unknown Role"),
                "match_score": match.get("match_percentage", 75),
                "primary_reason": match.get("match_reasons", ["General compatibility"])[0] if match.get("match_reasons") else "Your military background provides a strong foundation.",
                "fit_factors": match.get("match_reasons", ["Military discipline", "Security mindset"])[:3],
                "concerns": [],
                "avery_quote": f"Your {years} years of service built the discipline this role demands.",
            })

        return {
            "avery_intro": intro,
            "recommendations": recommendations,
        }
