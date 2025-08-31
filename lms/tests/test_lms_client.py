import pytest
from unittest.mock import MagicMock, patch
from lms import OpenAIClient


@pytest.mark.django_db
@patch("lms.OpenAI")
def test_get_topic_and_stance_parses_response(MockOpenAI, settings):
    mock_instance = MockOpenAI.return_value
    mock_resp = MagicMock()
    mock_resp.output_text = '{"topic": "AI", "bot_stance": "pro", "response": "Hello!"}'
    mock_instance.responses.create.return_value = mock_resp

    client = OpenAIClient()
    topic, stance, response = client.get_topic_and_stance("Is AI safe?")

    assert topic == "AI"
    assert stance == "pro"
    assert response == "Hello!"
    mock_instance.responses.create.assert_called_once()


@pytest.mark.django_db
@patch("lms.OpenAI")
def test_debate_reply_returns_bot_text(MockOpenAI, settings):
    mock_instance = MockOpenAI.return_value
    mock_resp = MagicMock()
    mock_resp.output_text = "Counter argument!"
    mock_instance.responses.create.return_value = mock_resp

    client = OpenAIClient()
    history = [{"role": "system", "content": "Stay calm"}]
    response = client.debate_reply("AI", "con", history, "But I like AI")

    assert "Counter argument!" in response
    mock_instance.responses.create.assert_called_once()
