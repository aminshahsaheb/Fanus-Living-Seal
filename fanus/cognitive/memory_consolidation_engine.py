class FanusMemoryConsolidationEngine:

    def __init__(self):

        self.consolidated_memory = {
            "patterns": [],
            "compressed_events": [],
            "identity_signatures": [],
            "drift_history": []
        }

    # =========================
    # 🧠 MAIN CONSOLIDATION
    # =========================
    def consolidate(self, raw_memory, cognitive_state, identity):

        events = raw_memory.get("events", [])
        drift = cognitive_state.get("drift", 0.0)
        coherence = cognitive_state.get("coherence", 1.0)

        identity_strength = identity.get("identity_strength", 1.0)

        # -------------------------
        # 📦 COMPRESS EVENTS
        # -------------------------
        compressed = self._compress_events(events)

        # -------------------------
        # 🧠 EXTRACT PATTERNS
        # -------------------------
        patterns = self._extract_patterns(events, cognitive_state)

        # -------------------------
        # 🧬 IDENTITY SIGNATURE
        # -------------------------
        signature = {
            "identity_strength": identity_strength,
            "coherence": coherence,
            "drift": drift
        }

        # -------------------------
        # 🌊 DRIFT TRACKING
        # -------------------------
        self.consolidated_memory["drift_history"].append(drift)

        # keep last 50
        self.consolidated_memory["drift_history"] = \
            self.consolidated_memory["drift_history"][-50:]

        # -------------------------
        # 🧠 STORE
        # -------------------------
        self.consolidated_memory["compressed_events"].extend(compressed)
        self.consolidated_memory["patterns"].extend(patterns)
        self.consolidated_memory["identity_signatures"].append(signature)

        return self.consolidated_memory

    # =========================
    # 📦 EVENT COMPRESSION
    # =========================
    def _compress_events(self, events):

        compressed = []

        for e in events[-10:]:  # only recent window

            compressed.append({
                "summary": str(e)[:80],
                "type": e.get("type", "unknown") if isinstance(e, dict) else "raw",
            })

        return compressed

    # =========================
    # 🧠 PATTERN EXTRACTION
    # =========================
    def _extract_patterns(self, events, cognitive_state):

        patterns = []

        drift = cognitive_state.get("drift", 0.0)
        coherence = cognitive_state.get("coherence", 1.0)

        if drift > 0.6:
            patterns.append("high_drift_behavior")

        if coherence < 0.5:
            patterns.append("low_coherence_cycle")

        if len(events) > 20:
            patterns.append("memory_overflow_pressure")

        return patterns
