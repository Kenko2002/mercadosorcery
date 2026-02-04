#!/bin/bash
set -e

# Activate the virtual environment to run Django commands
source .venv/bin/activate

echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Populating database with card data ---"
python manage.py populate_links

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput --clear
