#!/bin/bash
set -e

export VIRTUAL_ENV=/opt/venv

echo "Starting Star Sorter application..."

echo "Initializing database..."
python app/database.py

# Start the application
echo "Starting Star Sorter web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000


