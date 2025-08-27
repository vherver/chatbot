from rest_framework import serializers


class MessageRequestSerializer(serializers.Serializer):
    """
        Serializer to validate incoming request data for creating  a message.

        Expected JSON body:
        {
            "conversation_id": "UUID | null",
            "message": "string"
        }

        Fields:
        --------
        conversation_id : UUID (optional, nullable)
            - Represents the identifier of an existing conversation.
            - If null or not provided, it means the message may start a new
            conversation.
            - Example: "550e8400-e29b-41d4-a716-446655440000"

        message : str (required)
            - The actual content of the message sent by the user.
            - Max length set to 500 characters.
        """
    conversation_id = serializers.UUIDField(
        required=False, allow_null=True
    )
    message = serializers.CharField(max_length=500)