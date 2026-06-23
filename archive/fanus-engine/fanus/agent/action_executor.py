import subprocess
import os

class ActionExecutor:

    def execute(self, decision, context):

        if decision == "ALLOW":
            return self._noop("allowed but no action")

        if decision == "ALLOW_CONFIDENT":
            return self._safe_git_status()

        if decision == "ALLOW_WITH_CAUTION":
            return self._safe_diff()

        if decision == "BLOCK":
            return self._block_action()

        return {"status": "unknown"}

    def _safe_git_status(self):
        return self._run("git status")

    def _safe_diff(self):
        return self._run("git diff --name-only")

    def _block_action(self):
        return {"status": "blocked", "reason": "risk threshold"}

    def _noop(self, msg):
        return {"status": "noop", "msg": msg}

    def _run(self, cmd):
        try:
            result = subprocess.check_output(
                cmd,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True
            )
            return {"status": "ok", "output": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
