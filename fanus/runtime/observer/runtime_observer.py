"""
==========================================================
FANUS OBSERVER LAYER (FINAL STABLE)
==========================================================

Passive full-trace recorder.

- No influence on runtime
- No mutation
- No decision logic

Stores complete execution trace safely.
==========================================================
"""

class RuntimeObserver:

    def __init__(self):
        self.logs = []

    # ==================================================
    # CORE TRACE ENTRY
    # ==================================================
    def observe(
        self,
        tick_index,
        identity,
        reflection,
        evolution,
        collapse,
        decision,
        execution,
        stability=None
    ):
        """
        Full runtime snapshot per tick.
        """

        event = {
            "tick": tick_index,

            "identity": identity,
            "reflection": reflection,
            "evolution": evolution,
            "collapse": collapse,

            # decision layer (raw action)
            "decision": decision,

            # execution result (validated event)
            "execution": execution,

            # optional stability layer (future-safe)
            "stability": stability
        }

        self.logs.append(event)

        return event

    # ==================================================

    def history(self, last_n=None):

        if last_n is None:
            return self.logs

        return self.logs[-last_n:]

    # ==================================================

    def export(self):

        return {
            "total_ticks": len(self.logs),
            "trace": self.logs
        }
