import threading
import time
from fanus.cognitive.curiosity_engine import CuriosityEngine
from fanus.cognitive.research_planner import ResearchPlanner
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.memory.pipeline import MemoryPipeline


class AutoResearchLoop:

    def __init__(self):
        self.curiosity = CuriosityEngine()
        self.planner = ResearchPlanner()
        self.gateway = KnowledgeGateway()
        self.memory = MemoryPipeline()
        self.running = False
        self.cycles = 0
        self.log = []

    def run_cycle(self, topic):
        questions = self.curiosity.generate(topic)
        plan = self.planner.create(topic, [q["question"] for q in questions[:3]])
        results = self.gateway.quick_search(topic)
        finding = "Found " + str(results["total_results"]) + " sources for: " + topic
        self.planner.add_finding(plan["id"], finding, 0.8)
        self.memory.process(finding, "auto_research", 0.8)
        self.cycles += 1
        entry = {"cycle": self.cycles, "topic": topic, "sources": results["total_results"]}
        self.log.append(entry)
        return entry

    def stats(self):
        return {"cycles": self.cycles, "log": self.log[-5:]}
