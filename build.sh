#!/bin/bash

# Exit on error
set -e

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py create_superuser
