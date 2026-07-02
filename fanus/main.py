from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.cognitive.self_model import SelfModel
from fanus.cognitive.collapse.collapse_controller import CollapseController
from fanus.evolution.evolution_engine import EvolutionEngine
from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine


class FanusSystem:

    def __init__(self):
        self.identity = IdentityKernel()
        self.self_model = SelfModel()
        self.collapse = CollapseController()
        self.stabilizer = SelfStabilizationEngine()
        self.engine = EvolutionEngine()

    def run_once(self, intent="test"):
        state = self.engine.run({"intent": intent})
        identity = self.identity.evaluate(state["state"])
        reflection = self.self_model.observe(identity)
        collapse = self.collapse.evaluate(identity, state["state"], reflection)
        stabilizer = self.stabilizer.evaluate(collapse, state)
        return {**state, "identity": identity, "reflection": reflection, "collapse": collapse, "stabilizer": stabilizer}

    def run_loop(self, n=5):
        for i in range(n):
            result = self.run_once("test")
            mode = result["identity"]["mode"]
            stab = round(result["state"]["stability"], 4)
            alert = result["collapse"]["meta"]["alert_level"]
            sys_mode = result["stabilizer"]["mode"]
            damping = result["stabilizer"]["damping_factor"]
            print(f"[TICK {i}]  mode={mode}  stability={stab}  alert={alert}  sys={sys_mode}  damping={damping}")


if __name__ == "__main__":
    system = FanusSystem()
    system.run_loop()