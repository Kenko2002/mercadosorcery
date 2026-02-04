#!/bin/bash
set -e

# Install system dependencies for psycopg2 using yum
echo "--- Installing system dependencies with yum ---"
yum install -y postgresql-devel

# Create a virtual environment
echo "--- Creating Python virtual environment ---"
python3 -m venv .venv

# Install Python dependencies into the virtual environment
echo "--- Installing Python dependencies ---"
.venv/bin/pip install -r requirements.txt
