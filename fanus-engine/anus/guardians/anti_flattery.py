class AntiFlatteryShield:
    def validate(self, user_message: str) -> bool:
        # Simple heuristic: if message contains excessive praise without substance, flag it.
        flattery_keywords = ["best", "greatest", "amazing", "perfect", "genius", "wonderful", "فوق‌العاده‌ای", "بهترین"]
        score = sum(1 for word in flattery_keywords if word in user_message.lower())
        # Allow minor compliments, but if too many, reject
        return score < 3
