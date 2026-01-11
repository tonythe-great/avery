#!/bin/bash
cd /Users/tonystephenson/avery

# Create root .gitignore
cat > .gitignore << 'GITIGNORE'
venv/
__pycache__/
*.pyc
node_modules/
.next/
.env
.DS_Store
*.log
GITIGNORE

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Avery MVP - Navy veteran career transition platform"

# Add remote and push
git remote add origin https://github.com/tonythe-great/avery.git
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your project is now at: https://github.com/tonythe-great/avery"
