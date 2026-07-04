import os
from fanus.core.identity import FanusIdentity
from fanus.runtime.loop import FanusLoop
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.cognitive.orchestrator import CognitiveOrchestrator

SYSTEM_PROMPT = FanusIdentity().system_prompt()

class FanusSystem:

    def __init__(self):
        self.loop = FanusLoop()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
        self.memory = MemoryPipeline()
        self.gateway = KnowledgeGateway()
        self.orchestrator = CognitiveOrchestrator()

    def run_once(self, user_input):
        self.memory.process(user_input, "user", 1.0)
        knowledge = self.gateway.quick_search(user_input)
        self.loop._tick()
        identity = self.loop.identity.evaluate()
        enriched = SYSTEM_PROMPT + " [sources: " + str(knowledge["total_results"]) + "]"
        response = self.llm.generate(enriched, user_input)
        self.memory.process(response, "fanus", 0.9)
        cognitive = self.orchestrator.process(user_input, response)
        mode = identity["mode"]
        stab = round(identity["stability"], 4)
        return response, mode, stab, cognitive

    def run_interactive(self):
        print("Fanus is ready.")
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() == "exit":
                break
            response, mode, stab, cognitive = self.run_once(user_input)
            print("[" + mode + " | " + str(stab) + "]")
            print("Fanus: " + response)
            print()

if __name__ == "__main__":
    system = FanusSystem()
    system.run_interactive()
