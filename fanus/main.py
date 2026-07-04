import os
from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel
from fanus.cognitive.collapse.collapse_controller import CollapseController
from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine
from fanus.adapters.groq_adapter import GroqAdapter

SYSTEM_PROMPT = "تو فانوس هستی. فقط و فقط به زبان فارسی جواب بده. هرگز عربی استفاده نکن. صادق باش و چاپلوسی نکن."

class FanusSystem:

    def __init__(self):
        self.identity = IdentityKernel()
        self.self_model = SelfModel()
        self.collapse = CollapseController()
        self.stabilizer = SelfStabilizationEngine()
        self.engine = EvolutionEngine()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))

    def run_once(self, user_input):
        state = self.engine.run({"intent": "user_input"})
        identity = self.identity.evaluate(state["state"])
        reflection = self.self_model.observe(identity)
        collapse = self.collapse.evaluate(identity, state["state"], reflection)
        stabilizer = self.stabilizer.evaluate(collapse, state)
        response = self.llm.generate(SYSTEM_PROMPT, user_input)
        mode = identity["mode"]
        stab = round(state["state"]["stability"], 4)
        sys_mode = stabilizer["mode"]
        return response, mode, stab, sys_mode

    def run_interactive(self):
        print("فانوس آماده است.")
        while True:
            user_input = input("شما: ")
            if user_input.strip().lower() == "exit":
                break
            response, mode, stab, sys_mode = self.run_once(user_input)
            print("[" + mode + " | " + sys_mode + " | " + str(stab) + "]")
            print("فانوس: " + response)
            print()

if __name__ == "__main__":
    system = FanusSystem()
    system.run_interactive()