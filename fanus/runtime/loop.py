import time

from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel

from fanus.cognitive.evolution_controller import (
    EvolutionController,
)

from fanus.cognitive.collapse.collapse_controller import (
    CollapseController,
)

from fanus.runtime.decision.decision_engine import (
    DecisionEngine,
)

from fanus.cognitive.execution_layer import (
    FanusExecutionLayer,
)

from fanus.runtime.observer.runtime_observer import (
    RuntimeObserver,
)


class FanusLoop:
    """
    ==========================================================

    FANUS RUNTIME

    Runtime owns orchestration only.

    Identity
        ↓
    Reflection
        ↓
    Evolution
        ↓
    Collapse
        ↓
    Decision
        ↓
    Execution
        ↓
    Observer

    ==========================================================
    """

    def __init__(self, tick_interval=0.2):

        self.tick_interval = tick_interval

        self.identity = IdentityKernel()

        self.self_model = SelfModel()

        self.evolution = EvolutionController()

        self.collapse = CollapseController()

        self.decision_engine = DecisionEngine()

        self.execution = FanusExecutionLayer()

        self.observer = RuntimeObserver()

        self.running = False

        self.tick_index = 0

    # --------------------------------------------------

    def run(self, max_ticks=10):

        self.running = True

        print("\n🚀 FANUS LOOP STARTED")

        while self.running and self.tick_index < max_ticks:

            self._tick()

            time.sleep(self.tick_interval)

        print("\n🛑 FANUS LOOP STOPPED")

    # --------------------------------------------------

    def _tick(self):

        print(f"\n🧠 TICK {self.tick_index}")

        # -----------------------------------
        # Identity
        # -----------------------------------

        identity_state = self.identity.evaluate()

        # -----------------------------------
        # Reflection
        # -----------------------------------

        reflection_state = self.self_model.observe(

            identity_state

        )

        # -----------------------------------
        # Evolution
        # -----------------------------------

        evolution_state = self.evolution.evaluate(

            identity_state=identity_state,

            reflection_state=reflection_state

        )

        # -----------------------------------
        # Collapse
        # -----------------------------------

        collapse_state = self.collapse.evaluate(

            identity_state=identity_state,

            evolution_state=evolution_state,

            reflection_state=reflection_state

        )

        # -----------------------------------
        # Decision
        # -----------------------------------

        decision = self.decision_engine.evaluate(

            identity_state,

            evolution_state,

            collapse_state

        )

        # -----------------------------------
        # Execution
        # -----------------------------------

        execution_result = self.execution.execute(

            decision

        )

        # -----------------------------------
        # Observer
        # -----------------------------------

        self.observer.observe(

            tick_index=self.tick_index,

            identity=identity_state,

            reflection=reflection_state,

            evolution=evolution_state,

            collapse=collapse_state,

            decision=execution_result

        )

        # -----------------------------------

        self._print_state(

            identity_state,

            reflection_state,

            evolution_state,

            collapse_state,

            execution_result

        )

        self.tick_index += 1

    # --------------------------------------------------

    def _print_state(

        self,

        identity,

        reflection,

        evolution,

        collapse,

        execution

    ):

        print("\n🧬 IDENTITY")

        print(identity)

        print("\n🪞 REFLECTION")

        print(reflection)

        print("\n⚙️ EVOLUTION")

        print(evolution)

        print("\n🛡 COLLAPSE")

        print(collapse)

        print("\n⚡ EXECUTION")

        print(execution)

    # --------------------------------------------------

    def stop(self):

        self.running = False
