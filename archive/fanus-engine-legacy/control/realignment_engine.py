# fanus-engine/control/realignment_engine.py

class RealignmentEngine:

    def apply(self, state, drift_score):

        # کاهش confidence در وضعیت خطر
        if drift_score > 0.6:
            state["confidence"] = max(0.1, state.get("confidence", 1.0) * 0.85)
            state["mode"] = "recalibration"

        return state
