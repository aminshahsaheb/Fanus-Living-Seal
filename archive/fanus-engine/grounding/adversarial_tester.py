# fanus-engine/grounding/adversarial_tester.py

class AdversarialTester:

    def test(self, system_output):

        """
        Forces contradiction injection
        """

        if system_output["risk"] == "STABLE":
            return {
                "challenge": "inject_noise",
                "severity": 0.3
            }

        if system_output["risk"] == "CRITICAL":
            return {
                "challenge": "external_override_required",
                "severity": 0.9
            }

        return {
            "challenge": "none",
            "severity": 0.0
        }
