from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from typing import Optional
from app.database import Base


# SQLAlchemy Model
class Veteran(Base):
    __tablename__ = "veterans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    branch = Column(String(50), nullable=False)
    rank = Column(String(50), nullable=False)
    rating = Column(String(50), nullable=True)  # Navy rating/MOS
    security_clearance = Column(String(50), nullable=True)  # Security clearance level
    years_of_service = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic Schemas
class VeteranOnboardingStart(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    branch: str = Field(..., min_length=1, max_length=50)
    rank: str = Field(..., min_length=1, max_length=50)
    rating: Optional[str] = Field(None, max_length=50)
    security_clearance: Optional[str] = Field(None, max_length=50)
    years_of_service: int = Field(..., ge=0, le=50)


class VeteranResponse(BaseModel):
    id: int
    name: str
    email: str
    branch: str
    rank: str
    rating: Optional[str]
    security_clearance: Optional[str]
    years_of_service: int

    class Config:
        from_attributes = True
