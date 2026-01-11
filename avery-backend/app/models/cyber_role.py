from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Text
from typing import Optional
from app.database import Base


# SQLAlchemy Model
class CyberRole(Base):
    __tablename__ = "cyber_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    
    # Big Five trait weights (how important each trait is for this role, 0.0-1.0)
    openness_weight = Column(Float, default=0.5)
    conscientiousness_weight = Column(Float, default=0.5)
    extraversion_weight = Column(Float, default=0.5)
    agreeableness_weight = Column(Float, default=0.5)
    stability_weight = Column(Float, default=0.5)  # Inverted neuroticism
    
    # Ideal trait scores for this role (1-5 scale)
    openness_ideal = Column(Float, default=3.0)
    conscientiousness_ideal = Column(Float, default=3.0)
    extraversion_ideal = Column(Float, default=3.0)
    agreeableness_ideal = Column(Float, default=3.0)
    stability_ideal = Column(Float, default=3.0)
    
    # Military experience bonus factors
    min_years_preferred = Column(Integer, default=0)
    leadership_bonus = Column(Float, default=0.0)  # Bonus for higher ranks


# Pydantic Schemas
class CyberRoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class RoleMatch(BaseModel):
    role: CyberRoleResponse
    match_percentage: float
    match_reasons: list[str]
