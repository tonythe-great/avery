#!/bin/bash
cd /Users/tonystephenson/avery

echo "=== Checking git status ==="
git status

echo ""
echo "=== Files that will be pushed ==="
git ls-files

echo ""
echo "=== Adding all files ==="
git add -A

echo ""
echo "=== Committing ==="
git commit -m "Add all project files" --allow-empty

echo ""
echo "=== Pushing to GitHub ==="
git push -u origin main

echo ""
echo "✅ Done! Check https://github.com/tonythe-great/avery"
