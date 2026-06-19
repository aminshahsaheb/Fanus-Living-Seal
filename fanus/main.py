from fanus.evolution.evolution_engine import EvolutionEngine


class FanusSystem:

    def __init__(self):
        self.engine = EvolutionEngine()

    def run_once(self, intent="test"):
        return self.engine.run({"intent": intent})

    def run_loop(self, n=5):
        for i in range(n):
            result = self.run_once("test")
            print(f"[TICK {i}] ", result)


if __name__ == "__main__":
    system = FanusSystem()
    system.run_loop()
