#!/bin/bash

echo "🚀 Starting Avery..."
echo ""

# Kill any existing processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start backend in background
echo "Starting backend on http://localhost:8000..."
cd /Users/tonystephenson/avery/avery-backend
source ../venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend in background
echo "Starting frontend on http://localhost:3000..."
cd /Users/tonystephenson/avery/avery-frontend
npm run dev -- --hostname 0.0.0.0 &
FRONTEND_PID=$!

echo ""
echo "✅ Avery is running!"
echo ""
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Mobile:   http://192.168.1.247:3000"
echo ""
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers..."
echo ""

# Wait for Ctrl+C and clean up
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM

# Keep script running
wait
