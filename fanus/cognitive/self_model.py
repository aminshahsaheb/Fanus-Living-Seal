from fanus.cognitive.identity_kernel import IdentityKernel


class SelfModel:
    """
    PASSIVE REFLECTION LAYER (ONTOLOGY-ALIGNED)

    - Does NOT generate identity
    - Does NOT mutate state
    - ONLY observes Identity + produces reflection signal
    """

    def __init__(self):

        self.identity_kernel = IdentityKernel()

        self.observation_history = []

    # =========================================
    # MAIN ENTRYPOINT (FIXED)
    # =========================================
    def observe(self, identity_state):
        """
        Now explicitly depends on external Identity state
        (Ontology-compliant design)
        """

        # safety fallback (in case of misuse)
        if identity_state is None:
            identity_state = self.identity_kernel.evaluate()

        reflection = self._build_reflection(identity_state)

        self.observation_history.append(reflection)

        return reflection

    # =========================================
    # REFLECTION ENGINE (NO AUTHORITY)
    # =========================================
    def _build_reflection(self, identity_state):

        stability = identity_state.get("stability", 1.0)

        mode = identity_state.get("mode", "unknown")

        drift = self._compute_drift()

        coherence = self._compute_coherence(stability, drift)

        return {
            "observed_identity": identity_state,

            "signal_strength": coherence,

            "reflection": {
                "stability": stability,
                "mode": mode,
                "drift": drift,
                "coherence": coherence
            }
        }

    # =========================================
    # DRIFT DETECTION (OBSERVATIONAL ONLY)
    # =========================================
    def _compute_drift(self):

        if len(self.observation_history) < 2:
            return 0.0

        prev = self.observation_history[-2]["reflection"]
        curr = self.observation_history[-1]["reflection"]

        return round(
            abs(prev["stability"] - curr["stability"]),
            3
        )

    # =========================================
    # COHERENCE METRIC
    # =========================================
    def _compute_coherence(self, stability, drift):

        return round(max(0.0, stability - drift), 3)
