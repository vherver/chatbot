import json

from django.conf import settings
from openai import OpenAI


class OpenAIClient:
    """
    Cliente thin-wrapper para generar réplicas de debate
    con postura fija usando el Responses API.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_output_tokens = settings.OPENAI_MAX_OUTPUT_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

    def get_topic_and_stance(self, message: str) -> [str, str, str]:
        """
        Identify topic and stance in conversation
        """
        system = {
            "role": "system",
            "content": (
                "Extract the topic, the bot_stance (pro, con) and response "
                " the BOT "
                "should take "
                "from "
                "the user's message. "
                "Rules:"
                "1) If the user explicitly assigns a stance"
                " to the BOT, use it."
                "2) If the user states their OWN stance only, "
                "set the BOT to the opposite."
                "3) If neither is stated, infer a reasonable stance "
                "from the message; if ambiguous, pick 'pro'. Add the first "
                "response to user related of topic and bot stance as response"
                "Return ONLY a JSON"
            )
        }

        user = {"role": "user", "content": message}

        resp = self.client.responses.create(
            model=self.model,
            input=[system, user],
            temperature=0,
            max_output_tokens=120,

        )

        data = json.loads(resp.output_text)
        return data["topic"], data["bot_stance"], data["response"]
