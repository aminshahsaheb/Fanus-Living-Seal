class LivingOrchestrator:

    def __init__(self, control_center):

        # اتصال به کنترل سنتر (اما نه وابسته کامل)
        self.control_center = control_center

        # وضعیت کل سیستم
        self.global_state = {
            "mode": "INIT",
            "stability": 1.0,
            "cycles": 0
        }

        # ماژول‌های فعال (زنده)
        self.modules = []

    def register_module(self, module):

        self.modules.append(module)

    def tick(self, input_event: dict):

        """
        هر tick = یک نفس سیستم
        """

        self.global_state["cycles"] += 1

        drift_result = input_event.get("drift_result", {})

        context = input_event.get("context", {})

        # ─────────────────────────────
        # 1. PROPAGATE TO CONTROL CENTER
        # ─────────────────────────────
        cc_result = self.control_center.process(
            drift_result,
            self.global_state,
            context
        )

        # ─────────────────────────────
        # 2. DISTRIBUTE STATE TO MODULES
        # ─────────────────────────────
        for module in self.modules:
            if hasattr(module, "update"):
                module.update(cc_result, self.global_state)

        # ─────────────────────────────
        # 3. COLLECT FEEDBACK FROM MODULES
        # ─────────────────────────────
        feedback = []

        for module in self.modules:
            if hasattr(module, "feedback"):
                feedback.append(module.feedback())

        # ─────────────────────────────
        # 4. EMERGENT STABILITY COMPUTATION
        # ─────────────────────────────
        instability = 0.0

        for f in feedback:
            instability += f.get("instability", 0.0)

        self.global_state["stability"] = max(
            0.0,
            1.0 - instability / max(1, len(feedback))
        )

        # ─────────────────────────────
        # 5. SELF-REGULATION LOOP
        # ─────────────────────────────
        if self.global_state["stability"] < 0.5:
            self.global_state["mode"] = "SELF_REPAIR"

        elif self.global_state["stability"] < 0.2:
            self.global_state["mode"] = "CRITICAL_REALIGNMENT"

        else:
            self.global_state["mode"] = "STABLE"

        # ─────────────────────────────
        # 6. RETURN SYSTEM SNAPSHOT
        # ─────────────────────────────
        return {
            "global_state": self.global_state,
            "control_output": cc_result,
            "module_feedback": feedback
        }
