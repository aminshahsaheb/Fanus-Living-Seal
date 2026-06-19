import os
import subprocess


class FanusGitGuard:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def check_repo_root(self):
        try:
            root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"]
            ).decode().strip()

            cwd = os.getcwd()

            if root not in cwd:
                self.errors.append("NOT_IN_REPO_ROOT")
                return False

            return True

        except Exception:
            self.errors.append("NOT_A_GIT_REPO")
            return False

    def check_status(self):
        try:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"]
            ).decode().strip()

            if status == "":
                self.warnings.append("CLEAN_WORKING_TREE")

            return status

        except Exception as e:
            self.errors.append(str(e))
            return ""

    def check_untracked(self):
        try:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"]
            ).decode().splitlines()

            bad_paths = []

            for line in status:
                if line.startswith("??"):
                    path = line[3:]

                    if path.startswith("../"):
                        bad_paths.append(path)

            if bad_paths:
                self.errors.append("OUTSIDE_REPO_FILES_DETECTED")

            return bad_paths

        except Exception:
            return []

    def pre_commit_check(self):
        root_ok = self.check_repo_root()
        status = self.check_status()
        bad = self.check_untracked()

        return {
            "repo_root_ok": root_ok,
            "status": status,
            "bad_paths": bad,
            "errors": self.errors,
            "warnings": self.warnings
        }

    def safe_commit(self, message="auto commit"):

        report = self.pre_commit_check()

        if report["errors"]:
            print("🛑 BLOCKED BY FANUS GIT GUARD")
            print(report)
            return False

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", message])

        print("✅ SAFE COMMIT DONE")
        return True

    def safe_push(self):

        try:
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("🚀 SAFE PUSH DONE")
            return True

        except Exception as e:
            print("🛑 PUSH FAILED")
            print(str(e))
            return False
