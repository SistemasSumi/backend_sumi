import os

import sys

import site

from django.core.wsgi import get_wsgi_application

# Add the app"s directory to the PYTHONPATH

sys.path.append("C:/DOLICMAG/Backend")

sys.path.append("C:/DOLICMAG/Backend/Sigban")

os.environ["DJANGO_SETTINGS_MODULE"] = 'Sigban.settings.prod'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Sigban.settings.prod')

application = get_wsgi_application()