"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# ASGI SETTINGS: fija el módulo de configuración antes de construir la aplicación.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ENTRADA ASGI: objeto que usan servidores asíncronos para atender solicitudes.
application = get_asgi_application()
