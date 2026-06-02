from pathlib import Path

ROOT = Path(".")

required_paths = [
    "README.md",
    "ANRP_STANDARD.md",
    "intent/INTENT_GRAPH.md",
    "intent/COLLAPSE_DEFINITION.md",
    "concept-map/SYSTEM_GRAPH.md",
    "concept-map/SEMANTIC_GRAVITY.md",
    "failure/KNOWN_FAILURES.md",
    "questions/OPEN_QUESTIONS.md",
    "validation/RECONSTRUCTION_TEST.md",
    "validation/AI_READER_PROTOCOL.md",
]

missing = []

for p in required_paths:
    if not Path(p).exists():
        missing.append(p)

if missing:
    print("\nANRP VIOLATIONS:\n")
    for item in missing:
        print(f" - {item}")
    raise SystemExit(1)

print("ANRP STRUCTURE VALID")
