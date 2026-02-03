"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the parent directory of this file (the 'mysite' directory) to the Python path.
# This allows the Vercel runtime to find the 'base' module.
# __file__ -> /var/task/mysite/base/wsgi.py
# .parent -> /var/task/mysite/base
# .parent.parent -> /var/task/mysite
sys.path.append(str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

application = get_wsgi_application()

# Vercel needs this to be called 'app'
app = application
