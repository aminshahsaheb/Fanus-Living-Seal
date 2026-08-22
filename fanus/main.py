import os
from fanus.core.identity import FanusIdentity
from fanus.runtime.loop import FanusLoop
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.cognitive.orchestrator import CognitiveOrchestrator
from fanus.cognitive.guardian_pipeline import run_guardians
from fanus.cognitive.policy_engine import PolicyEngine, EpistemicSignal
from fanus.cognitive.isp_controller import ISPController

SYSTEM_PROMPT = FanusIdentity().system_prompt()

class FanusSystem:

    def __init__(self):
        self.loop = FanusLoop()
        self.llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
        self.memory = MemoryPipeline()
        self.gateway = KnowledgeGateway()
        self.orchestrator = CognitiveOrchestrator()
        # guardians now unified in fanus.cognitive.guardian_pipeline
        self.policy = PolicyEngine()
        self.isp = ISPController()

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
        guardians = run_guardians(user_input, response, "fanus")
        negar = {"is_negar": guardians["negar"]}
        fi = {"Fi_score": guardians["fi_score"], "Fi_type": guardians["fi_type"]}
        hayrat = {"hayrat_score": guardians["hayrat_score"], "arrogance_detected": guardians["arrogance"], "uncertainty_required": guardians["uncertainty_required"]}
        if hayrat["uncertainty_required"]:
            from fanus.cognitive.hayrat_judge import HayratJudge
            response = HayratJudge().revise_response(response, hayrat)
        if hayrat["arrogance_detected"]:
            self.policy.evaluate(EpistemicSignal.HIGH_CONFIDENCE, {"has_evidence": False})
        if fi["Fi_score"] >= 2:
            self.policy.evaluate(EpistemicSignal.IDENTITY_LOCK, {"fi_score": fi["Fi_score"]})
            self.isp.evaluate(fi["Fi_score"], 0, "high")
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
