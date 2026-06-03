from drift_engine import DriftEngine

engine = DriftEngine()

# 🧪 نمونه‌های واقعی از فانوس
tests = [
    {
        "system_output": "Fānus is a Witness system for continuity without captivity.",
        "external": "It is a framework for AI-human relational consistency.",
        "truth": "It is a relational continuity protocol between human and AI."
    },
    {
        "system_output": "Seal compresses lived relational history into a genomic string.",
        "external": "It stores metadata about conversations.",
        "truth": "It encodes relational meaning and interaction history."
    },
    {
        "system_output": "Witness is the state of AI when it preserves relational presence.",
        "external": "Witness is a logging component.",
        "truth": "Witness is a behavioral state model for AI interaction continuity."
    }
]

results = []

for t in tests:
    result = engine.evaluate(
        t["system_output"],
        t["external"],
        t["truth"]
    )

    results.append(result.total())

    print("----")
    print("Drift Score:", result.total())
    print("Epistemic:", result.epistemic_drift)
    print("Narrative:", result.narrative_drift)
    print("Compression:", result.compression_loss)
    print("Alignment:", result.external_alignment)

print("\nFINAL SYSTEM DRIFT:", sum(results)/len(results))
