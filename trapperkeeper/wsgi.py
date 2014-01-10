"""
WSGI config for trapperkeeper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
try:
    import trapperkeeper.settings_local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trapperkeeper.settings_local")
except:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trapperkeeper.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
