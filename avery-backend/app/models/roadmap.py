from pydantic import BaseModel
from typing import List, Optional


class Certification(BaseModel):
    """A professional certification for a cybersecurity career path."""
    name: str
    provider: str  # CompTIA, EC-Council, ISC2, etc.
    level: str  # foundation, intermediate, advanced
    estimated_weeks: int
    cost_usd: int
    url: str
    description: str


class SkillTranslation(BaseModel):
    """Maps military experience to cybersecurity skills."""
    military_skill: str
    military_context: str  # "As an IT2, you..."
    cyber_skill: str
    transferability: int  # 0-100 percentage


class ActionStep(BaseModel):
    """A phase in the career transition timeline."""
    phase: str  # "Month 1-3", "Month 4-6"
    title: str
    description: str
    tasks: List[str]


class CareerRoadmap(BaseModel):
    """Complete career transition roadmap for a cybersecurity role."""
    role_id: int
    role_name: str
    quick_summary: str  # "Entry-ready in 3-6 months with Security+"
    estimated_months_to_entry: int
    certifications: List[Certification]
    skill_translations: List[SkillTranslation]
    action_steps: List[ActionStep]
    salary_entry: str  # "$65,000 - $85,000"
    salary_experienced: str  # "$95,000 - $130,000"
    job_outlook: str  # Brief market outlook


class RoadmapPreview(BaseModel):
    """Condensed roadmap info for results page cards."""
    role_id: int
    quick_summary: str
    top_certification: str
    estimated_months: int
    salary_entry: str
