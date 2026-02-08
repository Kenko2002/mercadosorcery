#!/bin/bash
set -e



echo "--- Applying database migrations ---"
python manage.py migrate

echo "--- Populating database with card data -- -"
python manage.py populate_cards

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput --clear
