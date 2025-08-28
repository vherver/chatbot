import uuid
from django.db import models
from django.db.models import QuerySet


class Conversation(models.Model):
    """
    Represents a user conversation.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    topic = models.TextField()
    stance = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

    def set_topic_and_stance(self, topic, stance):
        self.topic = topic
        self.stance = stance
        self.save()


class Message(models.Model):
    """
    Represents a message inside a conversation.
    """

    class Role(models.TextChoices):
        BOT = "bot", "Bot"
        USER = "user", "User"

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True,
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        db_index=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "message"
        ordering = ["created_at", "message_id"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
        ]

    def __str__(self):
        return f"[{self.role}] {self.conversation_id} · {str(self.message_id)}"

    @classmethod
    def get_last_messages_from_conversation(
            cls,
            conversation: Conversation,
            quantity: int = 5) -> QuerySet["Message"]:
        """
        Retrieve the latest messages from a given conversation.
        """
        qs = (
                 cls.objects
                 .filter(conversation=conversation)
                 .select_related("conversation")
                 .order_by("-created_at", "-message_id")
             )[: max(quantity, 0)]

        return qs
