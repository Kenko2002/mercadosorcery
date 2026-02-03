#!/bin/bash

# Exit on error
set -e

# The Vercel platform automatically runs `pip install -r requirements.txt`
# so we don't need to do it here.

# We just need to ensure the Django `collectstatic` command is run.
# We navigate into the `mysite` directory to run the command.
cd mysite
python manage.py collectstatic --no-input
