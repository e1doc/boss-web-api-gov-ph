from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/building-file-upload/', consumers.BuildingFileUploadConsumer.as_asgi()),
]