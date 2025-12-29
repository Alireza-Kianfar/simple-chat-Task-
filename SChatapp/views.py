# views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer


def chat_page(request):
    return render(request, 'index1.html')


def get_default_conversation():
    return Conversation.objects.get_or_create(title="Default Chat")[0]


class ConversationListAPI(APIView):
    def get(self, request):
        conversations = Conversation.objects.all().order_by('-updated_at')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        conv = Conversation.objects.create(title="New Chat")
        return Response({'id': conv.id, 'title': conv.title}, status=status.HTTP_201_CREATED)

    def delete(self, request, conv_id=None):
        if not conv_id:
            return Response({'error': 'Conversation ID required'}, status=status.HTTP_400_BAD_REQUEST)
        conv = get_object_or_404(Conversation, id=conv_id)
        conv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatAPIView(APIView):
    def get(self, request, conv_id=None):
        if conv_id is None:
            conv = get_default_conversation()
        else:
            conv = get_object_or_404(Conversation, id=conv_id)

        messages = conv.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'messages': serializer.data,
            'conversation': {'id': conv.id, 'title': conv.title}
        })

    def post(self, request, conv_id=None):
        if conv_id is None:
            conv = get_default_conversation()
        else:
            conv = get_object_or_404(Conversation, id=conv_id)

        text = request.data.get('text', '').strip()
        if not text:
            return Response({'error': 'Empty text'}, status=status.HTTP_400_BAD_REQUEST)

        user_message = Message.objects.create(
            conversation=conv,
            text=text,
            is_user=True,
            user=request.user if request.user.is_authenticated else None
        )


        bot_reply_text = f"Message received: \"{text}\""
        bot_message = Message.objects.create(
            conversation=conv,
            text=bot_reply_text,
            is_user=False
        )

        if conv.messages.filter(is_user=True).count() == 1:
            conv.title = text[:40] + "..." if len(text) > 40 else text
            conv.save()

        conv.updated_at = timezone.now()
        conv.save()

        return Response({
            'user_message': MessageSerializer(user_message).data,
            'bot_reply': MessageSerializer(bot_message).data,
        }, status=status.HTTP_201_CREATED)