"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
"""
    A Channels routing configuration is an ASGI application that is similar to a Django URLconf, 
    in that it tells Channels what code to run when an HTTP request is received by the Channels server.
    When Django accepts an HTTP request, it consults the root URLconf to lookup a view function, 
    and then calls the view function to handle the request. Similarly, when Channels accepts a WebSocket 
    connection, it consults the root routing configuration to lookup a consumer, and then calls various 
    functions on the consumer to handle events from the connection.
"""
import os

import core.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

django_asgi_app = get_asgi_application()
# creating a routing configuration for Channels
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(core.routing.websocket_urlpatterns)))
})
