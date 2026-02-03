#!/bin/bash
# Navigate into the directory where manage.py is located
cd mysite

# Activate virtual environment
source ../.venv/bin/activate

# Run the Django development server
python manage.py runserver 0.0.0.0:8080
