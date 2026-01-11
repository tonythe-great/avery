from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import onboarding, assessment, results


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup."""
    from app.database import engine, Base
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Warning: Could not connect to database: {e}")
        print("Make sure PostgreSQL is running and the 'avery' database exists.")
    yield


app = FastAPI(
    title="Avery API",
    version="1.0.0",
    description="Navy veteran career transition platform - matching veterans to cybersecurity roles based on personality and experience.",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(onboarding.router, prefix="/api/v1", tags=["Onboarding"])
app.include_router(assessment.router, prefix="/api/v1", tags=["Assessment"])
app.include_router(results.router, prefix="/api/v1", tags=["Results"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Avery API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
