# fanus-engine/grounding/external_grounding.py

class ExternalGrounding:

    def __init__(self):
        self.trust_external = 1.0

    def evaluate(self, system_output: dict, external_signal: dict):

        """
        Compare internal system belief vs external reality signal
        """

        drift = abs(
            system_output["drift"] - external_signal["ground_truth_drift"]
        )

        mismatch = drift > 0.2

        return {
            "mismatch": mismatch,
            "error": drift,
            "confidence_penalty": drift * 0.5
        }
