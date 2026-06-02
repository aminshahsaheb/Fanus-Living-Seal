from pathlib import Path

zones = [
    "cal/clarity",
    "cal/interpretability",
    "cal/open",
]

missing = []

for z in zones:
    if not Path(z).exists():
        missing.append(z)

if missing:
    print("CAL VIOLATION")
    print(missing)
    raise SystemExit(1)

print("CAL STRUCTURE VALID")
