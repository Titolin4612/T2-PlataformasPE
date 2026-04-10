"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# WSGI SETTINGS: fija el módulo de configuración antes de construir la aplicación.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ENTRADA WSGI: objeto que usan servidores síncronos tradicionales para servir el proyecto.
application = get_wsgi_application()
