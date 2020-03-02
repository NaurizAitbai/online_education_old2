from django.urls import path

from base import consumers


websocket_urlpatterns = [
    path('ws/lesson/<int:lesson_id>/', consumers.LessonConsumer),
]