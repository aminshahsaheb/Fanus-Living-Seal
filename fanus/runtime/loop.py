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

        self.engine = EvolutionEngine()
        self.observer = FanusObserver()

        self.memory = FanusMemoryLayer(max_size=max_memory)
        self.memory_consolidator = FanusMemoryConsolidationEngine()

        self.cognitive = FanusCognitiveState()
        self.identity_field = FanusUnifiedIdentityField()

        self.evolution = FanusEvolutionController()
        self.executor = FanusExecutionLayer()

        self.identity_core = FanusIdentityDrivenCore()
        self.self_learning = FanusSelfLearningLoop()

        self.autonomy_core = FanusIdentityAutonomyCore()
        self.collapse_core = FanusCollapseResistanceCore()

        self.governor = FanusAutonomyGovernor()
        self.stabilizer = FanusSystemCollapseStabilizer()

        self.sip = FanusSystemIntegrationProtocol()

        self.tick_delay = tick_delay
        self.tick = 0
        self.running = False

    # =========================
    # 🔁 CYCLE
    # =========================
    def cycle(self):

        self.tick += 1

        # 1. SIP check
        boot = self.sip.validate_runtime()

        if not boot["runtime_ready"]:
            print("\n🛑 SIP BLOCKED BOOT — SYSTEM NOT READY\n")
            print("📦 IMPORT:", boot["imports"])
            print("🧬 GIT:", boot["git"])
            return None

        # 2. STATE
        state = {
            "tick": self.tick,
            "intent": "test"
        }

        # 3. MEMORY INPUT (history)
        history = self.memory.recent() if hasattr(self.memory, "recent") else []
        state["memory_context"] = history

        self.memory.store(state)

        # 4. IDENTITY
        identity_state = self.identity_field.evolve(state)
        weight = identity_state.get("confidence", 1.0)

        state["identity_weight"] = weight

        # 5. EVOLUTION (identity + memory aware)
        evolved_state = self.evolution.step({
            "state": state,
            "identity": identity_state,
            "memory": history
        })

        # 6. EXECUTION
        output = self.executor.execute(evolved_state)

        # 7. OBSERVATION
        observation = self.observer.observe(output)

        # 8. CONSOLIDATION
        self.memory_consolidator.consolidate(self.memory)

        # 9. STABILIZATION
        self.stabilizer.stabilize(state)

        # 10. FEEDBACK LOOP
        self.memory.store({
            "tick": self.tick,
            "state": state,
            "identity": identity_state,
            "output": output,
            "observation": observation
        })

        return {
            "tick": self.tick,
            "state": state,
            "identity": identity_state,
            "output": output,
            "observation": observation
        }

    # =========================
    # 🚀 RUN
    # =========================
    def run(self, steps=5):

        print("\n🚀 FANUS LOOP STARTED\n")

        for _ in range(steps):
            result = self.cycle()

            if result:
                print(f"[TICK {result['tick']}]", result)

            time.sleep(self.tick_delay)

        print("\n✅ FANUS LOOP FINISHED\n")

    def stop(self):
        self.running = False
