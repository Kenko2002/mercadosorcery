#!/bin/bash
set -e

# These commands run after dependencies are installed
echo "--- Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Creating superuser ---"
python manage.py create_superuser
