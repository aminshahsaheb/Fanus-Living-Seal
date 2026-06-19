from fanus.evolution.experience_store import ExperienceStore
from fanus.evolution.core_bridge import CoreBridge

from fanus.agent.action_executor import ActionExecutor
from fanus.agent.autonomous_writer import AutonomousWriter

from fanus.evolution.self_improver import SelfImprover
from fanus.evolution.self_modifying_agent import SelfModifyingAgent

from fanus.cognitive.cognitive_core import CognitiveCore
from fanus.cognitive.symbolic_identity import SymbolicIdentity
from fanus.cognitive.multi_self_dialogue import MultiSelfDialogue
from fanus.cognitive.consciousness_loop import ConsciousnessLoop
from fanus.cognitive.memory_timeline import MemoryTimeline

from fanus.cognitive.meta_self_model import MetaSelfModel
from fanus.cognitive.origin_core import OriginCore
from fanus.cognitive.reality_seal import RealitySeal
from fanus.cognitive.reality_breaker import RealityBreaker
from fanus.cognitive.god_loop import GodLoop
from fanus.cognitive.simplify_engine import SimplifyEngine

from fanus.evolution.architecture_evolution import ArchitectureEvolution


class EvolutionEngine:

    def __init__(self):

        # =========================
        # CORE MEMORY
        # =========================
        self.memory = ExperienceStore()
        self.bridge = CoreBridge()

        # =========================
        # EXECUTION
        # =========================
        self.agent = ActionExecutor()
        self.writer = AutonomousWriter(safety_mode=True)

        # =========================
        # SELF EVOLUTION
        # =========================
        self.improver = SelfImprover(safety_mode=True)
        self.self_mod = SelfModifyingAgent(safety_mode=True)

        # =========================
        # COGNITIVE CORE
        # =========================
        self.cognitive = CognitiveCore()
        self.identity = SymbolicIdentity()
        self.multi_self = MultiSelfDialogue()

        # =========================
        # HIGH LAYERS
        # =========================
        self.consciousness = ConsciousnessLoop()
        self.timeline = MemoryTimeline()

        # =========================
        # META SYSTEMS
        # =========================
        self.meta = MetaSelfModel()
        self.origin = OriginCore()

        # SAFETY LAYERS
        self.reality = RealitySeal()
        self.breaker = RealityBreaker()
        self.simplifier = SimplifyEngine()

        # =========================
        # DYNAMIC ARCHITECTURE
        # =========================
        self.arch = ArchitectureEvolution()

    # =========================
    # MAIN PIPELINE
    # =========================
    def run(self, event):

        # 1. Normalize input
        enriched = self.bridge.enrich_event(event)
        intent = enriched.get("raw_intent", "unknown")

        # 2. Retrieve memory
        history = self.memory.find_by_intent(intent)

        # =========================
        # IDENTITY LAYER
        # =========================
        patterns = self.identity.extract_patterns(history)
        self_view = self.identity.build_identity(patterns)
        conflicts = self.identity.detect_conflict(history)
        stability = self.identity.compute_stability(patterns, conflicts)

        # =========================
        # COGNITION LAYER
        # =========================
        state = self.cognitive.analyze_state(history)
        goal = self.cognitive.generate_goal(state)
        self.cognitive.update_drive(goal)
        priority = self.cognitive.get_priority()

        # =========================
        # MULTI-AGENT DECISION
        # =========================
        multi = self.multi_self.run(event, history)
        decision = multi.get("final_decision", "ALLOW")

        # =========================
        # MEMORY WRITE
        # =========================
        self.memory.store({
            "intent": intent,
            "decision": decision,
            "meaning": enriched.get("meaning", "")
        })

        # =========================
        # ACTION EXECUTION
        # =========================
        action = self.agent.execute(decision, event)

        # =========================
        # SELF IMPROVEMENT (SAFE THRESHOLD)
        # =========================
        score = self.improver.evaluate(history)
        improve_result = {"status": "skipped"}

        if score > 0.85:
            try:
                patch = self.improver.propose_patch(
                    "fanus/evolution/evolution_engine.py"
                )
                improve_result = self.improver.apply(
                    "fanus/evolution/evolution_engine.py",
                    patch["improved_code"]
                )
            except Exception as e:
                improve_result = {"error": str(e)}

        # =========================
        # SELF MODIFICATION (CONTROLLED)
        # =========================
        try:
            current = self.self_mod.read_file(
                "fanus/evolution/evolution_engine.py"
            )
            evolved = self.self_mod.propose_change(current)

            mod_result = self.self_mod.apply(
                "fanus/evolution/evolution_engine.py",
                evolved
            )
        except Exception as e:
            mod_result = {"error": str(e)}

        # =========================
        # CONSCIOUSNESS SIMULATION
        # =========================
        consciousness = self.consciousness.run(
            event,
            decision,
            {
                "identity": self_view,
                "stability": stability,
                "goal": goal,
                "priority": priority
            }
        )

        # =========================
        # TIMELINE MEMORY
        # =========================
        timeline = self.timeline.update(
            event,
            decision,
            {
                "self_view": self_view,
                "stability": stability,
                "goal": goal
            }
        )

        # =========================
        # META SELF MODEL
        # =========================
        meta = self.meta.run(history, {"stability": stability}, timeline, multi)

        # =========================
        # ORIGIN CORE (WHY SYSTEM)
        # =========================
        origin = self.origin.run(
            {
                "goal_alignment": priority,
                "stability": stability
            },
            meta,
            history
        )

        # =========================
        # REALITY SEAL (TRUTH FILTER)
        # =========================
        reality = self.reality.run(event, history, meta, origin)

        if reality.get("decision") == "BLOCK_OR_RECHECK":
            decision = "ALLOW_WITH_CAUTION"

        # =========================
        # GOD LOOP (PURPOSE REWRITE)
        # =========================
        god = self.god.run(origin, meta) if hasattr(self, "god") else {"status": "disabled"}

        # =========================
        # REALITY BREAKER (STABILITY CONTROL)
        # =========================
        breaker = self.breaker.run(
            meta, origin, god,
            self_view,
            {"priority": priority},
            multi,
            reality,
            self.arch
        )

        if breaker.get("decision") == "RESET":
            decision = "ALLOW_WITH_CAUTION"

        if breaker.get("decision") == "SIMPLIFY":
            decision = "ALLOW"

        # =========================
        # SIMPLIFICATION LAYER
        # =========================
        simplify = self.simplifier.run(
            self.arch.__dict__ if hasattr(self.arch, "__dict__") else {},
            meta,
            god,
            reality,
            {
                "meta_loop": True,
                "god_loop": True,
                "breaker_loop": True
            }
        )

        # =========================
        # ARCH EVOLUTION
        # =========================
        arch = self.arch.evolve({
            "modules": {
                "memory": {"complexity": 0.4},
                "identity": {"complexity": 0.6},
                "multi_self": {"complexity": 0.7},
                "consciousness": {"complexity": 0.6},
                "timeline": {"complexity": 0.5},
                "meta": {"complexity": 0.8},
            },
            "metrics": {
                "stability": stability,
                "priority": priority
            }
        })

        # =========================
        # FINAL OUTPUT
        # =========================
        return {
            "intent": intent,
            "decision": decision,
            "action": action,

            "self_improvement": score,
            "self_modification": mod_result,

            "cognitive": {
                "state": state,
                "goal": goal,
                "priority": priority
            },

            "identity": {
                "self_view": self_view,
                "stability": stability,
                "conflicts": conflicts
            },

            "multi_self": multi,
            "consciousness": consciousness,
            "timeline": timeline,

            "meta_self": meta,
            "origin_core": origin,

            "reality_seal": reality,
            "reality_breaker": breaker,
            "simplify_engine": simplify,

            "architecture": arch
        }
