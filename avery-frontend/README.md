# Avery Frontend

A mobile-first Next.js frontend for the Avery veteran career transition platform.

## Features

- **Mobile-first design** - Optimized for phones with touch-friendly UI
- **PWA-ready** - Can be installed on mobile devices
- **Navy-themed** - Custom color palette with navy blues and gold accents
- **Smooth animations** - Slide and fade transitions throughout

## Pages

1. **Home** (`/`) - Welcome screen with feature overview
2. **Onboarding** (`/onboarding`) - Multi-step profile creation
3. **Assessment** (`/assessment`) - Personality test with 12 questions
4. **Results** (`/results`) - Top 3 cybersecurity career matches

## Setup

### 1. Install dependencies

```bash
cd avery-frontend
npm install
```

### 2. Configure API endpoint (optional)

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Run development server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Requirements

- Node.js 18+
- Avery Backend running on port 8000

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React 18

## Mobile Installation (PWA)

On mobile browsers:
1. Open the app in Safari (iOS) or Chrome (Android)
2. Tap "Add to Home Screen" 
3. The app will work like a native app
