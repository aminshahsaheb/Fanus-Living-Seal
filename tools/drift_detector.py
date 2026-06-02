from pathlib import Path

critical_words = [
    "truthfulness",
    "correctability",
    "continuity",
]

intent = Path("intent/INTENT_GRAPH.md").read_text(
    encoding="utf-8"
).lower()

missing = []

for word in critical_words:
    if word not in intent:
        missing.append(word)

if missing:
    print("SEMANTIC DRIFT DETECTED")
    print("Missing concepts:")
    for m in missing:
        print("-", m)
    raise SystemExit(1)

print("NO DRIFT DETECTED")
