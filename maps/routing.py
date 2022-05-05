from django.urls import re_path
from .consumers import StartProjectConsumer, ProjectDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/startproject/(?P<project_id>\w+)/', ProjectDataConsumer.as_asgi()),
    re_path(r'ws/startproject/', StartProjectConsumer.as_asgi()),

]