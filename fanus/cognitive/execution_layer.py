"""
==========================================================
FANUS EXECUTION LAYER
==========================================================

Canonical Execution Layer

Pipeline

Decision Event
      ↓
Validation
      ↓
Execution
      ↓
Memory
      ↓
Execution Report

Execution NEVER:

- creates proposals
- evaluates policy
- edits identity
- edits evolution
- edits collapse

==========================================================
"""

from fanus.cognitive.memory_layer import MemoryLayer
from fanus.cognitive.ontology.event_factory import EventFactory


class FanusExecutionLayer:

    def __init__(self):

        self.memory = MemoryLayer()

        self.applied = []

        self.rejected = []

    # =====================================================

    def execute(self, decision: str):

        if not self._validate(decision):

            event = EventFactory.decision(

                payload={

                    "action": decision,

                    "status": "rejected"

                },

                source="execution",

                metadata={

                    "layer": "execution"

                }

            )

            self.rejected.append(event)

            self.memory.store(event)

            return event

        event = EventFactory.decision(

            payload={

                "action": decision,

                "status": "executed"

            },

            source="execution",

            metadata={

                "layer": "execution"

            }

        )

        self.applied.append(event)

        self.memory.store(event)

        return event

    # =====================================================

    def _validate(self, decision):

        forbidden = {

            "rewrite_identity",

            "rewrite_core",

            "override_core",

            "delete_memory",

            "break_loop",

            "disable_collapse_monitor"

        }

        return decision not in forbidden

    # =====================================================

    def history(self):

        return self.memory.all()

    # =====================================================

    def statistics(self):

        return {

            "applied": len(self.applied),

            "rejected": len(self.rejected),

            "memory": self.memory.size()

        }
