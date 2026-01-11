#!/bin/bash
cd /Users/tonystephenson/avery

echo "📦 Pushing changes to GitHub for Render deployment..."

git add .
git commit -m "Add Render deployment configuration"
git push origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo ""
echo "Now go to https://render.com and create a new Web Service:"
echo ""
echo "1. Connect your GitHub repo: tonythe-great/avery"
echo "2. Use these settings:"
echo ""
echo "   Root Directory:  avery-backend"
echo "   Build Command:   pip install -r requirements.txt"
echo "   Start Command:   gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:\$PORT"
echo ""
echo "3. Click 'Create Web Service'"
echo ""
