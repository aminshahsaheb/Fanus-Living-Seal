class FanusUnifiedIdentityField:

    def __init__(self):

        self.state_history = []

        self.current_field = {
            "coherence": 1.0,
            "stability": 1.0,
            "complexity": 0.0,
            "drift": 0.0,
            "identity_strength": 1.0
        }

    # =========================
    # 🧠 MAIN UPDATE
    # =========================
    def update(self, memory, meta, evolution, execution, recursive, boundary, identity):

        snapshot = {
            "memory": memory,
            "meta": meta,
            "evolution": evolution,
            "execution": execution,
            "recursive": recursive,
            "boundary": boundary,
            "identity": identity
        }

        self.state_history.append(snapshot)

        if len(self.state_history) > 50:
            self.state_history.pop(0)

        self._compute_field()

        return self.current_field

    # =========================
    # ⚡ FIELD COMPUTATION
    # =========================
    def _compute_field(self):

        if not self.state_history:
            return

        last = self.state_history[-1]

        meta = last["meta"]
        boundary = last["boundary"]
        identity = last["identity"]

        # -------------------------
        # 🧠 COHERENCE
        # -------------------------
        coherence = identity.get("stability", 1.0)

        # -------------------------
        # ⚖️ STABILITY
        # -------------------------
        stability = meta.get("stability", 1.0)

        # -------------------------
        # 🌪 DRIFT (from boundary)
        # -------------------------
        drift = boundary.get("drift_score", 0.0)

        # -------------------------
        # 🧬 COMPLEXITY
        # -------------------------
        complexity = len(self.state_history) / 50

        # -------------------------
        # 🧠 FINAL FIELD
        # -------------------------
        self.current_field = {
            "coherence": round(coherence, 3),
            "stability": round(stability, 3),
            "drift": round(drift, 3),
            "complexity": round(complexity, 3),
            "identity_strength": round(
                (coherence + stability - drift) / 2, 3
            )
        }
