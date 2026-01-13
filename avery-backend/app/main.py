import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import onboarding, assessment, results, scct, roadmap


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables and seed data on startup."""
    from app.database import engine, Base
    from app.seed_data import seed_database
    from app.scct_seed_data import seed_scct_data

    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        # Auto-seed in production
        seed_database()
        seed_scct_data()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
    yield


app = FastAPI(
    title="Avery API",
    version="1.0.0",
    description="Navy veteran career transition platform - matching veterans to cybersecurity roles based on personality and experience.",
    lifespan=lifespan,
)

# CORS middleware for frontend - allow Vercel and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(onboarding.router, prefix="/api/v1", tags=["Onboarding"])
app.include_router(assessment.router, prefix="/api/v1", tags=["Assessment"])
app.include_router(results.router, prefix="/api/v1", tags=["Results"])
app.include_router(scct.router, prefix="/api/v1", tags=["SCCT Assessment"])
app.include_router(roadmap.router, prefix="/api/v1", tags=["Career Roadmap"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Avery API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
