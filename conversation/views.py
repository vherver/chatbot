from rest_framework.generics import CreateAPIView

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

    pass
