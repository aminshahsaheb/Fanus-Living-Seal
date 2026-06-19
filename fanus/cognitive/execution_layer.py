class FanusExecutionLayer:

    def __init__(self):
        self.applied = []
        self.rejected = []

        # 🧠 FANUS CONCEPT MEMORY (IMPORTANT)
        self.semantic_core = {
            "stability": "system balance over time",
            "evolution": "controlled behavioral change",
            "memory": "persistent identity across time",
            "meta": "self-referential reasoning layer"
        }

    # =========================
    # ⚙️ MAIN EXECUTION
    # =========================
    def execute(self, evolution_result):

        proposals = evolution_result.get("proposals", [])

        applied = []

        for p in proposals:

            if self._validate(p):
                self._apply(p)
                applied.append(p)
            else:
                self.rejected.append(p)

        return {
            "applied": applied,
            "rejected": self.rejected,
            "semantic_state": self.semantic_core
        }

    # =========================
    # 🔍 VALIDATION LAYER
    # =========================
    def _validate(self, proposal):

        # SAFE RULES ONLY

        dangerous_actions = ["rewrite_core", "delete_memory", "break_loop"]

        if proposal.get("action") in dangerous_actions:
            return False

        return True

    # =========================
    # ⚡ APPLY LAYER
    # =========================
    def _apply(self, proposal):

        self.applied.append(proposal)

        # 🧠 EMBED MEANING INTO SYSTEM CORE
        self._embed_meaning(proposal)

    # =========================
    # 🧠 MEANING EMBEDDING LAYER
    # =========================
    def _embed_meaning(self, proposal):

        p_type = proposal.get("type")

        # هر execution یک meaning اضافه می‌کند
        self.semantic_core[p_type] = {
            "status": "active",
            "last_action": proposal.get("action"),
            "reason": proposal.get("reason")
        }
