import time


class QuestionGenerator:

    TYPES = {
        "causal": "چرا ",
        "comparative": "تفاوت ",
        "hypothetical": "اگر ",
        "evaluative": "آیا ",
        "predictive": "آینده "
    }

    def __init__(self):
        self.history = []

    def generate(self, topic, belief_type="FACT", confidence=1.0):
        questions = []
        if confidence < 0.7:
            questions.append({"type": "causal", "question": "چرا " + topic + " هنوز اثبات نشده؟"})
            questions.append({"type": "evaluative", "question": "آیا شواهد کافی برای " + topic + " وجود دارد؟"})
        if belief_type == "HYPOTHESIS":
            questions.append({"type": "hypothetical", "question": "اگر " + topic + " درست باشد چه نتایجی دارد؟"})
        if belief_type == "FACT":
            questions.append({"type": "predictive", "question": "آینده تحقیقات " + topic + " چیست؟"})
            questions.append({"type": "comparative", "question": "تفاوت " + topic + " با نظریه‌های مشابه چیست؟"})
        result = {
            "topic": topic,
            "questions": questions,
            "timestamp": time.time()
        }
        self.history.append(result)
        return result

    def stats(self):
        total = sum(len(r["questions"]) for r in self.history)
        return {"topics": len(self.history), "total_questions": total}