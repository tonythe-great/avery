"""
Roadmap service for generating career transition roadmaps.
Provides static roadmap data with optional personalization based on veteran profile.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.roadmap import (
    CareerRoadmap, RoadmapPreview, Certification, SkillTranslation, ActionStep
)
from app.models.veteran import Veteran
from app.models.cyber_role import CyberRole
from app.roadmap_data import get_roadmap, get_all_roadmaps


def get_roadmap_for_role(role_id: int) -> Optional[CareerRoadmap]:
    """
    Get the career roadmap for a specific role.
    Returns None if role_id is not found.
    """
    roadmap_data = get_roadmap(role_id)
    if not roadmap_data:
        return None

    return CareerRoadmap(
        role_id=role_id,
        role_name=roadmap_data["role_name"],
        quick_summary=roadmap_data["quick_summary"],
        estimated_months_to_entry=roadmap_data["estimated_months_to_entry"],
        certifications=[Certification(**cert) for cert in roadmap_data["certifications"]],
        skill_translations=[SkillTranslation(**skill) for skill in roadmap_data["skill_translations"]],
        action_steps=[ActionStep(**step) for step in roadmap_data["action_steps"]],
        salary_entry=roadmap_data["salary_entry"],
        salary_experienced=roadmap_data["salary_experienced"],
        job_outlook=roadmap_data["job_outlook"]
    )


def get_roadmap_preview(role_id: int) -> Optional[RoadmapPreview]:
    """
    Get a condensed preview of the roadmap for results page cards.
    """
    roadmap_data = get_roadmap(role_id)
    if not roadmap_data:
        return None

    # Get the first (most important) certification
    top_cert = roadmap_data["certifications"][0]["name"] if roadmap_data["certifications"] else "Security+"

    return RoadmapPreview(
        role_id=role_id,
        quick_summary=roadmap_data["quick_summary"],
        top_certification=top_cert,
        estimated_months=roadmap_data["estimated_months_to_entry"],
        salary_entry=roadmap_data["salary_entry"]
    )


def get_personalized_roadmap(
    db: Session,
    veteran_id: int,
    role_id: int
) -> Optional[CareerRoadmap]:
    """
    Get a personalized career roadmap based on veteran's profile.
    Personalizes skill translations based on veteran's rating/MOS.
    """
    # Get base roadmap
    roadmap = get_roadmap_for_role(role_id)
    if not roadmap:
        return None

    # Get veteran for personalization
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        return roadmap  # Return base roadmap if veteran not found

    # Personalize skill translations with veteran's context
    personalized_translations = []
    for skill in roadmap.skill_translations:
        # Update military context with veteran's specific info if available
        context = skill.military_context
        if veteran.rating:
            context = context.replace("your", f"As a {veteran.rating}, your")
        elif veteran.rank:
            context = context.replace("Your", f"As a {veteran.rank}, your")

        personalized_translations.append(
            SkillTranslation(
                military_skill=skill.military_skill,
                military_context=context,
                cyber_skill=skill.cyber_skill,
                transferability=skill.transferability
            )
        )

    # Return personalized roadmap
    return CareerRoadmap(
        role_id=roadmap.role_id,
        role_name=roadmap.role_name,
        quick_summary=roadmap.quick_summary,
        estimated_months_to_entry=roadmap.estimated_months_to_entry,
        certifications=roadmap.certifications,
        skill_translations=personalized_translations,
        action_steps=roadmap.action_steps,
        salary_entry=roadmap.salary_entry,
        salary_experienced=roadmap.salary_experienced,
        job_outlook=roadmap.job_outlook
    )


def get_all_roadmap_previews() -> list[RoadmapPreview]:
    """
    Get previews for all available roadmaps.
    """
    all_roadmaps = get_all_roadmaps()
    previews = []

    for role_id in all_roadmaps.keys():
        preview = get_roadmap_preview(role_id)
        if preview:
            previews.append(preview)

    return previews
