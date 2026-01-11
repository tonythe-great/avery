# Avery - Navy Veteran Career Transition Platform

🚀 **[Live Demo](https://avery-gamma.vercel.app)** | 📖 **[API Docs](https://avery-sg3k.onrender.com/docs)**

A platform that helps Navy veterans discover their ideal cybersecurity career path based on personality assessment and military experience.

## Features

- 🎯 Personality assessment based on Big Five traits
- ⚓ Tailored for Navy veterans (rank, years of service, rating)
- 🔒 Matches to 10 cybersecurity career paths
- 📱 Mobile-first, PWA-ready design
- ⚡ Real-time career recommendations with match percentages

## Tech Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: SQLite
- **Deployment**: Vercel (frontend), Render (backend)

## Project Structure

```
avery/
├── avery-backend/        # FastAPI backend
│   ├── app/
│   │   ├── main.py       # API entry point
│   │   ├── models/       # Database models
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   └── seed_data.py  # Questions & roles
│   └── requirements.txt
├── avery-frontend/       # Next.js frontend
│   ├── src/app/          # App pages
│   └── src/lib/          # API client
└── start.sh              # Start both servers locally
```

## Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+

### Quick Start

```bash
# Clone the repo
git clone https://github.com/tonythe-great/avery.git
cd avery

# Start both servers
chmod +x start.sh
./start.sh
```

Then open http://localhost:3000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/onboarding/start` | Create veteran profile |
| GET | `/api/v1/assessment/questions` | Get personality questions |
| POST | `/api/v1/assessment/submit` | Submit answers |
| GET | `/api/v1/results/{id}` | Get top 3 career matches |

## License

MIT
