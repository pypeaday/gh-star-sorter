#!/bin/bash
set -e

# Add extreme verbosity for debugging
set -x

echo "--- DOCKER ENTRYPOINT DIAGNOSTICS ---"
echo "Timestamp: $(date)"
echo "Running as user: '$(whoami)'"
echo "User ID: $(id -u)"
echo "Current directory: '$(pwd)'"

echo "Listing contents of /app (working directory):"
ls -alh /app

echo "Attempting to create data directory at /app/data..."
mkdir -p /app/data

echo "Listing contents of /app/data directory:"
# This might fail if permissions are wrong, so we add a fallback message
ls -alh /app/data || echo "!! Could not list /app/data. It might not exist or permissions are wrong."

echo "--- END DIAGNOSTICS ---"

echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
