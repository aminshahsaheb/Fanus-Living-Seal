import time

from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel

from fanus.cognitive.evolution_controller import EvolutionController
from fanus.cognitive.collapse.collapse_controller import CollapseController

from fanus.runtime.decision.decision_engine import DecisionEngine
from fanus.cognitive.execution_layer import FanusExecutionLayer

from fanus.runtime.observer.runtime_observer import RuntimeObserver
from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine
from fanus.cognitive.autonomy_governor import FanusAutonomyGovernor


class FanusLoop:
    """
    ==========================================================
    FANUS RUNTIME LOOP (STABLE FINAL CORE)
    ==========================================================

    PIPELINE:

    Identity
        ↓
    Reflection
        ↓
    Evolution
        ↓
    Collapse
        ↓
    Self-Stabilization (GATE)
        ↓
    Decision
        ↓
    Execution (CONTROLLED)
        ↓
    Observer (FULL TRACE)

    ==========================================================
    """

    def __init__(self, tick_interval=0.2):

        # -------------------------
        # Runtime config
        # -------------------------
        self.tick_interval = tick_interval
        self.tick_index = 0
        self.running = False

        # -------------------------
        # Cognitive core
        # -------------------------
        self.identity = IdentityKernel()
        self.self_model = SelfModel()
        self.evolution = EvolutionController()
        self.collapse = CollapseController()

        # -------------------------
        # Reasoning layer
        # -------------------------
        self.decision_engine = DecisionEngine()
        self.execution = FanusExecutionLayer()

        # -------------------------
        # Control layer
        # -------------------------
        self.self_stabilizer = SelfStabilizationEngine()
        self.observer = RuntimeObserver()
        self.governor = FanusAutonomyGovernor()

    # ==================================================
    # MAIN LOOP
    # ==================================================

    def run(self, max_ticks=10):

        self.running = True
        # print("\n🚀 FANUS LOOP STARTED")

        while self.running and self.tick_index < max_ticks:
            self._tick()

        # print("\n🛑 FANUS LOOP STOPPED")

    # ==================================================
    # SINGLE TICK
    # ==================================================

    def _tick(self):

        # print(f"\n🧠 TICK {self.tick_index}")

        # 1. Identity evaluation
        identity_state = self.identity.evaluate()

        # 2. Reflection
        reflection_state = self.self_model.observe(identity_state)

        # 3. Evolution
        evolution_state = self.evolution.evaluate(
            identity_state=identity_state,
            reflection_state=reflection_state
        )

        # 4. Collapse analysis
        collapse_state = self.collapse.evaluate(
            identity_state=identity_state,
            evolution_state=evolution_state,
            reflection_state=reflection_state
        )

        # 5. STABILITY GATE (CRITICAL CONTROL POINT)
        stability_state = self.self_stabilizer.evaluate(
            collapse_state=collapse_state,
            evolution_state=evolution_state
        )

        # 🛑 HARD SAFETY CHECK
        if not stability_state.get("allowed", True):
            print("\n🛑 STABILITY GATE BLOCKED EXECUTION")
            time.sleep(stability_state.get("tick_delay", 0.5))
            self.tick_index += 1
            return

        # 6. Decision
        decision = self.decision_engine.evaluate(
            identity_state,
            evolution_state,
            collapse_state
        )

        # 7. Execution (CONTROLLED BY STABILITY GATE)
        execution_result = self.execution.execute({
            "decision": decision,
            "proposals": evolution_state.get("proposals", []),
            "execution_limit": stability_state.get("execution_limit", 1.0)
        })

        # 7.5 Autonomy governance
        governance = self.governor.evaluate(
            {"stability": identity_state.get("stability", 1.0), "drift": reflection_state.get("reflection", {}).get("drift", 0.0)},
            stability_state,
            collapse_state.get("meta", {})
        )
        if governance["locked"]:
            return

        # 8. Observer (FULL SYSTEM TRACE)
        self.observer.observe(
            tick_index=self.tick_index,
            identity=identity_state,
            reflection=reflection_state,
            evolution=evolution_state,
            collapse=collapse_state,
            decision=decision,
            execution=execution_result,
            stability=stability_state
        )

        # 9. Debug output
        # self._print_state(
            

        # 10. adaptive runtime control
        time.sleep(stability_state.get("tick_delay", self.tick_interval))
        self.tick_index += 1

    # ==================================================
    # DEBUG PRINTER
    # ==================================================

    def _print_state(
        self,
        identity,
        reflection,
        evolution,
        collapse,
        execution,
        stability
    ):

        print("\n🧬 IDENTITY")
        print(identity)

        print("\n🪞 REFLECTION")
        print(reflection)

        print("\n⚙️ EVOLUTION")
        print(evolution)

        print("\n🛡 COLLAPSE")
        print(collapse)

        print("\n🚦 STABILITY")
        print(stability)

        print("\n⚡ EXECUTION")
        print(execution)

    # ==================================================

    def stop(self):
        self.running = False
