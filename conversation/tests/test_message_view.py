from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from conversation.models import Conversation, Message
from conversation.views import MessageView

class MessageViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("send-message")
        self.topic = "test topic"

    @patch("conversation.views.OpenAIClient")
    def test_create_new_conversation_calls_get_topic_and_stance_and_persists_messages(
        self, MockClient
    ):
        mock_client = MockClient.return_value
        mock_client.get_topic_and_stance.return_value = (
            self.topic, "pro", "Hello bot!"
        )

        payload = {"conversation_id": None, "message": "hola"}
        resp = self.client.post(self.url, payload, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)  # user + system
        conversation = Conversation.objects.first()
        self.assertEqual(conversation.topic, self.topic)
        self.assertEqual(conversation.stance, "pro")
        mock_client.get_topic_and_stance.assert_called_once_with(message="hola")

    @patch("conversation.views.OpenAIClient")
    def test_existing_conversation_calls_debate_reply(self, MockClient):
        conversation = Conversation.objects.create(topic=self.topic, stance="pro")
        Message.objects.create(conversation=conversation, role=Message.Role.USER, message="Prev msg")

        mock_client = MockClient.return_value
        mock_client.debate_reply.return_value = "Bot answer"

        response = self.client.post(
            self.url,
            {"conversation_id": str(conversation.conversation_id), "message": "New msg"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 3)
        mock_client.debate_reply.assert_called_once()

    def test_conversation_not_found_returns_404(self):
        fake_uuid = "11111111-1111-1111-1111-111111111111"
        response = self.client.post(
            self.url,
            {"conversation_id": fake_uuid, "message": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Conversation not found", response.data["detail"])

    def test_missing_message_returns_400(self):
        response = self.client.post(self.url, {"conversation_id": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("conversation.views.OpenAIClient")
    def test_existing_conversation_with_no_messages(self, MockClient):
        conv = Conversation.objects.create(topic=self.topic, stance="pro")
        mock_client = MockClient.return_value
        mock_client.debate_reply.return_value = "Bot answer"

        response = self.client.post(
            self.url,
            {"conversation_id": str(conv.conversation_id), "message": "Start"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_client.debate_reply.assert_called_once_with(self.topic, "pro", [], "Start")


class MessageViewStaticMethodsTests(TestCase):
    def setUp(self):
        self.topic = "AI"
        self.conversation = Conversation.objects.create(topic=self.topic, stance="pro")

    def test_get_conversation_creates_new_if_none(self):
        conv, created = MessageView.get_conversation(None)
        self.assertTrue(created)
        self.assertIsInstance(conv, Conversation)

    def test_get_conversation_returns_existing(self):
        conv, created = MessageView.get_conversation(self.conversation.conversation_id)
        self.assertFalse(created)
        self.assertEqual(conv.conversation_id, self.conversation.conversation_id)

    def test_create_message_persists_in_db(self):
        msg = MessageView.create_message(self.conversation, "Hello", Message.Role.USER)
        self.assertEqual(msg.message, "Hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.conversation, self.conversation)

    def test_get_last_messages_returns_dicts(self):
        Message.objects.create(conversation=self.conversation, role=Message.Role.USER, message="Msg1")
        Message.objects.create(conversation=self.conversation, role=Message.Role.SYSTEM, message="Msg2")
        result = MessageView.get_last_messages(self.conversation)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["role"], "system")
        self.assertEqual(result[1]["content"], "Msg1")
