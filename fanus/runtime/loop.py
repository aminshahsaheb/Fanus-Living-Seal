import time

from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.observer import FanusObserver
from fanus.cognitive.self_model import FanusSelfModel
from fanus.cognitive.meta_self_model import FanusMetaSelfModel
from fanus.cognitive.self_improvement import FanusSelfImprovement
from fanus.cognitive.memory_layer import FanusMemoryLayer
from fanus.cognitive.evolution_controller import FanusEvolutionController
from fanus.cognitive.execution_layer import FanusExecutionLayer
from fanus.cognitive.identity_kernel import FanusIdentityKernel
from fanus.cognitive.conscious_loop_boundary import FanusConsciousLoopBoundary
from fanus.cognitive.recursive_self_model import FanusRecursiveSelfModel
from fanus.cognitive.unified_identity_field import FanusUnifiedIdentityField
from fanus.cognitive.system_collapse_stabilizer import FanusSystemCollapseStabilizer
from fanus.cognitive.autonomy_governor import FanusAutonomyGovernor

from fanus.runtime.system_integration import FanusSystemIntegration


class FanusLoop:

    def __init__(self, tick_delay=1, max_memory=200):

        # =========================
        # 🧠 CORE INITIALIZATION
        # =========================
        self.tick = 0
        self.running = False
        self.tick_delay = tick_delay

        # =========================
        # ENGINE
        # =========================
        self.engine = EvolutionEngine()

        # =========================
        # MEMORY
        # =========================
        self.memory = FanusMemoryLayer(max_size=max_memory)

        # =========================
        # OBSERVER
        # =========================
        self.observer = FanusObserver()

        # =========================
        # SELF MODELS
        # =========================
        self.self_model = FanusSelfModel()
        self.meta_model = FanusMetaSelfModel()
        self.identity = FanusIdentityKernel()
        self.recursive_model = FanusRecursiveSelfModel()

        # =========================
        # EVOLUTION + EXECUTION
        # =========================
        self.evolution = FanusEvolutionController()
        self.executor = FanusExecutionLayer()
        self.self_improver = FanusSelfImprovement()

        # =========================
        # STABILITY SYSTEMS
        # =========================
        self.boundary = FanusConsciousLoopBoundary()
        self.unified_field = FanusUnifiedIdentityField()
        self.stabilizer = FanusSystemCollapseStabilizer()
        self.governor = FanusAutonomyGovernor()

        # =========================
        # SYSTEM INTEGRATION (LAST)
        # =========================
        self.system = FanusSystemIntegration(self)

        # 🧪 bootstrap AFTER full init
        bootstrap_result = self.system.bootstrap()

        print("\n⚙️ SYSTEM BOOTSTRAP:")
        print(bootstrap_result)

    # =========================
    # 🔁 CYCLE
    # =========================
    def cycle(self, intent="test"):

        result = self.engine.run({"intent": intent})

        self.memory.store(result)

        observation = self.observer.observe(result)

        self_model = self.self_model.update(observation, result)

        meta = self.meta_model.analyze(self_model)

        evolution = self.evolution.evaluate(
            self.memory.snapshot(),
            meta
        )

        execution = self.executor.execute(evolution)

        identity = self.identity.update(
            self.memory.snapshot(),
            meta,
            evolution,
            execution
        )

        recursive = self.recursive_model.update(
            self_model,
            meta,
            self.memory.snapshot()
        )

        unified = self.unified_field.update(
            self.memory.snapshot(),
            meta,
            evolution,
            execution,
            recursive,
            {},
            identity
        )

        boundary = self.boundary.analyze(
            self.tick,
            result,
            meta,
            identity
        )

        collapse = self.stabilizer.analyze(
            unified,
            boundary,
            recursive
        )

        governance = self.governor.evaluate(
            unified,
            unified,
            collapse
        )

        # 🛑 SAFE STOP CONDITIONS
        if governance["locked"]:
            print("🔐 SYSTEM LOCKED — STOPPING CYCLE")
            return

        self.self_improver.evaluate(meta)

        self._print(result, meta, evolution, execution, identity, unified, collapse, governance)

    # =========================
    # 🧠 PRINT
    # =========================
    def _print(self, result, meta, evolution, execution, identity, unified, collapse, governance):

        print("\n🧠 TICK:", self.tick)
        print("Result:", result.get("decision"))

        print("\n🧠 META:", meta)
        print("\n⚙️ EVOLUTION:", evolution)
        print("\n⚡ EXECUTION:", execution)
        print("\n🧬 IDENTITY:", identity)
        print("\n🌐 UNIFIED:", unified)
        print("\n🛡 COLLAPSE:", collapse)
        print("\n⚖️ GOVERNANCE:", governance)

    # =========================
    # 🔁 RUN LOOP
    # =========================
    def run(self, max_ticks=10):

        self.running = True

        print("\n🚀 FANUS LOOP STARTED\n")

        while self.running and self.tick < max_ticks:

            self.cycle("test")

            self.tick += 1
            time.sleep(self.tick_delay)

        print("\n🛑 FANUS LOOP STOPPED")
