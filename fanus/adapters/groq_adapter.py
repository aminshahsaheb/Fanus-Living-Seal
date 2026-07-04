import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqAdapter:

    def __init__(self, api_key=None):
        key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.client = Groq(api_key=key)
        self.model = "llama-3.3-70b-versatile"

    def generate(self, system_prompt, user_message):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content