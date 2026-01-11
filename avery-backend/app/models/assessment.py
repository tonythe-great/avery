from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from typing import List
from app.database import Base


# SQLAlchemy Models
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    trait = Column(String(50), nullable=False)  # openness, conscientiousness, etc.
    order = Column(Integer, nullable=False)


class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(Integer, primary_key=True, index=True)
    veteran_id = Column(Integer, ForeignKey("veterans.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_value = Column(Integer, nullable=False)  # 1-5 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic Schemas
class QuestionResponse(BaseModel):
    id: int
    text: str
    trait: str
    order: int

    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    question_id: int
    answer_value: int = Field(..., ge=1, le=5)


class AssessmentSubmission(BaseModel):
    veteran_id: int
    answers: List[AnswerSubmission]


class AssessmentSubmitResponse(BaseModel):
    message: str
    veteran_id: int
    answers_recorded: int
