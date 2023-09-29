from django.urls import re_path
from csv_generator import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/socket-server/",
        consumers.CSVGeneratorConsumer.as_asgi()
    )
]
