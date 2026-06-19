import time

from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.observer import FanusObserver
from fanus.cognitive.self_model import FanusSelfModel
from fanus.cognitive.meta_self_model import FanusMetaSelfModel
from fanus.cognitive.self_improvement import FanusSelfImprovement
from fanus.cognitive.memory_layer import FanusMemoryLayer
from fanus.cognitive.evolution_controller import FanusEvolutionController
from fanus.cognitive.execution_layer import FanusExecutionLayer


class FanusLoop:
    """
    FANUS FULL CONTROLLED COGNITIVE SYSTEM

    LAYERS:
    1. Engine
    2. Memory
    3. Observer
    4. Self Model
    5. Meta Model
    6. Evolution Controller
    7. Execution Layer (semantic + safe apply)
    8. Self Improvement
    """

    def __init__(self, tick_delay=1, max_memory=200):

        # 🧠 CORE ENGINE
        self.engine = EvolutionEngine()

        # 👁 OBSERVATION
        self.observer = FanusObserver()

        # 🧠 COGNITION
        self.self_model = FanusSelfModel()
        self.meta_model = FanusMetaSelfModel()

        # 🔁 EVOLUTION
        self.evolution = FanusEvolutionController()

        # ⚡ EXECUTION (NEW IMPORTANT LAYER)
        self.executor = FanusExecutionLayer()

        # 🛠 SELF IMPROVEMENT
        self.self_improver = FanusSelfImprovement()

        # 💾 MEMORY
        self.memory = FanusMemoryLayer(max_size=max_memory)

        # ⚙️ CONFIG
        self.tick_delay = tick_delay

        # 🧠 STATE
        self.tick = 0
        self.running = False

    # =========================
    # 🔁 SINGLE CYCLE
    # =========================
    def cycle(self, intent="test"):

        # 1. ENGINE
        result = self.engine.run({"intent": intent})

        # 2. MEMORY STORE
        self.memory.store(result)

        # 3. OBSERVER
        observation = self.observer.observe(result)

        # 4. SELF MODEL
        self_model = self.self_model.update(observation, result)

        # 5. META MODEL
        meta = self.meta_model.analyze(self_model)

        # 6. EVOLUTION (proposals)
        evolution = self.evolution.evaluate(
            self.memory.snapshot(),
            meta
        )

        # 7. EXECUTION LAYER (apply safe changes + semantic embedding)
        execution = self.executor.execute(evolution)

        # 8. SELF IMPROVEMENT (evaluation layer)
        improvement = self.self_improver.evaluate(meta)

        # 9. OUTPUT
        self._print(result, observation, self_model, meta, evolution, execution, improvement)

        return {
            "result": result,
            "observation": observation,
            "self_model": self_model,
            "meta": meta,
            "evolution": evolution,
            "execution": execution,
            "improvement": improvement,
            "memory": self.memory.snapshot()
        }

    # =========================
    # 🧠 OUTPUT
    # =========================
    def _print(self, result, observation, self_model, meta, evolution, execution, improvement):

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

        print("\n⚙️ EVOLUTION:")
        print(evolution)

        print("\n⚡ EXECUTION:")
        print(execution)

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
