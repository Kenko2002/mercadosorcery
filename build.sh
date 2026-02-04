#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Installing system dependencies ---"
apt-get update && apt-get install -y postgresql-client libpq-dev

echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Creating superuser ---"
python manage.py create_superuser
