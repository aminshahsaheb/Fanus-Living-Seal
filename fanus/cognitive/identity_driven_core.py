class FanusIdentityDrivenCore:

    def __init__(self):
        self.decision_history = []

    # =========================
    # 🧠 MAIN DECISION LAYER
    # =========================
    def decide(self, engine_result, cognitive_state, identity, governance):

        raw_decision = engine_result.get("decision")
        stability = cognitive_state.get("stability", 1.0)
        coherence = cognitive_state.get("coherence", 1.0)
        drift = cognitive_state.get("drift", 0.0)

        identity_strength = identity.get("identity_strength", 1.0)
        mode = identity.get("mode", "unknown")

        autonomy = governance.get("autonomy_level", 0.5)

        # -------------------------
        # 🧠 BASE DECISION
        # -------------------------
        decision = raw_decision

        # -------------------------
        # ⚖️ IDENTITY BIAS
        # -------------------------
        if identity_strength < 0.5:
            decision = "stabilize"

        # -------------------------
        # 🧠 STABILITY CONTROL
        # -------------------------
        if stability < 0.4:
            decision = "reduce_activity"

        # -------------------------
        # 🌊 DRIFT CONTROL
        # -------------------------
        if drift > 0.7:
            decision = "halt_and_realign"

        # -------------------------
        # 🧬 COHERENCE OVERRIDE
        # -------------------------
        if coherence < 0.5:
            decision = "coherence_repair"

        # -------------------------
        # ⚖️ AUTONOMY LIMIT
        # -------------------------
        if autonomy < 0.3:
            decision = "safe_mode"

        # -------------------------
        # 🧠 MODE-BASED BEHAVIOR
        # -------------------------
        if mode == "adaptive_instability_mode":
            decision = "explore_safely"

        # -------------------------
        # 🧠 STORE HISTORY
        # -------------------------
        self.decision_history.append(decision)

        if len(self.decision_history) > 50:
            self.decision_history.pop(0)

        return {
            "final_decision": decision,
            "raw_decision": raw_decision,
            "identity_influence": identity_strength,
            "stability": stability,
            "coherence": coherence,
            "drift": drift,
            "mode": mode
        }
