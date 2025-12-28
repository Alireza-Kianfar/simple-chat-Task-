from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render
import time

class ChatAPIView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.save(is_user=True)

            bot_reply_text ='' + user_message.text
            bot_message = Message.objects.create(
                text=bot_reply_text,
                is_user=False
            )
            return Response({
                'text': user_message.text,
                'created_at': user_message.created_at.isoformat(),
                'reply': bot_reply_text,
                'reply_time': bot_message.created_at.isoformat()
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def chat_page(request):

    messages = Message.objects.all().order_by('created_at')
    return render(request, 'index1.html', {'messages': messages})