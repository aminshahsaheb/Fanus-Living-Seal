import copy


class ArchitectureEvolution:

    def __init__(self):

        self.history = []
        self.version = 1

    # =========================
    # 🧠 1. ANALYZE SYSTEM
    # =========================
    def analyze(self, system_state):

        modules = system_state.get("modules", {})
        metrics = system_state.get("metrics", {})

        analysis = {
            "module_count": len(modules),
            "high_complexity": [],
            "unused_modules": [],
            "critical_paths": []
        }

        # detect complexity
        for name, data in modules.items():

            if data.get("complexity", 0) > 0.8:
                analysis["high_complexity"].append(name)

            if data.get("usage", 1) == 0:
                analysis["unused_modules"].append(name)

            if data.get("critical", False):
                analysis["critical_paths"].append(name)

        return analysis

    # =========================
    # 🧠 2. GENERATE EVOLUTION PLAN
    # =========================
    def propose_evolution(self, analysis):

        plan = {
            "remove": [],
            "refactor": [],
            "isolate": []
        }

        # حذف ماژول‌های بلااستفاده
        plan["remove"] = analysis["unused_modules"]

        # رفرکت ماژول‌های پیچیده
        plan["refactor"] = analysis["high_complexity"]

        # محافظت از مسیرهای حیاتی
        plan["isolate"] = analysis["critical_paths"]

        return plan

    # =========================
    # 🧠 3. GENERATE PATCH
    # =========================
    def generate_patch(self, system_state, plan):

        new_state = copy.deepcopy(system_state)

        # REMOVE
        for m in plan["remove"]:
            new_state["modules"].pop(m, None)

        # REFACTOR (simplify complexity)
        for m in plan["refactor"]:
            if m in new_state["modules"]:
                new_state["modules"][m]["complexity"] *= 0.7

        # ISOLATE critical paths
        for m in plan["isolate"]:
            if m in new_state["modules"]:
                new_state["modules"][m]["isolated"] = True

        return new_state

    # =========================
    # 🧠 4. SAFETY CHECK
    # =========================
    def safety_check(self, old_state, new_state):

        old_modules = len(old_state.get("modules", {}))
        new_modules = len(new_state.get("modules", {}))

        # جلوگیری از collapse
        if new_modules < old_modules * 0.5:
            return False

        return True

    # =========================
    # 🧠 5. EVOLVE SYSTEM
    # =========================
    def evolve(self, system_state):

        analysis = self.analyze(system_state)

        plan = self.propose_evolution(analysis)

        new_state = self.generate_patch(system_state, plan)

        safe = self.safety_check(system_state, new_state)

        if not safe:
            return {
                "status": "blocked",
                "reason": "unsafe evolution detected",
                "analysis": analysis
            }

        self.history.append({
            "version": self.version,
            "plan": plan
        })

        self.version += 1

        return {
            "status": "evolved",
            "version": self.version,
            "analysis": analysis,
            "plan": plan,
            "new_state": new_state
        }
