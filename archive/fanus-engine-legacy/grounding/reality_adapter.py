# fanus-engine/grounding/reality_adapter.py

class RealityAdapter:

    def __init__(self):
        pass

    def fetch_external_signal(self, context: dict):

        """
        This simulates external reality input.
        In real version → API / benchmarks / human labels
        """

        return {
            "ground_truth_drift": context.get("reference_drift", 0.5),
            "external_label": context.get("label", "UNKNOWN")
        }
