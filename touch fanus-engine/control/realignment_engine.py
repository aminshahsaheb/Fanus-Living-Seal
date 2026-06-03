class RealignmentEngine:

    def realign(self, state, drift_score):

        if drift_score > 0.6:
            state["mode"] = "reconstruct"
            state["confidence"] *= 0.8

        return state
