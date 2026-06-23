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
    # 🔁 MAIN RUN
    # =========================
    def run(self, steps=1):

        print("\n🚀 FANUS SIP-VALIDATED LOOP STARTED\n")

        # 1. SIP BOOT CHECK
        boot_status = self.sip.safe_boot(self._cycle)

        # 🔴 FIX: handle both dict and bool safely
        if isinstance(boot_status, bool):
            boot_status = {
                "status": "ok" if boot_status else "blocked",
                "raw": boot_status
            }

        if isinstance(boot_status, dict):
            if boot_status.get("status") == "blocked":
                print("🛑 SIP BLOCKED BOOT — SYSTEM NOT READY")
                return

        print("🚀 SIP OK — BOOTING FANUS SYSTEM")

        # 2. RUN LOOP
        for _ in range(steps):
            self._cycle()
            time.sleep(self.tick_delay)

    # =========================
    # 🔁 SINGLE CYCLE
    # =========================
    def _cycle(self):

        self.tick += 1

        state = {
            "tick": self.tick,
            "intent": "test",
            "decision": "ALLOW_WITH_CAUTION",
            "action": {"status": "safe_ok", "output": "test"},
            "state": {"stability": 0.99 ** self.tick}
        }

        print(f"[TICK {self.tick}] ", state)
        return state

    # =========================
    # 🛑 STOP
    # =========================
    def stop(self):
        self.running = False
