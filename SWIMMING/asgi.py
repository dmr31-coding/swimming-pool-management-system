"""
ASGI config for SWIMMING project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SWIMMING.settings")

from channels.routing import ProtocolTypeRouter, URLRouter
import swimming_app.routing

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {"websocket": URLRouter(swimming_app.routing.ws_patterns)}
)
