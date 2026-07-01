from fanus.cognitive.evolution.signal_aggregator import SignalAggregator
from fanus.cognitive.evolution.evolution_policy import EvolutionPolicy
from fanus.cognitive.evolution.proposal_builder import ProposalBuilder
from fanus.cognitive.evolution.proposal_rewriter import ProposalRewriter


class EvolutionController:
    """
    ==========================================================
    FANUS EVOLUTION CONTROLLER (STEP 22 FINAL)
    ==========================================================

    Pipeline:
    Identity → Reflection → Signals → Memory Pressure
           → Policy → Proposal → Rewrite Layer

    No execution. No authority.
    Only adaptive proposal generation.
    ==========================================================
    """

    def __init__(self):

        self.aggregator = SignalAggregator()
        self.policy = EvolutionPolicy()
        self.rewriter = ProposalRewriter()

    # ==================================================

    def evaluate(
        self,
        identity_state,
        reflection_state,
        semantic_memory=None,
        memory_pressure=0.0,
        collapse_state=None
    ):

        # ------------------------------------------
        # 1. Signal aggregation
        # ------------------------------------------
        signals = self.aggregator.aggregate(
            identity_state=identity_state,
            reflection_state=reflection_state,
            semantic_memory=semantic_memory
        )

        # ------------------------------------------
        # 2. Inject memory pressure
        # ------------------------------------------
        signals["memory_pressure"] = memory_pressure
        signals["combined"] = signals.get("combined", 0) + memory_pressure * 0.4

        # ------------------------------------------
        # 3. Base policy decision
        # ------------------------------------------
        proposal = self.policy.evaluate(signals)

        base_event = ProposalBuilder.build(
            proposal,
            source="evolution"
        )

        proposals = [base_event]

        # ------------------------------------------
        # 4. Collapse-aware rewriting layer
        # ------------------------------------------
        if collapse_state is not None:

            proposals = self.rewriter.rewrite(
                proposals,
                memory_pressure,
                collapse_state
            )

        # ------------------------------------------
        # 5. Output
        # ------------------------------------------
        return {
            "signals": signals,
            "proposals": proposals,
            "meta": {
                "stability": signals.get("stability"),
                "reflection": signals.get("reflection"),
                "memory_signal": signals.get("memory"),
                "trend": signals.get("trend"),
                "combined": signals.get("combined"),
                "memory_pressure": memory_pressure,
                "rewritten": True
            }
        }
