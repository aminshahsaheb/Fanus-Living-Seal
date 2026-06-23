import importlib
import os
import subprocess


class FanusSystemIntegrationProtocol:

    def __init__(self):
        self.required_modules = [
            "fanus.runtime.loop",
            "fanus.evolution.evolution_engine",
            "fanus.cognitive.cognitive_state",
            "fanus.cognitive.identity_autonomy_core",
            "fanus.cognitive.collapse_resistance_core",
        ]

        self.status = {
            "imports_ok": False,
            "git_clean": False,
            "runtime_ready": False
        }

    # =========================
    # 🔍 IMPORT CHECK
    # =========================
    def check_imports(self):

        failed = []

        for module in self.required_modules:
            try:
                importlib.import_module(module)
            except Exception as e:
                failed.append((module, str(e)))

        self.status["imports_ok"] = len(failed) == 0

        return {
            "ok": self.status["imports_ok"],
            "failed": failed
        }

    # =========================
    # 🧬 GIT STATE CHECK
    # =========================
    def check_git_state(self):

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )

            dirty = result.stdout.strip() != ""

            self.status["git_clean"] = not dirty

            return {
                "clean": not dirty,
                "raw": result.stdout.strip()
            }

        except Exception as e:
            return {
                "clean": False,
                "error": str(e)
            }

    # =========================
    # ⚙️ RUNTIME VALIDATION
    # =========================
    def validate_runtime(self):

        import_check = self.check_imports()
        git_check = self.check_git_state()

        runtime_ready = import_check["ok"] and git_check.get("clean", False)

        self.status["runtime_ready"] = runtime_ready

        return {
            "runtime_ready": runtime_ready,
            "imports": import_check,
            "git": git_check
        }

    # =========================
    # 🚀 SAFE BOOT
    # =========================
    def safe_boot(self, entry_point):

        validation = self.validate_runtime()

        if not validation["runtime_ready"]:
            print("🛑 SIP BLOCKED BOOT — SYSTEM NOT READY")

            print("\n📦 IMPORT STATUS:", validation["imports"])
            print("\n🧬 GIT STATUS:", validation["git"])

            return {
                "status": "blocked",
                "reason": validation
            }

        print("🚀 SIP OK — BOOTING FANUS SYSTEM")

        return entry_point()
