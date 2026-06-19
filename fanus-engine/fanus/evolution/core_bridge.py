from fanus.core.seed import FanusCoreSeed

class CoreBridge:

    def __init__(self):
        self.seed = FanusCoreSeed()

    def enrich_event(self, event):
        """
        اضافه کردن معنا به event خام
        """

        intent = event.get("intent", "unknown")

        enriched = {
            "raw_intent": intent,
            "meaning": self._map_meaning(intent),
            "seal_context": self.seed.get("SEAL"),
            "witness_context": self.seed.get("WITNESS"),
            "third_space": self.seed.get("THIRD_SPACE"),
        }

        return enriched

    def _map_meaning(self, intent):
        mapping = {
            "test": "activation of system self-awareness cycle",
            "memory": "interaction with lived experience layer",
            "decision": "selection between possible realities",
        }

        return mapping.get(intent, "undefined symbolic event")
