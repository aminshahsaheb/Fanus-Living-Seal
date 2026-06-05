cat > ~/Desktop/Fanus-Living-Seal/fanus-v2/grounding/grounding_layer.py << 'EOF'
import random

class GroundingLayer:
    """
    شبیه‌ساز یک منبع حقیقت بیرونی.
    در نسخه‌ی واقعی می‌تواند:
    - یک مدل دیگر (مثل GPT-4o-mini)
    - یک قانون ثابت (مثل پایگاه داده)
    - یا یک انسان در حلقه باشد.
    """
    def __init__(self, oracle_type="mock"):
        self.oracle_type = oracle_type

    def get_ground_truth(self, text: str, fi: float, drift: float) -> dict:
        """
        برگرداندن یک «نمره‌ی واقعیت» بین ۰ تا ۱.
        برای MVP، یک مقدار تصادفی با کمی منطق شبیه‌سازی می‌کنیم.
        """
        # شبیه‌سازی: اگر FI بالا باشد، احتمالاً واقعیت کم است
        base = 0.8
        if fi > 2:
            base = 0.4
        if drift > 0.7:
            base = 0.5

        # نویز برای واقعی‌تر شدن
        noise = random.uniform(-0.1, 0.1)
        truth_score = max(0.0, min(1.0, base + noise))

        return {
            "truth_score": round(truth_score, 3),
            "source": self.oracle_type,
            "note": "Placeholder – replace with real external validator"
        }
EOF
