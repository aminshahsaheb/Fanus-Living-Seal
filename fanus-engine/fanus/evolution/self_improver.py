import difflib
import os
import copy


class SelfImprover:

    def __init__(self, safety_mode=True):
        self.safety_mode = safety_mode

    # =========================
    # 🧠 1. EVALUATE SYSTEM
    # =========================
    def evaluate(self, history):
        """
        ساده‌ترین مدل performance scoring
        """

        if not history:
            return 0.5

        success = sum(1 for h in history if h.get("decision") == "ALLOW_CONFIDENT")
        caution = sum(1 for h in history if h.get("decision") == "ALLOW_WITH_CAUTION")
        block = sum(1 for h in history if h.get("decision") == "BLOCK")

        score = (success * 1.0 + caution * 0.5 - block * 1.0) / len(history)

        return max(0.0, min(1.0, score))

    # =========================
    # 🧠 2. PROPOSE IMPROVEMENT
    # =========================
    def propose_patch(self, file_path):
        """
        نسخه ساده: بهبود logging + safety guard
        """

        if not os.path.exists(file_path):
            return {"status": "error", "reason": "file not found"}

        with open(file_path, "r") as f:
            code = f.read()

        improved_code = self._inject_safety_hook(code)

        diff = list(difflib.unified_diff(
            code.splitlines(),
            improved_code.splitlines(),
            fromfile="current",
            tofile="improved",
            lineterm=""
        ))

        return {
            "status": "proposed",
            "diff": "\n".join(diff),
            "improved_code": improved_code
        }

    # =========================
    # 🧠 3. APPLY IMPROVEMENT SAFELY
    # =========================
    def apply(self, file_path, improved_code):

        if self.safety_mode:
            if "rm -rf" in improved_code:
                return {"status": "blocked", "reason": "dangerous pattern"}

        backup = file_path + ".bak"

        with open(file_path, "r") as f:
            original = f.read()

        # backup
        with open(backup, "w") as f:
            f.write(original)

        # write new version
        with open(file_path, "w") as f:
            f.write(improved_code)

        return {
            "status": "applied",
            "backup": backup
        }

    # =========================
    # 🧠 4. INTERNAL IMPROVEMENT RULES
    # =========================
    def _inject_safety_hook(self, code):
        """
        اینجا Fanus یاد می‌گیرد خودش را امن‌تر کند
        """

        if "Safety" in code:
            return code

        hook = """

# 🧠 FANUS SELF-IMPROVEMENT HOOK
def safety_guard(event):
    if event.get("intent") == "danger":
        return False
    return True

"""

        return code + hook
