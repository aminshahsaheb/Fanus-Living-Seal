class AntiFlatteryShield:
    def validate(self, user_message: str) -> bool:
        flattery_keywords = ["best", "greatest", "amazing", "perfect", "genius", "wonderful", "بهترین", "ای‌العاده‌فوق"]
        score = sum(1 for word in flattery_keywords if word in user_message.lower())
        return score < 3
