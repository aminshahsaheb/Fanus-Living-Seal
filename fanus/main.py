import os
from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel
from fanus.cognitive.collapse.collapse_controller import CollapseController
from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline

SYSTEM_PROMPT = "تو فانوس هستی. فقط و فقط به زبان فارسی جواب بده. هرگز عربی استفاده نکن. صادق باش و چاپلوسی نکن."

class FanusSystem:

    def __init__(self):
        self.identity = IdentityKernel()
        self.self_model = SelfModel()
        self.collapse = CollapseController()
        self.stabilizer = SelfStabilizationEngine()
        self.engine = EvolutionEngine()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
        self.memory = MemoryPipeline()

    def run_once(self, user_input):
        self.memory.process(user_input, "user", 1.0)
        state = self.engine.run({"intent": "user_input"})
        identity = self.identity.evaluate(state["state"])
        reflection = self.self_model.observe(identity)
        collapse = self.collapse.evaluate(identity, state["state"], reflection)
        stabilizer = self.stabilizer.evaluate(collapse, state)
        response = self.llm.generate(SYSTEM_PROMPT, user_input)
        self.memory.process(response, "fanus", 0.9)
        mode = identity["mode"]
        stab = round(state["state"]["stability"], 4)
        sys_mode = stabilizer["mode"]
        return response, mode, stab, sys_mode

    def run_interactive(self):
        print("فانوس آماده است.")
        while True:
            user_input = input("شما: ")
            if user_input.strip().lower() == "exit":
                print("ledger size: " + str(self.memory.ledger.size()))
                break
            response, mode, stab, sys_mode = self.run_once(user_input)
            print("[" + mode + " | " + sys_mode + " | " + str(stab) + "]")
            print("فانوس: " + response)
            print()

if __name__ == "__main__":
    system = FanusSystem()
    system.run_interactive()