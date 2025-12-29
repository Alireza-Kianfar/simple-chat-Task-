from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at', 'is_user']

class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_time = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'last_message', 'last_time', 'created_at']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        return msg.text[:50] + "..." if msg and len(msg.text) > 50 else (msg.text if msg else "No messages")

    def get_last_time(self, obj):
        msg = obj.messages.last()
        if msg:
            return msg.created_at.isoformat()
        return obj.created_at.isoformat()