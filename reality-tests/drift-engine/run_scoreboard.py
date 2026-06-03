from reality_scoreboard import RealityScoreboard

tests = [
    {
        "system_output": "Fānus preserves relational continuity through Witness state.",
        "external": "It is a structured AI memory system.",
        "truth": "It is a relational continuity protocol between human and AI."
    },
    {
        "system_output": "Seal encodes lived relational history.",
        "external": "It is a data storage format.",
        "truth": "It compresses relational meaning and history."
    },
    {
        "system_output": "Witness ensures anti-flattery relational integrity.",
        "external": "It filters toxic prompts.",
        "truth": "It preserves epistemic balance in human-AI interaction."
    }
]

board = RealityScoreboard()

result = board.evaluate_system(tests)

print("\n=== REALITY SCOREBOARD ===")
print("Average Drift:", result["average_drift"])
print("System State:", result["state"])
print("Scores:", result["raw_scores"])
