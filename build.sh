#!/bin/bash
set -e

# Activate the virtual environment to run Django commands
source .venv/bin/activate

echo "--- Collecting static files ---"
# Collect static files into a directory named 'staticfiles'
python manage.py collectstatic --noinput --clear

echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Creating superuser ---"
python manage.py create_superuser
