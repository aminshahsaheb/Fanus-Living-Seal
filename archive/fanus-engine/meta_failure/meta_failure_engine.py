class MetaFailureEngine:
    """
    V5.30.0 — Meta Failure Loop Engine

    هدف:
    تبدیل failure logs به evolution signals
    """

    def __init__(self):

        # ─────────────────────────────
        # FAILURE MEMORY
        # ─────────────────────────────
        self.failure_buffer = []

        # ─────────────────────────────
        # EVOLUTION THRESHOLD
        # ─────────────────────────────
        self.rewrite_threshold = 5

    def ingest_failure(self, failure_report: dict):

        # ذخیره شکست
        self.failure_buffer.append(failure_report)

        if len(self.failure_buffer) > 50:
            self.failure_buffer.pop(0)

    def analyze(self):

        if len(self.failure_buffer) < self.rewrite_threshold:
            return {
                "status": "insufficient_data",
                "action": "wait"
            }

        # ─────────────────────────────
        # FAILURE PATTERN EXTRACTION
        # ─────────────────────────────
        fi_errors = 0
        di_errors = 0
        drift_instability = 0

        for f in self.failure_buffer:

            if "Fi_score" in f.get("type", ""):
                fi_errors += 1

            if "Di_score" in f.get("type", ""):
                di_errors += 1

            if f.get("category") == "drift":
                drift_instability += 1

        # ─────────────────────────────
        # EVOLUTION DECISION
        # ─────────────────────────────
        need_rewrite = (
            fi_errors >= self.rewrite_threshold or
            di_errors >= self.rewrite_threshold or
            drift_instability >= self.rewrite_threshold
        )

        if need_rewrite:
            return {
                "status": "rewrite_triggered",
                "action": "GENERATE_V5_31",
                "reason": {
                    "fi_errors": fi_errors,
                    "di_errors": di_errors,
                    "drift_instability": drift_instability
                }
            }

        return {
            "status": "stable",
            "action": "continue_learning"
        }
