"""
==========================================================
FANUS EXECUTION LAYER (COHERENT EVENT SYSTEM)
==========================================================
execution_limit now has real effect: it caps how many
proposals are processed in a single execute() call. Extra
proposals beyond the limit are deferred (not applied,
not rejected -- simply not reached this tick).
"""

from fanus.cognitive.memory_layer import MemoryLayer
from fanus.cognitive.ontology.event_factory import EventFactory


class FanusExecutionLayer:

    def __init__(self):
        self.memory = MemoryLayer()
        self.applied = []
        self.rejected = []

    def execute(self, payload):
        decision = payload.get("decision", "")
        proposals = payload.get("proposals", [])
        raw_limit = payload.get("execution_limit", 1)

        if isinstance(raw_limit, bool):
            limit = 1 if raw_limit else 0
        elif isinstance(raw_limit, float) and raw_limit <= 1.0:
            limit = 1
        else:
            limit = int(raw_limit)

        if proposals:
            candidates = [p.get("action", "") if isinstance(p, dict) else p for p in proposals]
        elif decision:
            candidates = [decision]
        else:
            candidates = []

        to_process = candidates[:limit]
        deferred_count = max(0, len(candidates) - limit)

        events = []
        for action in to_process:
            if not self._validate(action):
                event = EventFactory.decision(
                    payload={"action": action, "status": "rejected"},
                    source="execution",
                    metadata={"layer": "execution"}
                )
                self.rejected.append(event)
            else:
                event = EventFactory.decision(
                    payload={"action": action, "status": "executed"},
                    source="execution",
                    metadata={"layer": "execution"}
                )
                self.applied.append(event)
            self.memory.store(event)
            events.append(event)

        if events:
            primary_event = events[0]
        else:
            primary_event = EventFactory.decision(
                payload={"action": "", "status": "no_action"},
                source="execution",
                metadata={"layer": "execution"}
            )

        if isinstance(primary_event, dict):
            primary_event = dict(primary_event)
            primary_event["execution_limit_applied"] = limit
            primary_event["events_this_tick"] = len(events)
            primary_event["deferred_this_tick"] = deferred_count

        return primary_event

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

    def history(self):
        return self.memory.all()

    def statistics(self):
        return {
            "applied": len(self.applied),
            "rejected": len(self.rejected),
            "memory": self.memory.size()
        }
