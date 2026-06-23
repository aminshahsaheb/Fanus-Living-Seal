import importlib
import os
import sys
import subprocess


class FanusAutoHeal:

    def __init__(self):

        self.repair_log = []

    # =========================
    # 🔍 CHECK MODULE IMPORT
    # =========================
    def check_import(self, module_name):

        try:
            importlib.import_module(module_name)
            return {"ok": True}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    # =========================
    # 🧠 FIX PYTHONPATH
    # =========================
    def fix_pythonpath(self):

        cwd = os.getcwd()

        if cwd not in sys.path:
            sys.path.insert(0, cwd)

            self.repair_log.append("added_cwd_to_pythonpath")

        return {"status": "pythonpath_updated"}

    # =========================
    # 🧩 FIND MISSING MODULE
    # =========================
    def find_missing_hint(self, error_msg):

        if "No module named" in error_msg:
            missing = error_msg.split("No module named")[-1].strip().replace("'", "")
            return missing

        return None

    # =========================
    # 🔧 AUTO HEAL IMPORT
    # =========================
    def heal_import(self, module_name):

        result = self.check_import(module_name)

        if result["ok"]:
            return {"status": "ok"}

        error = result["error"]

        missing = self.find_missing_hint(error)

        self.fix_pythonpath()

        # try again
        retry = self.check_import(module_name)

        if retry["ok"]:
            return {
                "status": "healed",
                "module": module_name
            }

        return {
            "status": "failed",
            "missing": missing,
            "error": error
        }

    # =========================
    # 🔁 FULL SYSTEM HEAL
    # =========================
    def heal_system(self, core_modules):

        results = []

        for module in core_modules:

            res = self.heal_import(module)

            results.append({
                "module": module,
                "result": res
            })

        return {
            "status": "complete",
            "results": results,
            "repairs": self.repair_log
        }

    # =========================
    # 🚀 SAFE RECOVERY MODE
    # =========================
    def recovery_mode(self, test_module="fanus.runtime.loop"):

        print("🛠 AUTO HEAL INITIATED")

        result = self.heal_import(test_module)

        if result["status"] == "healed":
            print("✅ SYSTEM RECOVERED")

        else:
            print("🛑 HEAL FAILED")

        return result
