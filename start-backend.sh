#!/bin/bash
cd /Users/tonystephenson/avery/avery-backend
source ../venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0
