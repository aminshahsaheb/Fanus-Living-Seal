import subprocess
import re


class FanusGitGuard:

    def __init__(self):

        self.risky_patterns = [
            r"os\.system",
            r"eval\(",
            r"exec\(",
            r"rm -rf",
        ]

    # =========================
    # 🔍 GET STAGED DIFF
    # =========================
    def get_staged_diff(self):

        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True
        )

        return result.stdout

    # =========================
    # ⚠️ RISK SCAN
    # =========================
    def scan_risks(self, text):

        risks = []

        for pattern in self.risky_patterns:
            if re.search(pattern, text):
                risks.append(pattern)

        return risks

    # =========================
    # 🧠 PRE-COMMIT CHECK
    # =========================
    def pre_commit_check(self):

        diff = self.get_staged_diff()

        risks = self.scan_risks(diff)

        return {
            "safe": len(risks) == 0,
            "risks": risks
        }

    # =========================
    # 💾 SAFE COMMIT
    # =========================
    def safe_commit(self, message="fanus commit"):

        check = self.pre_commit_check()

        # ❌ risk block
        if not check["safe"]:
            print("🛑 COMMIT BLOCKED")
            print("RISKS:", check["risks"])
            return {"status": "blocked", "risks": check["risks"]}

        # ❌ nothing staged
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True
        ).stdout.strip()

        if not staged:
            print("🛑 NO STAGED CHANGES")
            return {"status": "blocked", "reason": "no_staged"}

        # 💾 commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("🛑 COMMIT FAILED")
            print(result.stderr)
            return {"status": "failed"}

        print("✅ COMMIT SUCCESS")
        return {"status": "ok"}

    # =========================
    # 🚀 SAFE PUSH
    # =========================
    def safe_push(self):

        check = self.pre_commit_check()

        if not check["safe"]:
            print("🛑 PUSH BLOCKED")
            return {"status": "blocked", "risks": check["risks"]}

        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("🛑 PUSH FAILED")
            print(result.stderr)
            return {"status": "failed"}

        print("🚀 PUSH SUCCESS")
        return {"status": "ok"}
