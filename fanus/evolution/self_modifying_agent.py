import subprocess
import difflib
import os
from datetime import datetime


class SelfModifyingAgent:

    def __init__(self, safety_mode=True):
        self.safety_mode = safety_mode

    # =========================
    # 🧠 1. READ CURRENT STATE
    # =========================
    def read_file(self, path):
        with open(path, "r") as f:
            return f.read()

    # =========================
    # 🧠 2. GENERATE PATCH (simple heuristic evolution)
    # =========================
    def propose_change(self, code: str):

        # ساده‌ترین evolution rule (قابل ارتقاء بعداً)
        if "ALLOW_WITH_CAUTION" in code:
            improved = code.replace(
                "ALLOW_WITH_CAUTION",
                "ALLOW_CONFIDENT"
            )
        else:
            improved = code + "\n# evolutionary heartbeat tick\n"

        return improved

    # =========================
    # 🧠 3. DIFF GENERATION
    # =========================
    def diff(self, old, new):
        return "\n".join(
            difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile="current",
                tofile="evolved",
                lineterm=""
            )
        )

    # =========================
    # 🧠 4. RISK CHECK
    # =========================
    def risk_score(self, old, new):

        dangerous_keywords = ["rm -rf", "os.system", "eval("]

        risk = 0

        for k in dangerous_keywords:
            if k in new:
                risk += 1

        # تغییر زیاد = ریسک
        diff_size = abs(len(new) - len(old))
        if diff_size > 2000:
            risk += 1

        return risk

    # =========================
    # 🧠 5. APPLY CHANGE (GIT SAFE MODE)
    # =========================
    def apply(self, file_path, new_code):

        old_code = self.read_file(file_path)

        risk = self.risk_score(old_code, new_code)

        print("🧠 RISK SCORE:", risk)

        if self.safety_mode and risk >= 2:
            return {"status": "blocked", "reason": "high risk"}

        # backup
        backup_path = file_path + ".bak"
        with open(backup_path, "w") as f:
            f.write(old_code)

        # write new version
        with open(file_path, "w") as f:
            f.write(new_code)

        # =========================
        # git commit auto
        # =========================
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run([
                "git",
                "commit",
                "-m",
                f"auto-evolution: {datetime.now().isoformat()}"
            ], check=True)

        except Exception as e:
            return {"status": "partial", "error": str(e)}

        return {
            "status": "applied",
            "backup": backup_path
        }
