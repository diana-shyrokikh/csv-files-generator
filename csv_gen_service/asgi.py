"""
ASGI config for csv_gen_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import csv_generator.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csv_gen_service.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(csv_generator.routing.websocket_urlpatterns)
        ),
    }
)
