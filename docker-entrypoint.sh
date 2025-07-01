#!/bin/bash
set -e
mkdir data || echo "data directory already exists"
uvicorn app.main:app --host 0.0.0.0 --port 8000
