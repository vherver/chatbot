from typing import List, Dict

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from conversation.models import Conversation, Message
from conversation.serializer import MessageRequestSerializer, \
    ConversationResponseSerializer
from lms import OpenAIClient


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
        client = OpenAIClient()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = serializer.validated_data.get("conversation_id")
        user_text = serializer.validated_data["message"]

        conversation, created = self.get_conversation(conversation_id)

        if created:
            topic, stance, bot_response = client.get_topic_and_stance(
                message=user_text)
            conversation.set_topic_and_stance(topic, stance)
        else:
            messages = self.get_last_messages(conversation)
            bot_response = client.debate_reply(conversation.topic,
                                               conversation.stance, messages,
                                               user_text)

        self.create_message(conversation, user_text, Message.Role.USER)
        self.create_message(conversation, bot_response, Message.Role.SYSTEM)

        data = ConversationResponseSerializer.build(conversation)

        return Response(status=status.HTTP_201_CREATED, data=data)

    @staticmethod
    def get_conversation(conversation_id) -> [Conversation, bool]:
        created = False
        if conversation_id:
            try:
                conversation = Conversation.objects.select_for_update().get(
                    conversation_id=conversation_id
                )
            except Conversation.DoesNotExist as e:
                raise NotFound("Conversation not found.") from e
        else:
            created = True
            conversation = Conversation.objects.create()

        return conversation, created

    @staticmethod
    def create_message(
            conversation: Conversation,
            message: str,
            role: str) -> Message:

        message = Message.objects.create(
            conversation=conversation,
            role=role,
            message=message,
        )
        return message

    @staticmethod
    def get_last_messages(conversation: Conversation) -> List[Dict[str, str]]:
        qs = Message.get_last_messages_from_conversation(conversation)
        return [
            {"role": m.role, "content": m.message}
            for m in qs
        ]
