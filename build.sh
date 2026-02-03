#!/bin/bash

# Exit on error
set -e

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r mysite/requirements.txt

# Navigate into the Django project directory
cd mysite

# Collect static files
python manage.py collectstatic --no-input
