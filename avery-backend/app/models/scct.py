from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List, Optional
from app.database import Base


# SQLAlchemy Models

class SCCTQuestion(Base):
    """SCCT assessment questions - 10 Navy-authentic questions covering
    self-efficacy, outcome expectations, goals, and barriers."""
    __tablename__ = "scct_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_key = Column(String(50), unique=True, nullable=False)  # e.g., "watchstation_identity"
    scct_construct = Column(String(50), nullable=False)  # self_efficacy, outcome_expectations, goals, barriers
    question_text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)

    options = relationship("SCCTOption", back_populates="question")


class SCCTOption(Base):
    """Options for each SCCT question with vector impact weights."""
    __tablename__ = "scct_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("scct_questions.id"), nullable=False)
    option_key = Column(String(1), nullable=False)  # a, b, c, d, e
    option_text = Column(Text, nullable=False)

    # Self-Efficacy dimensions (impact weights, -1.0 to 1.0)
    se_technical = Column(Float, default=0.0)  # Technical task confidence
    se_stress = Column(Float, default=0.0)     # Stress handling confidence
    se_growth = Column(Float, default=0.0)     # Learning ability confidence
    se_social = Column(Float, default=0.0)     # Social interaction confidence

    # Outcome Expectations dimensions
    oe_salary_priority = Column(Float, default=0.0)    # How much salary matters
    oe_stability_priority = Column(Float, default=0.0) # How much stability matters
    oe_meaning_priority = Column(Float, default=0.0)   # How much meaning matters

    # Goals dimensions
    goals_timeline = Column(Float, default=0.0)  # 0=immediate need, 1=long-term planning
    goals_level = Column(Float, default=0.0)     # 0=entry level, 1=executive ambition

    # Barriers dimensions
    barriers_financial = Column(Float, default=0.0)   # 0=flexible, 1=constrained
    barriers_technical = Column(Float, default=0.0)   # 0=ready, 1=needs training
    barriers_direction = Column(Float, default=0.0)   # 0=clear path, 1=needs guidance

    question = relationship("SCCTQuestion", back_populates="options")


class SCCTResponse(Base):
    """Veteran's responses to SCCT questions."""
    __tablename__ = "scct_responses"

    id = Column(Integer, primary_key=True, index=True)
    veteran_id = Column(Integer, ForeignKey("veterans.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("scct_questions.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("scct_options.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConfidenceVector(Base):
    """Computed career confidence vector from SCCT responses.
    12-dimensional vector representing veteran's career profile."""
    __tablename__ = "confidence_vectors"

    id = Column(Integer, primary_key=True, index=True)
    veteran_id = Column(Integer, ForeignKey("veterans.id"), unique=True, nullable=False)

    # Self-Efficacy Dimensions (0.0 to 1.0)
    se_technical = Column(Float, default=0.0)
    se_stress = Column(Float, default=0.0)
    se_growth = Column(Float, default=0.0)
    se_social = Column(Float, default=0.0)

    # Outcome Expectations (0.0 to 1.0)
    oe_salary_priority = Column(Float, default=0.0)
    oe_stability_priority = Column(Float, default=0.0)
    oe_meaning_priority = Column(Float, default=0.0)

    # Goals (0.0 to 1.0)
    goals_timeline = Column(Float, default=0.0)
    goals_level = Column(Float, default=0.0)

    # Barriers (0.0 to 1.0)
    barriers_financial = Column(Float, default=0.0)
    barriers_technical = Column(Float, default=0.0)
    barriers_direction = Column(Float, default=0.0)

    # Metadata
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    version = Column(String(20), default="1.0.0")


class SalaryBand(Base):
    """Salary bands for roles by experience level."""
    __tablename__ = "salary_bands"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("cyber_roles.id"), nullable=False)
    experience_level = Column(String(20), nullable=False)  # entry, mid, senior, lead, director

    # Salary percentiles (USD, annual)
    p10 = Column(Integer, nullable=False)
    p25 = Column(Integer, nullable=False)
    p50 = Column(Integer, nullable=False)  # Median
    p75 = Column(Integer, nullable=False)
    p90 = Column(Integer, nullable=False)

    data_source = Column(String(50), default="industry_average")
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic Schemas

class SCCTOptionResponse(BaseModel):
    id: int
    option_key: str
    option_text: str

    class Config:
        from_attributes = True


class SCCTQuestionResponse(BaseModel):
    id: int
    question_key: str
    scct_construct: str
    question_text: str
    order: int
    options: List[SCCTOptionResponse]

    class Config:
        from_attributes = True


class SCCTAnswerSubmission(BaseModel):
    question_id: int
    option_id: int


class SCCTSubmission(BaseModel):
    veteran_id: int
    answers: List[SCCTAnswerSubmission]


class SCCTSubmitResponse(BaseModel):
    message: str
    veteran_id: int
    answers_recorded: int


class ConfidenceVectorResponse(BaseModel):
    veteran_id: int
    se_technical: float
    se_stress: float
    se_growth: float
    se_social: float
    oe_salary_priority: float
    oe_stability_priority: float
    oe_meaning_priority: float
    goals_timeline: float
    goals_level: float
    barriers_financial: float
    barriers_technical: float
    barriers_direction: float
    version: str

    class Config:
        from_attributes = True


class SalaryEstimate(BaseModel):
    low: int
    mid: int
    high: int
    confidence: float
    source: str
    disclaimer: str = "Estimates based on industry data. Actual offers may vary."


class RecommendationExplanation(BaseModel):
    primary_reason: str
    secondary_reasons: List[str]
    concerns: List[str]
    next_steps: str
    avery_quote: str


class SCCTRoleMatch(BaseModel):
    role_id: int
    role_name: str
    role_description: str
    match_score: float
    salary_estimate: SalaryEstimate
    explanation: RecommendationExplanation
    score_breakdown: dict

    class Config:
        from_attributes = True
