class ProposalRewriter:
    """
    Takes evolution output and rewrites proposals
    based on memory pressure + collapse risk.
    """

    def rewrite(self, proposals, memory_pressure, collapse_state):

        rewritten = []

        for p in proposals:

            action = p.get("payload", {}).get("action", "NOOP")

            # collapse-aware soft mutation
            if memory_pressure > 0.7:
                action = f"adaptive_{action}"

            if collapse_state["meta"]["alert_level"] == "HIGH":
                action = "stabilize_" + action

            rewritten.append({
                **p,
                "payload": {
                    **p.get("payload", {}),
                    "action": action,
                    "rewritten": True
                }
            })

        return rewritten
