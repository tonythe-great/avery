from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.veteran import Veteran, VeteranOnboardingStart, VeteranResponse

router = APIRouter()


@router.post("/onboarding/start", response_model=VeteranResponse)
def start_onboarding(veteran_data: VeteranOnboardingStart, db: Session = Depends(get_db)):
    """
    Start the onboarding process by creating a veteran profile.
    Returns the created veteran with their ID for subsequent API calls.
    """
    # Check if email already exists
    existing = db.query(Veteran).filter(Veteran.email == veteran_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new veteran
    veteran = Veteran(
        name=veteran_data.name,
        email=veteran_data.email,
        branch=veteran_data.branch,
        rank=veteran_data.rank,
        rating=veteran_data.rating,
        years_of_service=veteran_data.years_of_service,
    )
    db.add(veteran)
    db.commit()
    db.refresh(veteran)
    
    return veteran


@router.get("/onboarding/veteran/{veteran_id}", response_model=VeteranResponse)
def get_veteran(veteran_id: int, db: Session = Depends(get_db)):
    """Get a veteran's profile by ID."""
    veteran = db.query(Veteran).filter(Veteran.id == veteran_id).first()
    if not veteran:
        raise HTTPException(status_code=404, detail="Veteran not found")
    return veteran
