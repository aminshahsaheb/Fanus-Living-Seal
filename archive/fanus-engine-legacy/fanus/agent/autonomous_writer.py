import subprocess
import difflib
import os

class AutonomousWriter:

    def __init__(self, safety_mode=True):
        self.safety_mode = safety_mode

    def propose_change(self, file_path, new_content):

        if not os.path.exists(file_path):
            return {"status": "error", "reason": "file not found"}

        with open(file_path, "r") as f:
            old_content = f.read()

        diff = list(difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile="current",
            tofile="proposed",
            lineterm=""
        ))

        return {
            "status": "proposed",
            "diff": "\n".join(diff)
        }

    def apply_change(self, file_path, new_content):

        if self.safety_mode:
            # 🔒 safety gate
            if "import os" in new_content and "rm" in new_content:
                return {"status": "blocked", "reason": "unsafe pattern detected"}

        backup_path = file_path + ".bak"

        # backup first
        if os.path.exists(file_path):
            subprocess.run(f"cp {file_path} {backup_path}", shell=True)

        # write new version
        with open(file_path, "w") as f:
            f.write(new_content)

        return {
            "status": "applied",
            "backup": backup_path
        }
