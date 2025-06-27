#!/bin/bash
set -e
mkdir data || echo "data directory already exists"
python ./app/database.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
