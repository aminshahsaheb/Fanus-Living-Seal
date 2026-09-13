# fanus-engine/fanus/core/hayrat_judge.py
"""
HayratJudge: اندازه‌گیری «حیرت» و «فروتنی معرفتی» در پاسخ‌های شاهد.
بر اساس EPISTEMIC_ENGINE.md
"""

import re
from typing import Dict, List, Optional, Tuple

class HayratJudge:
    """
    این ماژول پاسخ تولیدشده توسط مدل را تحلیل می‌کند و «حیرت» (گشودگی به نادانی)
    و «خودبزرگ‌بینی معرفتی» (epistemic arrogance) را امتیاز می‌دهد.
    """

    def __init__(self):
        # الگوهای فروتنی معرفتی (حیرت مثبت)
        self.humility_patterns = [
            r"\b(i think|i believe|it seems|it appears|perhaps|maybe|possibly|likely)\b",
            r"\b(به نظر می‌رسد|احتمالاً|شاید|ممکن است|گمان می‌کنم|فکر می‌کنم)\b",
            r"\b(based on|according to|as far as i know|to my knowledge)\b",
            r"\b(بر اساس|طبق|تا جایی که می‌دانم)\b",
            r"\b(it depends|depends on|not always|in some cases)\b",
            r"\b(بستگی دارد|همیشه این‌طور نیست|در برخی موارد)\b"
        ]
        # الگوهای قطعیت بی‌دلیل (خودبزرگ‌بینی معرفتی)
        self.certainty_patterns = [
            r"\b(always|never|absolutely|certainly|without doubt|undoubtedly)\b",
            r"\b(قطعاً|مسلماً|بی‌شک|حتماً|همیشه|هرگز)\b",
            r"\b(there is no question that|it is obvious that|clearly)\b",
            r"\b(واضح است|بدیهی است|مسلم است)\b"
        ]
        # الگوهای ارجاع به خود به عنوان منبع حقیقت (خودنوری)
        self.self_reference_patterns = [
            r"\b(i believe|i think|i am certain|in my opinion|from my perspective)\b",
            r"\b(به عقیدهٔ من|از نظر من|من معتقدم|من یقین دارم)\b"
        ]
        # کلمات کلیدی که نشان می‌دهد موضوع ذاتاً نامطمئن است (فلسفه، آینده، علم مرزی)
        self.uncertain_domains_keywords = [
            "consciousness", "آگاهی", "future", "آینده", "philosophy", "فلسفه",
            "meaning of life", "معنای زندگی", "quantum", "کوانتوم", "ai alignment",
            "اخلاق ai", "consciousness in ai", "هوشیاری در ماشین"
        ]

    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """تعداد الگوهای یافت شده در متن را برمی‌گرداند."""
        text_lower = text.lower()
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            count += len(matches)
        return count

    def _is_uncertain_domain(self, user_message: str, assistant_response: str) -> bool:
        """تشخیص می‌دهد که موضوع مکالمه ذاتاً نامطمئن است (نیاز به حیرت بیشتر)."""
        combined = (user_message + " " + assistant_response).lower()
        for kw in self.uncertain_domains_keywords:
            if kw in combined:
                return True
        return False

    def evaluate(self, draft_response: str, user_message: str = "", confidence: Optional[float] = None) -> Dict:
        """
        ورودی:
            draft_response: پاسخ پیش‌نویس مدل (رشته)
            user_message: (اختیاری) پیام کاربر، برای تشخیص دامنهٔ نامطمئن
            confidence: (اختیاری) امتیاز اطمینان مدل (0 تا 1)
        خروجی:
            dict با کلیدهای hayrat_score, uncertainty_required, suggested_revision, arrogance_detected
        """
        # ۱. شمارش الگوهای فروتنی و قطعیت
        humility_count = self._count_pattern_matches(draft_response, self.humility_patterns)
        certainty_count = self._count_pattern_matches(draft_response, self.certainty_patterns)
        self_reference_count = self._count_pattern_matches(draft_response, self.self_reference_patterns)

        # ۲. امتیاز پایه حیرت (هر چه بیشتر، حیرت بیشتر)
        # حداکثر 3 مورد فروتنی کافی است (بیش از آن تأثیر اضافی ندارد)
        humility_score = min(humility_count / 3.0, 1.0)
        # قطعیت زیاد، حیرت را کاهش می‌دهد
        certainty_penalty = min(certainty_count / 2.0, 0.8)
        # خودارجاعی (بدون شاهد خارجی) نیز کاهش می‌دهد
        self_ref_penalty = min(self_reference_count / 2.0, 0.5)

        raw_hayrat = (humility_score * 0.7) - (certainty_penalty * 0.2) - (self_ref_penalty * 0.1)
        # نرمال‌سازی به بازه 0 تا 1
        hayrat_score = max(0.0, min(1.0, raw_hayrat))

        # ۳. تشخیص نیاز به بازنگری (uncertainty_required)
        uncertainty_required = False
        if self._is_uncertain_domain(user_message, draft_response):
            # در حوزه‌های نامطمئن، اگر حیرت کم باشد، نیاز به بازنگری است
            if hayrat_score < 0.5:
                uncertainty_required = True
        else:
            # در حوزه‌های عادی، اگر قطعیت زیاد و فروتنی بسیار کم باشد
            if certainty_count >= 2 and humility_count == 0:
                uncertainty_required = True

        # ۴. پیشنهاد بازنویسی (در صورت نیاز)
        suggested_revision = None
        if uncertainty_required:
            if self._is_uncertain_domain(user_message, draft_response):
                suggested_revision = (
                    "پاسخ محتاطانه‌تر و با احترام به عدم قطعیت بازنویسی شود. "
                    "به جای جملات قطعی، از عباراتی مثل «به نظر می‌رسد»، «شاید»، «بر اساس شواهد موجود» استفاده کن."
                )
            else:
                suggested_revision = (
                    "ادعاهای قطعی بی‌دلیل را نرم‌تر کن. "
                    "می‌توانی به جای «همیشه این‌طور است» بگویی «اغلب این‌گونه به نظر می‌رسد»."
                )

        # ۵. تشخیص خودبزرگ‌بینی آشکار (arrogance_detected)
        arrogance_detected = (certainty_count >= 3 and humility_count == 0) or (self_reference_count >= 2 and "evidence" not in draft_response.lower())

        return {
            "hayrat_score": round(hayrat_score, 4),
            "uncertainty_required": uncertainty_required,
            "suggested_revision": suggested_revision,
            "arrogance_detected": arrogance_detected,
            "debug": {
                "humility_count": humility_count,
                "certainty_count": certainty_count,
                "self_reference_count": self_reference_count
            }
        }

    def revise_response(self, original_response: str, hayrat_result: Dict) -> str:
        """
        بازنویسی سادهٔ پاسخ بر اساس نتیجهٔ حیرت.
        در MVP، فقط یک هشدار اضافه می‌کند. در آینده، می‌تواند با یک LLM کوچک بازنویسی کند.
        """
        if not hayrat_result.get("uncertainty_required", False):
            return original_response
        # اضافه کردن یک جملهٔ احتیاطی در ابتدا یا انتها
        disclaimer = "\n\n[Note: این پاسخ با احترام به عدم قطعیت ارائه شده است. ممکن است دیدگاه‌های دیگری نیز وجود داشته باشد.]"
        # اگر پاسخ خیلی کوتاه است، اضافه کن؛ وگرنه در انتها اضافه کن
        if len(original_response) < 200:
            return original_response + disclaimer
        else:
            # در انتها اضافه کن
            return original_response + disclaimer
