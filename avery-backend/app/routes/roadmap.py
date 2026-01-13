from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.roadmap import CareerRoadmap, RoadmapPreview
from app.services.roadmap import (
    get_roadmap_for_role,
    get_roadmap_preview,
    get_personalized_roadmap,
    get_all_roadmap_previews
)

router = APIRouter()


@router.get("/roadmap/{role_id}", response_model=CareerRoadmap)
def get_roadmap(role_id: int):
    """
    Get the career roadmap for a specific cybersecurity role.
    Returns certifications, skill translations, action steps, and salary info.
    """
    roadmap = get_roadmap_for_role(role_id)

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail=f"Roadmap not found for role ID {role_id}. Valid IDs are 1-10."
        )

    return roadmap


@router.get("/roadmap/{role_id}/preview", response_model=RoadmapPreview)
def get_roadmap_preview_endpoint(role_id: int):
    """
    Get a condensed preview of the roadmap for results page cards.
    """
    preview = get_roadmap_preview(role_id)

    if not preview:
        raise HTTPException(
            status_code=404,
            detail=f"Roadmap not found for role ID {role_id}."
        )

    return preview


@router.get("/roadmap/veteran/{veteran_id}/role/{role_id}", response_model=CareerRoadmap)
def get_personalized_roadmap_endpoint(
    veteran_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a personalized career roadmap based on veteran's profile.
    Skill translations are personalized based on the veteran's rating/MOS.
    """
    roadmap = get_personalized_roadmap(db, veteran_id, role_id)

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail=f"Roadmap not found for role ID {role_id}."
        )

    return roadmap


@router.get("/roadmaps/previews", response_model=List[RoadmapPreview])
def get_all_previews():
    """
    Get preview information for all available career roadmaps.
    """
    return get_all_roadmap_previews()
