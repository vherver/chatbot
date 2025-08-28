from rest_framework import serializers

from conversation.models import Message, Conversation


class MessageRequestSerializer(serializers.Serializer):
    """
        Serializer to validate incoming request data for creating  a message.

        Expected JSON body:
        {
            "conversation_id": "UUID | null",
            "message": "string"
        }
        """
    conversation_id = serializers.UUIDField(
        required=False, allow_null=True
    )
    message = serializers.CharField(max_length=500)

from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for a single message inside a conversation.
    Includes the role (user/bot) and the message content.
    """
    class Meta:
        model = Message


class ConversationResponseSerializer(serializers.Serializer):
    """
    Serializer for the conversation response structure.
    It includes the conversation_id and a list of the most recent messages.
    """
    conversation_id = serializers.UUIDField()
    message = MessageSerializer(many=True)

    @staticmethod
    def build(conversation: Conversation):
        """
        Build a serialized dictionary with the last messages of the conversation.
        """
        messages_qs = Message.get_last_messages_from_conversation(conversation)
        serializer = ConversationResponseSerializer({
            "conversation_id": conversation.conversation_id,
            "message": messages_qs,
        })
        return serializer.data
