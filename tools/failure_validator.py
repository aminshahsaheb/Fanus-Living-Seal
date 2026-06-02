from pathlib import Path

content = Path(
    "failure/KNOWN_FAILURES.md"
).read_text(encoding="utf-8")

required = [
    "Assumption",
    "Failure Risk",
    "Impact",
    "Status",
]

missing = []

for r in required:
    if r not in content:
        missing.append(r)

if missing:
    print("FAILURE REGISTRY INVALID")
    print(missing)
    raise SystemExit(1)

print("FAILURE REGISTRY VALID")
