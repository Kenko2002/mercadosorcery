#!/bin/bash
set -e

# Install system dependencies for psycopg2
echo "--- Installing system dependencies ---"
apt-get update && apt-get install -y postgresql-client libpq-dev

# Install Python dependencies
echo "--- Installing Python dependencies ---"
pip install -r requirements.txt
