#!/bin/bash

# Exit on error
set -e

# The Vercel platform automatically runs `pip install -r requirements.txt`
# so we don't need to do it here.

# We just need to ensure the Django `collectstatic` command is run.
# We run it from the root directory, pointing to the correct manage.py file.
python mysite/manage.py collectstatic --no-input
