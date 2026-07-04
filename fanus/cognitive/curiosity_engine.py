import time
from fanus.memory.persistence import PersistenceLayer


class CuriosityEngine:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.questions = self.persistence.get("curiosity", [])

    def generate(self, topic, context=""):
        templates = [
            "چرا " + topic + " اینگونه عمل می‌کند؟",
            "تفاوت " + topic + " با موارد مشابه چیست؟",
            "آیا " + topic + " می‌تواند بهتر شود؟",
            "منشأ " + topic + " چیست؟",
            "آینده " + topic + " چه خواهد بود؟"
        ]
        questions = [{
            "id": len(self.questions) + i + 1,
            "question": q,
            "topic": topic,
            "answered": False,
            "created": time.time()
        } for i, q in enumerate(templates)]
        self.questions.extend(questions)
        self._save()
        return questions

    def unanswered(self):
        return [q for q in self.questions if not q["answered"]]

    def answer(self, question_id):
        for q in self.questions:
            if q["id"] == question_id:
                q["answered"] = True
                self._save()
                return q
        return None

    def _save(self):
        self.persistence.save({"curiosity": self.questions})

    def stats(self):
        return {
            "total": len(self.questions),
            "unanswered": len(self.unanswered())
        }