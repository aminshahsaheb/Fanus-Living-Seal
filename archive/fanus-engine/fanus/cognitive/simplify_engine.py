class SimplifyEngine:

    def __init__(self):

        self.history = []

    # =========================
    # 🧠 1. COMPLEXITY SCORE
    # =========================
    def compute_complexity(self, architecture):

        modules = architecture.get("modules", {})

        base = len(modules) * 0.1

        extra = 0

        for k, v in modules.items():
            extra += v.get("complexity", 0.5)

        return base + extra

    # =========================
    # 🧠 2. REDUNDANCY CHECK
    # =========================
    def redundancy(self, meta_self, god_loop, reality_seal):

        score = 0

        if meta_self:
            score += 0.3

        if god_loop:
            score += 0.4

        if reality_seal:
            score += 0.3

        # اگر همه فعال باشند → redundancy بالا
        return score

    # =========================
    # 🧠 3. LOOP OVERLAP
    # =========================
    def loop_overlap(self, state):

        loops = [
            state.get("meta_loop", False),
            state.get("god_loop", False),
            state.get("breaker_loop", False)
        ]

        return sum(1 for l in loops if l)

    # =========================
    # 🧠 4. SIMPLIFICATION STRATEGY
    # =========================
    def strategy(self, complexity, redundancy, overlap):

        if complexity > 2.5 or overlap >= 3:
            return "AGGRESSIVE_PRUNE"

        if complexity > 1.5:
            return "MODERATE_PRUNE"

        if redundancy > 0.8:
            return "MERGE_LAYERS"

        return "NO_ACTION"

    # =========================
    # 🧠 5. APPLY SIMPLIFICATION
    # =========================
    def apply(self, architecture, strategy):

        modules = architecture.get("modules", {})

        if strategy == "AGGRESSIVE_PRUNE":
            # keep only core modules
            keep = ["memory", "identity", "cognitive_core"]
            modules = {k: v for k, v in modules.items() if k in keep}

        elif strategy == "MODERATE_PRUNE":
            # reduce complexity weights
            for k in modules:
                modules[k]["complexity"] *= 0.7

        elif strategy == "MERGE_LAYERS":
            # simulate merging meta layers
            modules["meta_core"] = {
                "complexity": 0.5,
                "usage": 1
            }

        return {
            "modules": modules,
            "strategy": strategy
        }

    # =========================
    # 🧠 MAIN LOOP
    # =========================
    def run(self, architecture, meta_self, god_loop, reality_seal, state):

        complexity = self.compute_complexity(architecture)

        redundancy = self.redundancy(meta_self, god_loop, reality_seal)

        overlap = self.loop_overlap(state)

        strategy = self.strategy(complexity, redundancy, overlap)

        simplified = self.apply(architecture, strategy)

        result = {
            "complexity": complexity,
            "redundancy": redundancy,
            "overlap": overlap,
            "strategy": strategy,
            "result": simplified
        }

        self.history.append(result)

        return result
