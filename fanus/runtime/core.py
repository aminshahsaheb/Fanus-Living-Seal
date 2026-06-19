import os
import time
import sys


class FanusRuntimeCore:

    def __init__(self, tick_rate=2, max_memory=50):

        # 🧠 AUTO FIX PATH (CRITICAL FIX)
        self.root = os.getcwd()
        sys.path.append(self.root)

        self.tick_rate = tick_rate
        self.running = False

        self.memory = []
        self.max_memory = max_memory

        self._safe_import_engine()

    # =========================
    # 📍 SAFE IMPORT (NO CRASH)
    # =========================
    def _safe_import_engine(self):

        try:
            from fanus.evolution.evolution_engine import EvolutionEngine
            self.engine = EvolutionEngine()

        except Exception as e:
            print("🛑 ENGINE IMPORT FAILED")
            print("Reason:", str(e))
            self.engine = None

    # =========================
    # 📍 INPUT LAYER
    # =========================
    def get_input(self):

        return {
            "intent": "test",
            "timestamp": time.time()
        }

    # =========================
    # 📍 MEMORY SYSTEM
    # =========================
    def store_memory(self, data):

        self.memory.append(data)

        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

    # =========================
    # 📍 CORE EXECUTION TICK
    # =========================
    def tick(self):

        if not self.engine:
            print("🛑 No Engine Loaded — skipping tick")
            return None

        event = self.get_input()

        result = self.engine.run(event)

        self.store_memory(result)

        print("\n🧠 FANUS RUNTIME TICK")
        print("---------------------")
        print("Intent:", result.get("intent"))
        print("Decision:", result.get("decision"))
        print("Memory Size:", len(self.memory))

        return result

    # =========================
    # 📍 MAIN LOOP
    # =========================
    def run(self, max_ticks=10):

        self.running = True

        print("\n🚀 FANUS RUNTIME CORE STARTED")
        print("-----------------------------")

        tick = 0

        while self.running and tick < max_ticks:

            self.tick()

            tick += 1
            time.sleep(self.tick_rate)

        print("\n🛑 FANUS RUNTIME STOPPED")

    # =========================
    # 📍 STOP
    # =========================
    def stop(self):
        self.running = False
