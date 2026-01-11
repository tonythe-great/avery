#!/bin/bash
cd /Users/tonystephenson/avery

echo "📦 Pushing frontend changes to GitHub..."

git add .
git commit -m "Update frontend to use Render backend URL"
git push origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo ""
echo "Now deploy to Vercel:"
echo ""
echo "1. Go to https://vercel.com"
echo "2. Sign up/login with GitHub"
echo "3. Click 'Add New...' → 'Project'"
echo "4. Import your repo: tonythe-great/avery"
echo "5. Set Root Directory to: avery-frontend"
echo "6. Click 'Deploy'"
echo ""
echo "Your MVP will be live at something like: https://avery.vercel.app"
echo ""
