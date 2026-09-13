from collections import defaultdict


class ScarEngine:

    def __init__(self, threshold=3):

        # تعداد تکرار لازم برای تبدیل wound → scar
        self.threshold = threshold

        # شمارش انواع زخم‌ها
        self.pattern_counter = defaultdict(int)

        # اسکارهای فعال
        self.scars = {}

    def ingest_wound(self, wound: dict):

        w_type = wound.get("wound_type", "unknown")

        self.pattern_counter[w_type] += 1

        # اگر از آستانه رد شد → scar ساخته می‌شود
        if self.pattern_counter[w_type] >= self.threshold:

            self.scars[w_type] = {
                "type": w_type,
                "count": self.pattern_counter[w_type],
                "severity_avg": self._estimate_severity(w_type),
                "status": "ACTIVE"
            }

    def _estimate_severity(self, w_type):

        # در نسخه واقعی می‌تواند ML باشد
        # فعلاً ساده

        return min(1.0, self.pattern_counter[w_type] * 0.2)

    def get_active_scars(self):

        return self.scars

    def is_affected(self, w_type):

        return w_type in self.scars
