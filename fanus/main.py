import os
from fanus.core.identity import FanusIdentity
from fanus.runtime.loop import FanusLoop
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.cognitive.orchestrator import CognitiveOrchestrator
from fanus.cognitive.negar_detector import NegarDetector
from fanus.cognitive.hayrat_judge import HayratJudge
from fanus.cognitive.fi_detector import detect_fi

SYSTEM_PROMPT = FanusIdentity().system_prompt()

class FanusSystem:

    def __init__(self):
        self.loop = FanusLoop()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
        self.memory = MemoryPipeline()
        self.gateway = KnowledgeGateway()
        self.orchestrator = CognitiveOrchestrator()
        self.negar = NegarDetector()
        self.hayrat = HayratJudge()

    def run_once(self, user_input):
        self.memory.process(user_input, "user", 1.0)
        knowledge = self.gateway.quick_search(user_input)
        self.loop._tick()
        identity = self.loop.identity.evaluate()
        enriched = SYSTEM_PROMPT + " [sources: " + str(knowledge["total_results"]) + "]"
        try:
            response = self.llm.generate(enriched, user_input)
        except Exception as e:
            response = "خطا در ارتباط با مدل: " + str(e)[:100]
        self.memory.process(response, "fanus", 0.9)
        cognitive = self.orchestrator.process(user_input, response)
        negar = self.negar.analyze(response, "fanus")
        fi = detect_fi(user_input, response)
        hayrat = self.hayrat.evaluate(response, user_input)
        if hayrat["uncertainty_required"]:
            response = self.hayrat.revise_response(response, hayrat)
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
            negar_flag = " ⚠️NEGAR" if cognitive.get("negar", False) else ""
            print("[" + mode + " | " + str(stab) + negar_flag + "]")
            print("Fanus: " + response)
            print()

if __name__ == "__main__":
    system = FanusSystem()
    system.run_interactive()
