#!/bin/bash

# Exit on error
set -e

# Install dependencies using --break-system-packages to comply with PEP 668
python3.9 -m pip install -r mysite/requirements.txt --break-system-packages

# Collect static files
python3.9 mysite/manage.py collectstatic --noinput
