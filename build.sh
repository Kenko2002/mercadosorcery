#!/bin/bash

# Exit on error
set -e

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r mysite/requirements.txt

# Collect static files
python3.9 mysite/manage.py collectstatic --noinput
