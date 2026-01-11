# Avery - AI Career Intelligence System

<p align="center">
  <img src="docs/screenshots/avery-orb.png" alt="Avery AI Core" width="200"/>
</p>

<p align="center">
  <strong>Your personal JARVIS for cybersecurity careers</strong>
</p>

<p align="center">
  <a href="https://avery-gamma.vercel.app/start">Live Demo</a> •
  <a href="https://avery-gamma.vercel.app/orb-demo">Orb Demo</a> •
  <a href="https://avery-sg3k.onrender.com/docs">API Docs</a>
</p>

---

## Overview

Avery is a mobile-first AI career intelligence system that helps Navy veterans transition into high-paying cybersecurity roles. Unlike traditional career apps, Avery feels like a sentient AI system — analyzing your skills, experience, and personality to deliver authoritative career recommendations.

## Screenshots

<p align="center">
  <img src="docs/screenshots/welcome.png" alt="Welcome Screen" width="250"/>
  <img src="docs/screenshots/analysis.png" alt="Analysis Screen" width="250"/>
  <img src="docs/screenshots/results.png" alt="Results Screen" width="250"/>
</p>

| Welcome | Identity Input | Analysis | Results |
|---------|----------------|----------|---------|
| ![Welcome](docs/screenshots/welcome.png) | ![Identity](docs/screenshots/identity.png) | ![Analysis](docs/screenshots/analysis.png) | ![Results](docs/screenshots/results.png) |

## Features

### The Avery Orb
The AI core is a living, animated orb that responds to user interaction:

| State | Behavior | Use Case |
|-------|----------|----------|
| **Dormant** | Dim, still | Before interaction |
| **Awakening** | Fades in, rings start | Welcome screen |
| **Attentive** | Gentle pulse | Awaiting input |
| **Processing** | Fast spin, color cycling | During analysis |
| **Presenting** | Steady glow | Showing results |

### Intelligent Onboarding
- 4-screen flow: Welcome → Identity → Analysis → Recommendation
- Typewriter text reveals
- Floating card inputs
- Real-time profile analysis

### Career Intelligence
- Personality assessment (Big Five traits)
- 847 cybersecurity roles analyzed
- Confidence percentage with animated rings
- Salary range estimates ($65K - $350K)
- Match reasons explained

### Design System
- **Dark-mode first** — Pure black backgrounds
- **Cyan/Purple/Teal** — Avery color palette
- **No emojis** — Premium, professional feel
- **Glass morphism** — Subtle card effects
- **Glow effects** — Animated button highlights

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, SQLAlchemy |
| Database | SQLite |
| Deployment | Vercel (frontend), Render (backend) |

## Project Structure

```
avery/
├── avery-backend/
│   └── app/
│       ├── main.py              # FastAPI entry
│       ├── models/              # Database models
│       ├── routes/              # API endpoints
│       ├── services/            # Matching algorithm
│       └── seed_data.py         # Questions & roles
│
├── avery-frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx         # Home
│       │   ├── start/           # Onboarding flow
│       │   ├── assessment/      # Personality quiz
│       │   ├── results/         # Career matches
│       │   └── orb-demo/        # Orb state testing
│       │
│       └── components/
│           ├── AveryOrb/        # Animated AI core
│           ├── onboarding/      # Flow screens
│           └── ui/              # Shared components
│
└── docs/
    └── screenshots/             # App screenshots
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### Local Development

```bash
# Clone the repo
git clone https://github.com/tonythe-great/avery.git
cd avery

# Start both servers
chmod +x start.sh
./start.sh
```

Open http://localhost:3000

### Test the Orb

Visit http://localhost:3000/orb-demo to test all orb states interactively.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/onboarding/start` | Create veteran profile |
| GET | `/api/v1/assessment/questions` | Get 12 personality questions |
| POST | `/api/v1/assessment/submit` | Submit assessment answers |
| GET | `/api/v1/results/{id}` | Get top 3 career matches |

## Cybersecurity Roles

Avery matches veterans to 10 cybersecurity career paths:

| Role | Salary Range |
|------|--------------|
| SOC Analyst | $65K - $95K |
| Penetration Tester | $85K - $140K |
| Incident Response Specialist | $80K - $130K |
| Security Engineer | $95K - $155K |
| Cybersecurity Consultant | $90K - $160K |
| Threat Intelligence Analyst | $85K - $135K |
| Security Awareness Trainer | $70K - $110K |
| CISO | $180K - $350K |
| Digital Forensics Investigator | $75K - $125K |
| Cloud Security Architect | $140K - $220K |

## Adding Screenshots

To add screenshots, save images to `docs/screenshots/`:

```
docs/screenshots/
├── avery-orb.png      # The AI core image
├── welcome.png        # Welcome screen
├── identity.png       # Identity input screen
├── analysis.png       # Processing/analysis screen
└── results.png        # Results screen
```

## License

MIT
