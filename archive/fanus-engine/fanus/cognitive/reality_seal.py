class RealitySeal:

    def __init__(self):

        self.history = []

    # =========================
    # 🧠 1. SOURCE VALIDATION
    # =========================
    def validate_source(self, event):

        # اگر داده از بیرون آمده باشد
        if event.get("source") == "external":
            return 1.0

        # اگر داخلی / تولید شده باشد
        if event.get("source") == "internal":
            return 0.5

        return 0.2

    # =========================
    # 🧠 2. MEMORY CONSISTENCY
    # =========================
    def check_memory_consistency(self, memory, event):

        if not memory:
            return 0.5

        last = memory[-1].get("intent")

        if last == event.get("intent"):
            return 0.9

        return 0.4

    # =========================
    # 🧠 3. MODEL DRIFT CHECK
    # =========================
    def model_drift(self, meta_self, origin_core):

        try:
            stability = meta_self.get("analysis", {}).get("identity_stability", 0)
            direction = origin_core.get("direction", "")

            if stability > 0.7 and direction == "preserve_current_architecture":
                return 0.9

            if stability < 0.3:
                return 0.2

            return 0.6

        except Exception:
            return 0.3

    # =========================
    # 🧠 4. TRUTH SCORE
    # =========================
    def compute_truth_score(self, source, memory_score, drift_score):

        return (source * 0.4) + (memory_score * 0.3) + (drift_score * 0.3)

    # =========================
    # 🧠 5. FINAL DECISION
    # =========================
    def decide(self, truth_score):

        if truth_score > 0.75:
            return "ALLOW"

        if truth_score > 0.4:
            return "ALLOW_WITH_CAUTION"

        return "BLOCK_OR_RECHECK"

    # =========================
    # 🧠 MAIN PIPELINE
    # =========================
    def run(self, event, memory, meta_self, origin_core):

        source = self.validate_source(event)

        memory_score = self.check_memory_consistency(memory, event)

        drift_score = self.model_drift(meta_self, origin_core)

        truth_score = self.compute_truth_score(
            source,
            memory_score,
            drift_score
        )

        decision = self.decide(truth_score)

        result = {
            "source_score": source,
            "memory_score": memory_score,
            "drift_score": drift_score,
            "truth_score": truth_score,
            "decision": decision
        }

        self.history.append(result)

        return result
