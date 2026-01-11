# Avery Backend

A FastAPI backend for matching Navy veterans to cybersecurity careers based on personality assessment and military experience.

## Features

- **Veteran Onboarding**: Collect veteran profile information (name, rank, years of service)
- **Personality Assessment**: Big Five personality test (12 questions)
- **Career Matching**: Algorithm that matches veterans to top 3 cybersecurity roles
- **10 Cybersecurity Roles**: SOC Analyst, Penetration Tester, Incident Response, and more

## Prerequisites

- Python 3.10+
- PostgreSQL 13+

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL database

```bash
# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql

# Create the database
createdb avery

# Or using psql
psql -c "CREATE DATABASE avery;"
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env if you need different database credentials
```

### 5. Seed the database

```bash
cd avery-backend
python -m app.seed_data
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/v1/onboarding/start` | Create veteran profile |
| GET | `/api/v1/onboarding/veteran/{id}` | Get veteran profile |
| GET | `/api/v1/assessment/questions` | Get personality test questions |
| POST | `/api/v1/assessment/submit` | Submit assessment answers |
| GET | `/api/v1/assessment/status/{id}` | Check assessment completion |
| GET | `/api/v1/results/{id}` | Get top 3 role recommendations |
| GET | `/api/v1/results/{id}/full` | Get detailed results with trait scores |

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### 1. Create a veteran profile

```bash
curl -X POST http://localhost:8000/api/v1/onboarding/start \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "branch": "Navy",
    "rank": "E-6",
    "rating": "IT",
    "years_of_service": 8
  }'
```

### 2. Get assessment questions

```bash
curl http://localhost:8000/api/v1/assessment/questions
```

### 3. Submit assessment

```bash
curl -X POST http://localhost:8000/api/v1/assessment/submit \
  -H "Content-Type: application/json" \
  -d '{
    "veteran_id": 1,
    "answers": [
      {"question_id": 1, "answer_value": 4},
      {"question_id": 2, "answer_value": 5},
      ...
    ]
  }'
```

### 4. Get recommendations

```bash
curl http://localhost:8000/api/v1/results/1
```

## Project Structure

```
avery-backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database connection
│   ├── config.py         # Configuration settings
│   ├── seed_data.py      # Seed questions and roles
│   ├── models/
│   │   ├── veteran.py    # Veteran model
│   │   ├── assessment.py # Question/Response models
│   │   └── cyber_role.py # CyberRole model
│   ├── routes/
│   │   ├── onboarding.py # Onboarding endpoints
│   │   ├── assessment.py # Assessment endpoints
│   │   └── results.py    # Results endpoints
│   └── services/
│       └── matching.py   # Matching algorithm
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
