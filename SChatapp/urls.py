# SChatapp/urls.py
from django.urls import path
from .views import chat_page, ConversationListAPI, ChatAPIView

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('api/conversations/', ConversationListAPI.as_view(), name='conversation_list'),
    path('api/conversations/<int:conv_id>/', ConversationListAPI.as_view(), name='conversation_delete'),  # جدید برای DELETE
    path('api/chat/<int:conv_id>/', ChatAPIView.as_view(), name='chat_detail'),
]