#!/bin/bash
set -e

# Activate the virtual environment to run Django commands
source .venv/bin/activate

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Creating superuser ---"
python manage.py create_superuser
