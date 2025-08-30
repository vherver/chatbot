import pytest
from django.utils import timezone
from conversation.models import Conversation, Message


@pytest.mark.django_db
def test_conversation_set_topic_and_stance():
    conv = Conversation.objects.create(topic="init", stance="xxx")
    conv.set_topic_and_stance("AI Safety", "pro")

    conv.refresh_from_db()
    assert conv.topic == "AI Safety"
    assert conv.stance == "pro"
    assert str(conv) == f"Conversation {conv.conversation_id}"


@pytest.mark.django_db
def test_message_str_returns_expected_format():
    conv = Conversation.objects.create(topic="Test", stance="pro")
    msg = Message.objects.create(conversation=conv, role=Message.Role.USER, message="hello")

    s = str(msg)
    assert str(conv.conversation_id) in s
    assert str(msg.message_id) in s
    assert "[user]" in s


@pytest.mark.django_db
def test_get_last_messages_from_conversation_returns_latest_first():
    conv = Conversation.objects.create(topic="Test", stance="con")
    msgs = []
    for i in range(6):
        msgs.append(
            Message.objects.create(conversation=conv, role=Message.Role.USER, message=f"msg {i}")
        )

    last_msgs = Message.get_last_messages_from_conversation(conv, quantity=5)
    assert len(last_msgs) == 5
    assert last_msgs[0].created_at >= last_msgs[1].created_at

    assert list(Message.get_last_messages_from_conversation(conv, quantity=0)) == []