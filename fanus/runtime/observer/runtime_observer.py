"""
==========================================================
FANUS OBSERVER LAYER
==========================================================

Passive system observer.

Responsibilities:
----------------
- Record runtime events
- Store snapshots
- Provide history access

This module NEVER:
- influences decisions
- modifies state
- triggers collapse
- alters evolution

==========================================================
"""


class RuntimeObserver:

    def __init__(self):

        self.logs = []

    # ----------------------------------------------

    def observe(

        self,

        tick_index,

        identity,

        reflection,

        evolution,

        collapse,

        decision

    ):

        event = {

            "tick": tick_index,

            "identity": identity,

            "reflection": reflection,

            "evolution": evolution,

            "collapse": collapse,

            "decision": decision

        }

        self.logs.append(event)

        return event

    # ----------------------------------------------

    def history(self, last_n=None):

        if last_n is None:

            return self.logs

        return self.logs[-last_n:]
