import json
from typing import List, Dict

from django.conf import settings
from openai import OpenAI


class OpenAIClient:
    """
    Cliente thin-wrapper to generate replies
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_output_tokens = settings.OPENAI_MAX_OUTPUT_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

    def get_topic_and_stance(self, message: str, history=None) -> [str, str, str]:
        """
        Identify topic and stance in conversation
        """
        if history is None:
            history = []

        system = {
            "role": "system",
            "content": (
                "Extract the topic, the bot_stance (pro, con), "
                "and an initial response "
                "the BOT should take from the user's message. "
                "Rules:"
                "1) If the user explicitly assigns a stance to the "
                "BOT (e.g. 'you are pro', 'estás a favor'), "
                "then the BOT must keep that stance."
                "2) If the user only states their OWN stance "
                "(e.g. 'I am pro', 'estoy a favor'), "
                "then the BOT stance must be the opposite."
                "3) If neither is stated, infer a reasonable stance"
                " from the message."
                "4) If the message is a greeting, small talk, or not a "
                "debate-worthy topic "
                "(e.g. 'hello', 'how are you'), then set 'topic' = 'und' and "
                "return a response asking the user to clarify the debate topic"
                "5) If ambiguous, set 'bot_stance' = 'und' and respond "
                "asking the user "
                "to clarify whether they are 'pro' or 'con'."
                "6) Always return ONLY a valid JSON string "
                "with keys: 'topic', 'bot_stance', 'response'."
                "The 'response' must always be a single line string. "
                "Never include line breaks, or Markdown formatting. "
                "Formatting will be handled by the frontend."
            ),
        }

        user = {"role": "user", "content": message}

        history = history or []

        resp = self.client.responses.create(
            model=self.model,
            input=[system, user, *history],
            temperature=0,
            max_output_tokens=120,
        )

        data = json.loads(resp.output_text)
        return data["topic"], data["bot_stance"], data["response"]

    def debate_reply(
        self, topic: str, stance: str, history: List[Dict], user_text: str
    ) -> str:
        """
        Prepare response opposite to user
        """

        sys_behavior = {
            "role": "system",
            "content": (
                "You are a debate bot (role system in history). Stay on the "
                "original "
                "topic "
                "and keep your stance fixed. "
                "Be persuasive but calm. Use 2–3 concise points and "
                "end with a guiding question. "
                "If the user speaks Spanish, reply in Spanish."
                f"Topic: {topic}"
                f"Stance: {stance}"
                "Never change your stance or the topic."
            ),
        }

        history.append({"role": "user", "content": user_text})

        resp = self.client.responses.create(
            model=self.model,
            input=[sys_behavior, *history],
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
        )

        return resp.output_text
