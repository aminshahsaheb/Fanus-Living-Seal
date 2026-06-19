import os
import ast
import subprocess


class StructureRepairEngine:

    def __init__(self, root="."):
        self.root = root
        self.issues = []
        self.fixes = []

    # =========================
    # 📍 1. CHECK FILE STRUCTURE
    # =========================
    def scan_structure(self):

        expected_packages = [
            "fanus",
            "fanus/tools",
            "fanus/evolution",
            "fanus/cognitive",
            "fanus/agent"
        ]

        missing = []

        for path in expected_packages:
            full = os.path.join(self.root, path)
            if not os.path.exists(full):
                missing.append(path)

        if missing:
            self.issues.append({
                "type": "MISSING_FOLDERS",
                "data": missing
            })

        return missing

    # =========================
    # 📍 2. CHECK PYTHON FILES
    # =========================
    def scan_imports(self):

        broken_imports = []

        for dirpath, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(".py"):

                    full_path = os.path.join(dirpath, file)

                    try:
                        with open(full_path, "r") as f:
                            tree = ast.parse(f.read(), filename=full_path)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):

                                if node.module and "fanus" in node.module:

                                    expected_path = node.module.replace(".", "/") + ".py"
                                    abs_path = os.path.join(self.root, expected_path)

                                    if not os.path.exists(abs_path):
                                        broken_imports.append({
                                            "file": full_path,
                                            "import": node.module
                                        })

                    except Exception:
                        continue

        if broken_imports:
            self.issues.append({
                "type": "BROKEN_IMPORTS",
                "data": broken_imports
            })

        return broken_imports

    # =========================
    # 📍 3. CHECK GIT STATE
    # =========================
    def git_state(self):

        try:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"]
            ).decode().splitlines()

            untracked = [s for s in status if s.startswith("??")]

            return {
                "untracked": untracked
            }

        except Exception:
            return {}

    # =========================
    # 📍 4. ANALYZE STRUCTURE HEALTH
    # =========================
    def analyze(self):

        structure = self.scan_structure()
        imports = self.scan_imports()
        git = self.git_state()

        return {
            "missing_folders": structure,
            "broken_imports": imports,
            "git": git,
            "status": "OK" if not self.issues else "ISSUES_FOUND"
        }

    # =========================
    # 📍 5. SAFE FIX (NO AUTO DELETE)
    # =========================
    def suggest_fixes(self):

        fixes = []

        for issue in self.issues:

            if issue["type"] == "MISSING_FOLDERS":
                for folder in issue["data"]:
                    fixes.append(f"mkdir -p {folder}")

            if issue["type"] == "BROKEN_IMPORTS":
                for imp in issue["data"]:
                    fixes.append(
                        f"CHECK IMPORT: {imp['file']} -> {imp['import']}"
                    )

        self.fixes = fixes
        return fixes

    # =========================
    # 📍 6. PRINT REPORT
    # =========================
    def report(self):

        analysis = self.analyze()
        fixes = self.suggest_fixes()

        print("\n🧠 FANUS STRUCTURE REPAIR REPORT")
        print("----------------------------------")
        print("Status:", analysis["status"])

        print("\n📁 Missing Folders:")
        for m in analysis["missing_folders"]:
            print(" -", m)

        print("\n🔗 Broken Imports:")
        for b in analysis["broken_imports"]:
            print(" -", b)

        print("\n💡 Suggested Fixes:")
        for f in fixes:
            print(" -", f)

        print("\n----------------------------------")
