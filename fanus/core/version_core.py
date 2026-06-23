import os
import hashlib
import json
import time


class FanusVersionCore:

    def __init__(self, version="1.0.0"):

        self.version = version
        self.lock_file = "FANUS_LOCK.json"

        self.core_paths = [
            "fanus/runtime",
            "fanus/cognitive",
            "fanus/evolution",
            "fanus/core",
            "fanus/tools"
        ]

    # =========================
    # 🔐 HASH SYSTEM
    # =========================
    def hash_file(self, path):

        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None

    # =========================
    # 📦 SNAPSHOT
    # =========================
    def build_snapshot(self):

        snapshot = {}

        for base in self.core_paths:

            for root, _, files in os.walk(base):

                for file in files:

                    if file.endswith(".py"):

                        full_path = os.path.join(root, file)
                        snapshot[full_path] = self.hash_file(full_path)

        return snapshot

    # =========================
    # 🔒 CREATE LOCK
    # =========================
    def create_lock(self):

        snapshot = self.build_snapshot()

        lock_data = {
            "version": self.version,
            "timestamp": time.time(),
            "snapshot": snapshot
        }

        with open(self.lock_file, "w") as f:
            json.dump(lock_data, f, indent=2)

        print("🔒 FANUS SYSTEM LOCKED")

        return lock_data

    # =========================
    # 🔍 VERIFY INTEGRITY
    # =========================
    def verify(self):

        if not os.path.exists(self.lock_file):
            return {"status": "no_lock"}

        with open(self.lock_file, "r") as f:
            lock_data = json.load(f)

        current = self.build_snapshot()

        drift = []

        for path, old_hash in lock_data["snapshot"].items():

            if path not in current:
                drift.append({"missing": path})

            elif current[path] != old_hash:
                drift.append({"modified": path})

        return {
            "status": "verified",
            "drift": drift,
            "clean": len(drift) == 0
        }

    # =========================
    # 🚀 BOOT CHECK
    # =========================
    def boot_check(self):

        result = self.verify()

        if result["status"] == "no_lock":
            print("🟡 NO SYSTEM LOCK FOUND")
            return {"status": "unlocked"}

        if not result["clean"]:
            print("🛑 SYSTEM DRIFT DETECTED")
            print(result["drift"])
            return {"status": "blocked", "drift": result["drift"]}

        print("✅ SYSTEM LOCK VALID")
        return {"status": "ok"}
