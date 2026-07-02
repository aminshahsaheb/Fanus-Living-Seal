from fanus.cognitive.identity_kernel import IdentityKernel
from fanus.evolution.evolution_engine import EvolutionEngine


class FanusSystem:

    def __init__(self):
        self.identity = IdentityKernel()
        self.engine = EvolutionEngine()

    def run_once(self, intent="test"):
        state = self.engine.run({"intent": intent})
        identity = self.identity.evaluate(state["state"])
        return {**state, "identity": identity}

    def run_loop(self, n=5):
        for i in range(n):
            result = self.run_once("test")
            print(f"[TICK {i}]  mode={result['identity']['mode']}  stability={round(result['state']['stability'], 4)}")


if __name__ == "__main__":
    system = FanusSystem()
    system.run_loop()
