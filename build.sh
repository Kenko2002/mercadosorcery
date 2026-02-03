#!/bin/bash

# Exit on error
set -e

# The Vercel platform automatically runs `pip install -r requirements.txt`

# Run collectstatic
echo "--- Running collectstatic --- "
python mysite/manage.py collectstatic --no-input

# --- DIAGNOSTICS ---
# List the contents of the staticfiles directory to the build log.
# This will show us what `collectstatic` actually collected.
echo "--- Contents of staticfiles directory after collectstatic --- "
ls -R staticfiles
