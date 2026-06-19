import time

from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.observer import FanusObserver
from fanus.cognitive.self_model import FanusSelfModel
from fanus.cognitive.meta_self_model import FanusMetaSelfModel
from fanus.cognitive.self_improvement import FanusSelfImprovement
from fanus.cognitive.memory_layer import FanusMemoryLayer
from fanus.cognitive.evolution_controller import FanusEvolutionController


class FanusLoop:
    """
    FANUS FULL CONTROLLED COGNITIVE SYSTEM

    LAYERS:
    1. Engine
    2. Memory (persistent history)
    3. Observer (metrics)
    4. Self Model (identity)
    5. Meta Model (reasoning)
    6. Self Improvement (safe decisions)
    7. Evolution Controller (pattern → proposals)
    """

    def __init__(self, tick_delay=1, max_memory=200):

        # 🧠 CORE SYSTEMS
        self.engine = EvolutionEngine()
        self.observer = FanusObserver()
        self.self_model = FanusSelfModel()
        self.meta_model = FanusMetaSelfModel()
        self.self_improver = FanusSelfImprovement()
        self.evolution = FanusEvolutionController()

        # 💾 MEMORY LAYER
        self.memory = FanusMemoryLayer(max_size=max_memory)

        # ⚙️ RUNTIME CONFIG
        self.tick_delay = tick_delay

        # 🧠 STATE
        self.tick = 0
        self.running = False

    # =========================
    # 🔁 SINGLE CYCLE
    # =========================
    def cycle(self, intent="test"):

        # 1. ENGINE EXECUTION
        result = self.engine.run({"intent": intent})

        # 2. MEMORY STORE
        self.memory.store(result)

        # 3. OBSERVATION
        observation = self.observer.observe(result)

        # 4. SELF MODEL
        self_model = self.self_model.update(observation, result)

        # 5. META MODEL
        meta = self.meta_model.analyze(self_model)

        # 6. EVOLUTION ENGINE (pattern-based proposals)
        evolution = self.evolution.evaluate(
            self.memory.snapshot(),
            meta
        )

        # 7. SELF IMPROVEMENT (controlled evaluation)
        improvement = self.self_improver.evaluate(meta)

        # 8. OUTPUT
        self._print(result, observation, self_model, meta, evolution, improvement)

        return {
            "result": result,
            "observation": observation,
            "self_model": self_model,
            "meta": meta,
            "evolution": evolution,
            "improvement": improvement,
            "memory": self.memory.snapshot()
        }

    # =========================
    # 🧠 OUTPUT
    # =========================
    def _print(self, result, observation, self_model, meta, evolution, improvement):

        print("\n🧠 FANUS LOOP TICK")
        print("------------------")
        print("Tick:", self.tick)
        print("Intent:", result.get("intent"))
        print("Decision:", result.get("decision"))

        print("\n📊 OBSERVATION:")
        print(observation)

        print("\n🧠 SELF MODEL:")
        print(self_model)

        print("\n🧠 META MODEL:")
        print(meta)

        print("\n⚙️ EVOLUTION ENGINE:")
        print(evolution)

        print("\n🛠 SELF IMPROVEMENT:")
        print(improvement)

        print("\n💾 MEMORY:")
        print(self.memory.snapshot())

    # =========================
    # 🔁 LOOP
    # =========================
    def run(self, max_ticks=10):

        self.running = True

        print("\n🚀 FANUS FULL CONTROLLED COGNITIVE LOOP STARTED\n")

        while self.running and self.tick < max_ticks:

            self.cycle("test")

            self.tick += 1
            time.sleep(self.tick_delay)

        print("\n🛑 FANUS LOOP STOPPED")

    # =========================
    # ⛔ STOP
    # =========================
    def stop(self):
        self.running = False
