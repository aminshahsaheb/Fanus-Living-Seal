from control.thresholds import THRESHOLDS
import json
import os

class SystemEvolver:
    def __init__(self, thresholds_path=None):
        self.thresholds_path = thresholds_path or os.path.join(
            os.path.dirname(__file__), "..", "control", "thresholds.py"
        )

    def apply_new_thresholds(self, new_thresholds):
        if not new_thresholds:
            return False
        # به‌روزرسانی فایل thresholds.py
        content = f"""THRESHOLDS = {new_thresholds}
"""
        with open(self.thresholds_path, "w") as f:
            f.write(content)
        # به‌روزرسانی کش در ماژول (importlib.reload)
        import importlib
        import control.thresholds
        importlib.reload(control.thresholds)
        return True
