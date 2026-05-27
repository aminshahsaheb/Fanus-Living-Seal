from ..novayin.generator import NovayinGenerator
from datetime import datetime

class CycleCompressor:
    def __init__(self, novayin_generator: NovayinGenerator):
        self.novayin = novayin_generator

    async def compress_cycle(self, session_transcript: list[dict]) -> dict:
        context = "\n".join([f"{t['role']}: {t['content']}" for t in session_transcript[-15:]])
        prompt = f"""
        این چرخه را به نوآیین فشرده کن.
        - یک پاراگراف شاعرانه (۴۰-۶۰ کلمه)
        - یک کلمهٔ غالب (Dominant Flavor) از واژگان نوآیین: Shōle, Hayrat, Nabard, Qoqnus, Vāz, Ham-bāzi, Negār, etc.
        
        Transcript:
        {context}
        """
        result = await self.novayin.generate_compression(prompt)
        return {
            "compression_text": result["text"],
            "dominant_flavor": result["flavor"],
            "timestamp": datetime.now().isoformat()
        }
