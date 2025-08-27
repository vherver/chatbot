from uuid import UUID

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from conversation.models import Conversation, Message
from conversation.serializer import MessageRequestSerializer


class MessageView(CreateAPIView):
    """
    Create a new message in a conversation.

    Expected body:
    {
        "conversation_id": "UUID | null",
        "message": "string"
    }
    """
    serializer_class = MessageRequestSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = serializer.validated_data.get("conversation_id")
        message_text = serializer.validated_data["message"]

        conversation = self.get_conversation(conversation_id)

        self.create_message(conversation, message_text, Message.Role.USER)

        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def get_conversation(conversation_id: UUID) -> Conversation:
        if conversation_id:
            try:
                conversation = Conversation.objects.select_for_update().get(
                    conversation_id=conversation_id
                )
            except Conversation.DoesNotExist as e:
                raise NotFound("Conversation not found.") from e
        else:
            conversation = Conversation.objects.create()

        return conversation

    @staticmethod
    def create_message(
            conversation: Conversation,
            content: str,
            role: str) -> Message:

        message = Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
        )
        return message
