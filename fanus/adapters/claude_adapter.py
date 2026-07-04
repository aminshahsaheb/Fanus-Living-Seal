import os
import anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeAdapter:

    def __init__(self, api_key=None):
        key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.client = anthropic.Anthropic(api_key=key)
        self.model = "claude-sonnet-4-6"

    def generate(self, system_prompt, user_message):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return message.content[0].text