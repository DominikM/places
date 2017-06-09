"""
WSGI config for places project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

ACTIVATE = '/home/dominikm/python-envs/django/bin/activate_this.py'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""
with open(ACTIVATE) as file_:
    exec(file_.read(), dict(__file__=ACTIVATE))
"""
sys.path.insert(0, BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "places.settings")

application = get_wsgi_application()
