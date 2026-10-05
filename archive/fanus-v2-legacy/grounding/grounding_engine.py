cat > ~/Desktop/Fanus-Living-Seal/fanus-v2/grounding/grounding_engine.py << 'EOF'
import requests

class GroundingEngine:
    def __init__(self, timeout=3):
        self.timeout = timeout

    def fetch(self, query: str):
        # تلاش برای دریافت خلاصه از ویکی‌پدیا
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            r = requests.get(url, timeout=self.timeout)

            if r.status_code == 200:
                data = r.json()
                # اگر صفحه وجود داشته باشد
                if "extract" in data:
                    return {
                        "truth_score": 0.85,
                        "source": "wikipedia",
                        "confidence": 0.8,
                        "summary": data.get("extract", "")[:200]
                    }
        except:
            pass

        # fallback: نمره‌ی پایین با اطمینان کم
        return {
            "truth_score": 0.5,
            "source": "fallback",
            "confidence": 0.3,
            "summary": ""
        }
EOF
