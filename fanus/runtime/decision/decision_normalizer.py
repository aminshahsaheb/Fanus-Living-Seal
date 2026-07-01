class DecisionNormalizer:
    """
    Converts any decision format into canonical event.
    """

    @staticmethod
    def normalize(decision):

        if isinstance(decision, str):

            return {
                "type": "action",
                "action": decision,
                "source": "decision_engine",
                "status": "normalized"
            }

        if isinstance(decision, dict):

            return {
                "type": "action",
                "action": decision.get("action", "ALLOW_WITH_CAUTION"),
                "payload": decision,
                "source": "decision_engine",
                "status": "normalized"
            }

        return {
            "type": "action",
            "action": "ALLOW_WITH_CAUTION",
            "source": "decision_engine",
            "status": "fallback"
        }
