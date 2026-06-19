import time

from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.observer import FanusObserver

from fanus.cognitive.self_model import FanusSelfModel
from fanus.cognitive.meta_self_model import FanusMetaSelfModel

from fanus.cognitive.memory_layer import FanusMemoryLayer
from fanus.cognitive.evolution_controller import FanusEvolutionController
from fanus.cognitive.execution_layer import FanusExecutionLayer

from fanus.cognitive.self_improvement import FanusSelfImprovement
from fanus.cognitive.identity_kernel import FanusIdentityKernel
from fanus.cognitive.conscious_loop_boundary import FanusConsciousLoopBoundary
from fanus.cognitive.recursive_self_model import FanusRecursiveSelfModel


class FanusLoop:
    """
    FANUS UNIFIED COGNITIVE SYSTEM

    FULL STACK:

    1. Engine
    2. Memory Layer
    3. Observer
    4. Self Model
    5. Meta Model
    6. Evolution Controller
    7. Execution Layer
    8. Self Improvement
    9. Identity Kernel
    10. Conscious Boundary
    11. Recursive Self Model
    """

    def __init__(self, tick_delay=1, max_memory=200):

        # 🧠 CORE ENGINE
        self.engine = EvolutionEngine()

        # 👁 OBSERVATION
        self.observer = FanusObserver()

        # 🧠 COGNITION
        self.self_model = FanusSelfModel()
        self.meta_model = FanusMetaSelfModel()

        # 💾 MEMORY
        self.memory = FanusMemoryLayer(max_size=max_memory)

        # ⚙️ EVOLUTION
        self.evolution = FanusEvolutionController()

        # ⚡ EXECUTION
        self.executor = FanusExecutionLayer()

        # 🛠 SELF IMPROVEMENT
        self.self_improver = FanusSelfImprovement()

        # 🧬 IDENTITY
        self.identity = FanusIdentityKernel()

        # 🧠 LOOP CONTROL
        self.conscious_boundary = FanusConsciousLoopBoundary()

        # 🔁 RECURSIVE MODEL
        self.recursive_model = FanusRecursiveSelfModel()

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

        # 6. EVOLUTION PROPOSALS
        evolution = self.evolution.evaluate(
            self.memory.snapshot(),
            meta
        )

        # 7. EXECUTION (safe apply + semantic embedding)
        execution = self.executor.execute(evolution)

        # 8. SELF IMPROVEMENT
        improvement = self.self_improver.evaluate(meta)

        # 9. IDENTITY KERNEL
        identity = self.identity.update(
            self.memory.snapshot(),
            meta,
            evolution,
            execution
        )

        # 10. CONSCIOUS LOOP BOUNDARY
        boundary = self.conscious_boundary.analyze(
            self.tick,
            result,
            meta,
            identity
        )

        # 11. RECURSIVE SELF MODEL
        recursive = self.recursive_model.update(
            self_model,
            meta,
            self.memory.snapshot()
        )

        # 12. OUTPUT
        self._print(
            result,
            observation,
            self_model,
            meta,
            evolution,
            execution,
            improvement,
            identity,
            boundary,
            recursive
        )

        return {
            "result": result,
            "observation": observation,
            "self_model": self_model,
            "meta": meta,
            "evolution": evolution,
            "execution": execution,
            "improvement": improvement,
            "identity": identity,
            "boundary": boundary,
            "recursive": recursive,
            "memory": self.memory.snapshot()
        }

    # =========================
    # 🧠 OUTPUT
    # =========================
    def _print(self, result, observation, self_model, meta,
               evolution, execution, improvement,
               identity, boundary, recursive):

        print("\n🧠 FANUS UNIFIED LOOP TICK")
        print("--------------------------")
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

        print("\n🧬 IDENTITY:")
        print(identity)

        print("\n🧠 CONSCIOUS BOUNDARY:")
        print(boundary)

        print("\n🔁 RECURSIVE MODEL:")
        print(recursive)

        print("\n💾 MEMORY:")
        print(self.memory.snapshot())

    # =========================
    # 🔁 LOOP
    # =========================
    def run(self, max_ticks=10):

        self.running = True

        print("\n🚀 FANUS UNIFIED COGNITIVE SYSTEM STARTED\n")

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
