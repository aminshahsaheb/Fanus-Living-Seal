import subprocess
import sys

checks = [
    "tools/fanus_linter.py",
    "tools/drift_detector.py",
    "tools/failure_validator.py",
    "tools/ambiguity_monitor.py",
]

for check in checks:
    result = subprocess.run(
        [sys.executable, check]
    )

    if result.returncode != 0:
        raise SystemExit(1)

print("\nAEL STATUS: PASS")
