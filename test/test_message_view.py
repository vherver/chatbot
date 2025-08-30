from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from rest_framework import status
from rest_framework.test import APIClient

from conversation.models import Conversation, Message


def resolve_url():
    return reverse("send-message")


class MessageViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = resolve_url()

    @patch("conversation.views.OpenAIClient")
    def test_create_new_conversation_calls_get_topic_and_stance_and_persists_messages(
            self, MockClient
    ):
        mock_client = MockClient.return_value
        mock_client.get_topic_and_stance.return_value = (
        "AI Safety", "pro", "Hello bot!")

        payload = {"conversation_id": None, "message": "hola"}
        resp = self.client.post(self.url, payload, format="json")

        print(self.url)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)