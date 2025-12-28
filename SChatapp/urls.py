from django.urls import path
from .views import ChatAPIView, chat_page

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('api/message/', ChatAPIView.as_view(), name='chat_api'),
]