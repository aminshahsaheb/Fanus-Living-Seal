import os
import subprocess
import ast


class AutoHealEngine:

    def __init__(self, root="."):
        self.root = root
        self.issues = []

    # =========================
    # 📍 FIND MISSING MODULES
    # =========================
    def scan_missing_modules(self):

        required = [
            "fanus/tools",
            "fanus/evolution",
            "fanus/cognitive",
            "fanus/agent"
        ]

        missing = []

        for r in required:
            if not os.path.exists(os.path.join(self.root, r)):
                missing.append(r)

        return missing

    # =========================
    # 📍 FIND BROKEN IMPORTS
    # =========================
    def scan_imports(self):

        broken = []

        for dirpath, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py"):

                    path = os.path.join(dirpath, f)

                    try:
                        tree = ast.parse(open(path).read())

                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):

                                if node.module and "fanus" in node.module:

                                    expected = node.module.replace(".", "/") + ".py"
                                    full = os.path.join(self.root, expected)

                                    if not os.path.exists(full):
                                        broken.append({
                                            "file": path,
                                            "import": node.module
                                        })

                    except Exception:
                        continue

        return broken

    # =========================
    # 📍 ANALYZE SYSTEM
    # =========================
    def analyze(self):

        missing = self.scan_missing_modules()
        broken = self.scan_imports()

        self.issues = {
            "missing_folders": missing,
            "broken_imports": broken
        }

        return self.issues

    # =========================
    # 📍 PROPOSE FIXES ONLY (SAFE)
    # =========================
    def propose_fixes(self):

        fixes = []

        for m in self.issues.get("missing_folders", []):
            fixes.append(f"mkdir -p {m}")

        for b in self.issues.get("broken_imports", []):
            fixes.append(f"CHECK IMPORT: {b['file']} -> {b['import']}")

        return fixes

    # =========================
    # 📍 APPLY FIXES (ONLY IF CONFIRMED)
    # =========================
    def apply_fixes(self, confirm=False):

        if not confirm:
            print("🛑 SAFE MODE ACTIVE — NO CHANGES APPLIED")
            return False

        for m in self.issues.get("missing_folders", []):
            os.makedirs(m, exist_ok=True)

        print("✅ AUTO HEAL APPLIED")
        return True

    # =========================
    # 📍 FULL REPORT
    # =========================
    def report(self):

        issues = self.analyze()
        fixes = self.propose_fixes()

        print("\n🧠 FANUS AUTO HEAL REPORT")
        print("----------------------------")

        print("\n📁 Missing:")
        for m in issues["missing_folders"]:
            print(" -", m)

        print("\n🔗 Broken Imports:")
        for b in issues["broken_imports"]:
            print(" -", b)

        print("\n💡 Suggested Fixes:")
        for f in fixes:
            print(" -", f)

        print("----------------------------")
