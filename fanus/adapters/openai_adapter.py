import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIAdapter:

    def __init__(self, api_key=None):
        key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=key)
        self.model = "gpt-4o-mini"

    def generate(self, system_prompt, user_message):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content