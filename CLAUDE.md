# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Avery is a full-stack mobile-first AI career intelligence system that helps Navy veterans transition into cybersecurity roles. It uses a Big Five personality assessment to match veterans with 10 cybersecurity career paths.

## Development Commands

### Frontend (Next.js)
```bash
cd avery-frontend
npm install              # Install dependencies
npm run dev              # Development server (http://localhost:3000)
npm run build            # Production build
npm run lint             # ESLint
```

### Backend (FastAPI)
```bash
cd avery-backend
python -m venv venv && source venv/bin/activate  # Create/activate venv
pip install -r requirements.txt                   # Install dependencies
python -m app.seed_data                          # Seed database with questions/roles
uvicorn app.main:app --reload --port 8000        # Development server
```

### Both Servers
```bash
./start.sh               # Start frontend + backend simultaneously
```

Access points:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

## Architecture

### Monorepo Structure
- `avery-frontend/` - Next.js 14 with App Router, TypeScript, Tailwind CSS
- `avery-backend/` - FastAPI with SQLAlchemy ORM, SQLite database

### Frontend Key Patterns
- Pages use `'use client'` directive for interactivity
- API calls centralized in `src/lib/api.ts`
- Component state + Context for state management (no Redux)
- Custom Tailwind colors defined in `tailwind.config.ts`: `avery.cyan`, `avery.purple`, `avery.teal`, `avery.bg`

### Backend Key Patterns
- Routes in `app/routes/` organized by feature (onboarding, assessment, results)
- Business logic in `app/services/matching.py` (Big Five trait calculation + experience bonuses)
- Database auto-seeds on startup via lifespan event in `main.py`
- Pydantic models for request/response validation alongside SQLAlchemy models

### Core Algorithm
The matching algorithm in `app/services/matching.py`:
1. Calculates Big Five personality trait scores from assessment responses
2. Weights traits against role requirements
3. Applies bonuses for years of service and leadership rank (E-7+, O-1+)
4. Returns match percentage (0-99%) with explanation reasons

### User Flow
4-screen onboarding: Welcome → Identity Input → Analysis → Recommendations
Then: 12-question personality assessment → Top 3 career matches with salary ranges

## Key Files

- `avery-backend/app/services/matching.py` - Core career matching algorithm
- `avery-frontend/src/components/AveryOrb/AveryOrb.tsx` - Animated orb with 5 states (dormant, awakening, attentive, processing, presenting)
- `avery-frontend/src/lib/api.ts` - Frontend API client
- `avery-backend/app/seed_data.py` - Database seeding (questions + roles)
- `avery-frontend/tailwind.config.ts` - Design system with custom animations

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: https://avery-sg3k.onrender.com/api/v1)

### Backend
- `DATABASE_URL` - SQLite connection (default: sqlite:///./avery.db)
- `FRONTEND_URL` - CORS origin (default: http://localhost:3000)

## Design Principles
- Dark-mode first with pure black backgrounds
- No emojis - premium, professional aesthetic
- Glass morphism effects on cards
- The AveryOrb is the central UI element with animated state transitions
