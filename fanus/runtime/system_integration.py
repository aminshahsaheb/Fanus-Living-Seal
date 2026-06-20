class FanusSystemIntegration:

    def __init__(self, loop):

        self.loop = loop
        self.initialized = False
        self.errors = []

    # =========================
    # 🧠 BOOTSTRAP ENTRY
    # =========================
    def bootstrap(self):

        try:
            self._validate_loop_structure()
            self.initialized = True

        except Exception as e:
            self.errors.append(str(e))
            self.initialized = False

        return {
            "initialized": self.initialized,
            "errors": self.errors
        }

    # =========================
    # 🔍 SAFE VALIDATION
    # =========================
    def _validate_loop_structure(self):

        required_attrs = [
            "tick",
            "engine",
            "memory",
            "observer",
            "self_model",
            "meta_model"
        ]

        missing = [a for a in required_attrs if not hasattr(self.loop, a)]

        if missing:
            raise Exception(f"Missing core modules: {missing}")

    # =========================
    # 🔁 SAFE RUN
    # =========================
    def safe_run(self, max_ticks=10):

        if not self.initialized:
            raise Exception("System not bootstrapped")

        return self.loop.run(max_ticks)
