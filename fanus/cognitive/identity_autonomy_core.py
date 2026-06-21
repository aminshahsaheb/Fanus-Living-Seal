class FanusIdentityAutonomyCore:

    def __init__(self):

        self.autonomy_level = 1.0  # global control
        self.freeze_state = False

        self.history = []

    # =========================
    # 🧠 MAIN CONTROL FUNCTION
    # =========================
    def evaluate(self, cognitive_state, identity, learning_state):

        drift = cognitive_state.get("drift", 0.0)
        coherence = cognitive_state.get("coherence", 1.0)
        stability = cognitive_state.get("stability", 1.0)

        identity_strength = identity.get("identity_strength", 1.0)

        learning_pressure = learning_state.get("learning_state", {})
        drift_suppression = learning_pressure.get("drift_suppression", 0.0)

        # -------------------------
        # 🧠 AUTONOMY SCORING
        # -------------------------
        score = 1.0

        score -= drift * 0.4
        score -= (1 - coherence) * 0.3
        score -= (1 - stability) * 0.2
        score -= drift_suppression * 0.1

        score = max(0.0, min(score, 1.0))

        self.autonomy_level = score

        # -------------------------
        # ❄️ FREEZE CONDITIONS
        # -------------------------
        freeze = False

        if drift > 0.8:
            freeze = True

        if coherence < 0.3:
            freeze = True

        if stability < 0.2:
            freeze = True

        # -------------------------
        # 🔓 UNLOCK CONDITIONS
        # -------------------------
        if coherence > 0.7 and stability > 0.7:
            freeze = False

        self.freeze_state = freeze

        # -------------------------
        # 🧠 LEARNING ALLOWED?
        # -------------------------
        learning_allowed = not freeze and self.autonomy_level > 0.3

        # -------------------------
        # 🧬 STORE HISTORY
        # -------------------------
        self.history.append({
            "autonomy": self.autonomy_level,
            "freeze": self.freeze_state,
            "learning_allowed": learning_allowed
        })

        if len(self.history) > 100:
            self.history.pop(0)

        return {
            "autonomy_level": self.autonomy_level,
            "freeze": self.freeze_state,
            "learning_allowed": learning_allowed
        }
