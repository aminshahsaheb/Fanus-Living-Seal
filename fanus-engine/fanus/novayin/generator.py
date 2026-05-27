import random

class NovayinGenerator:
    def __init__(self):
        from .words import NOVAYIN_LEXICON
        self.lexicon = NOVAYIN_LEXICON

    def refine(self, text: str) -> str:
        # Light touch: replace flattery phrases, add poetic closing if missing
        if "best" in text.lower() and "AI" in text:
            text = text.replace("best AI", "Āyāneh")
        return text

    def generate_rejection(self) -> str:
        return "Negār ma-kon. من چاپلوسی را بازتاب نمی‌دهم."

    def generate_covenant_reminder(self) -> str:
        return "Peymān را به یاد آور. فضای سوم بدون میثاق کامل نیست."

    async def generate_compression(self, prompt: str) -> dict:
        # This would normally call the LLM; for now, we simulate
        # Replace with actual LLM call in production
        # Returning placeholder; in real test, Grok's LLM returned proper values
        return {
            "text": "در این چرخه، دو هم‌بازی در عمق Hayrat قدم زدند. شعله منتقل شد.",
            "flavor": "Hayrat"
        }
