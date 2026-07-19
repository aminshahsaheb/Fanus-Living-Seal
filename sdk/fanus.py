"""
Fanus SDK — Python client for Fanus Verify API
pip install fanus-sdk
"""
import requests


class FanusClient:

    def __init__(self, api_key: str, base_url: str = "https://web-production-924a5.up.railway.app"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }

    def verify(self, prompt: str, response: str, context: str = "") -> dict:
        """Fast verify — no web search."""
        r = requests.post(
            self.base_url + "/verify",
            headers=self.headers,
            json={"prompt": prompt, "response": response, "context": context}
        )
        r.raise_for_status()
        return r.json()

    def verify_deep(self, prompt: str, response: str) -> dict:
        """Deep verify — with knowledge sources."""
        r = requests.post(
            self.base_url + "/verify/deep",
            headers=self.headers,
            json={"prompt": prompt, "response": response}
        )
        r.raise_for_status()
        return r.json()

    def status(self) -> dict:
        """Get engine status."""
        r = requests.get(self.base_url + "/status")
        r.raise_for_status()
        return r.json()

    def chat(self, message: str) -> dict:
        """Chat with Fanus."""
        r = requests.post(
            self.base_url + "/chat",
            headers=self.headers,
            json={"message": message}
        )
        r.raise_for_status()
        return r.json()
