import time

from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.observer import FanusObserver

from fanus.cognitive.memory_layer import FanusMemoryLayer
from fanus.cognitive.memory_consolidation_engine import FanusMemoryConsolidationEngine

from fanus.cognitive.cognitive_state import FanusCognitiveState
from fanus.cognitive.unified_identity_field import FanusUnifiedIdentityField

from fanus.cognitive.evolution_controller import FanusEvolutionController
from fanus.cognitive.execution_layer import FanusExecutionLayer

from fanus.cognitive.identity_driven_core import FanusIdentityDrivenCore
from fanus.cognitive.self_learning_loop import FanusSelfLearningLoop
from fanus.cognitive.identity_autonomy_core import FanusIdentityAutonomyCore
from fanus.cognitive.collapse_resistance_core import FanusCollapseResistanceCore

from fanus.core.system_integration_protocol import FanusSystemIntegrationProtocol

from fanus.cognitive.system_collapse_stabilizer import FanusSystemCollapseStabilizer
from fanus.cognitive.autonomy_governor import FanusAutonomyGovernor


class FanusLoop:

    def __init__(self, tick_delay=1, max_memory=200):

        # core systems
        self.engine = EvolutionEngine()
        self.observer = FanusObserver()

        # memory
        self.memory = FanusMemoryLayer(max_size=max_memory)
        self.memory_consolidator = FanusMemoryConsolidationEngine()

        # cognitive
        self.cognitive = FanusCognitiveState()
        self.identity_field = FanusUnifiedIdentityField()

        # evolution + execution
        self.evolution = FanusEvolutionController()
        self.executor = FanusExecutionLayer()

        # intelligence layers
        self.identity_core = FanusIdentityDrivenCore()
        self.self_learning = FanusSelfLearningLoop()

        # control systems
        self.autonomy_core = FanusIdentityAutonomyCore()
        self.collapse_core = FanusCollapseResistanceCore()

        self.governor = FanusAutonomyGovernor()
        self.stabilizer = FanusSystemCollapseStabilizer()

        # SIP
        self.sip = FanusSystemIntegrationProtocol()

        self.tick_delay = tick_delay
        self.tick = 0
        self.running = False

    # =========================
    # 🔁 SINGLE CYCLE
    # =========================
    def cycle(self):

        self.tick += 1

        # 1. SIP validation
        boot_status = self.sip.validate_runtime()

        if not boot_status["runtime_ready"]:
            print("\n🛑 SIP BLOCKED BOOT — SYSTEM NOT READY\n")
            print("📦 IMPORT STATUS:", boot_status["imports"])
            print("🧬 GIT STATUS:", boot_status["git"])
            return None

        # 2. base state
        state = {
            "tick": self.tick,
            "intent": "test"
        }

        # 3. MEMORY WRITE (fix #1)
        self.memory.store(state)

        # 4. identity processing
        identity_state = self.identity_field.evolve(state)

        # 🔥 IDENTITY INFLUENCE LAYER (safe version)
        identity_weight = identity_state.get("confidence", 1.0)

        state["identity_weight"] = identity_weight
        state["weighted_intent"] = state["intent"]

        # 5. evolution
        evolved_state = self.evolution.step(identity_state)

        # 6. execution
        output = self.executor.execute(evolved_state)

        # 7. observation
        observation = self.observer.observe(output)

        # 8. memory consolidation
        self.memory_consolidator.consolidate(self.memory)

        # 9. stability enforcement
        self.stabilizer.stabilize(state)

        # 10. feedback loop (IMPORTANT)
        self.memory.store({
            "tick": self.tick,
            "state": state,
            "identity": identity_state,
            "output": output
        })

        return {
            "tick": self.tick,
            "state": state,
            "identity": identity_state,
            "output": output,
            "observation": observation
        }

    # =========================
    # 🚀 RUN LOOP
    # =========================
    def run(self, steps=5):

        print("\n🚀 FANUS SIP-VALIDATED LOOP STARTED\n")

        for _ in range(steps):
            result = self.cycle()

            if result:
                print(f"[TICK {result['tick']}] ", result)

            time.sleep(self.tick_delay)

        print("\n✅ FANUS LOOP FINISHED\n")

    # =========================
    # STOP
    # =========================
    def stop(self):
        self.running = False
