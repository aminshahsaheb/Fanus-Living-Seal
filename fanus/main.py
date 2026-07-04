import os
from fanus.core.identity import FanusIdentity
from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel
from fanus.cognitive.collapse.collapse_controller import CollapseController
from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.cognitive.orchestrator import CognitiveOrchestrator

SYSTEM_PROMPT = FanusIdentity().system_prompt()

class FanusSystem:

    def __init__(self):
        self.identity = IdentityKernel()
        self.self_model = SelfModel()
        self.collapse = CollapseController()
        self.stabilizer = SelfStabilizationEngine()
        self.engine = EvolutionEngine()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
        self.memory = MemoryPipeline()
        self.gateway = KnowledgeGateway()
        self.orchestrator = CognitiveOrchestrator()

    def run_once(self, user_input):
        self.memory.process(user_input, "user", 1.0)
        knowledge = self.gateway.quick_search(user_input)
        state = self.engine.run({"intent": "user_input"})
        identity = self.identity.evaluate(state["state"])
        reflection = self.self_model.observe(identity)
        collapse = self.collapse.evaluate(identity, state["state"], reflection)
        stabilizer = self.stabilizer.evaluate(collapse, state)
        enriched = SYSTEM_PROMPT + " [sources: " + str(knowledge["total_results"]) + "]"
        response = self.llm.generate(enriched, user_input)
        self.memory.process(response, "fanus", 0.9)
        cognitive = self.orchestrator.process(user_input, response)
        mode = identity["mode"]
        stab = round(state["state"]["stability"], 4)
        sys_mode = stabilizer["mode"]
        return response, mode, stab, sys_mode, cognitive

    def run_interactive(self):
        print("Fanus is ready.")
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() == "exit":
                break
            response, mode, stab, sys_mode, cognitive = self.run_once(user_input)
            print("[" + mode + " | " + sys_mode + " | " + str(stab) + "]")
            print("Fanus: " + response)
            print()

if __name__ == "__main__":
    system = FanusSystem()
    system.run_interactive()
