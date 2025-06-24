#!/bin/bash
set -e

export VIRTUAL_ENV=/opt/venv

echo "Starting Star Sorter application..."

# Run database init
# check if data/gh_stars.db exists
if [ ! -f data/gh_stars.db ]; then
    echo "Initializing database..."
    python app/database.py
fi

# Start the application
echo "Starting Star Sorter web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000


