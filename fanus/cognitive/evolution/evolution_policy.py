"""
==========================================================
FANUS EVOLUTION POLICY
==========================================================

Deterministic Evolution Policy

Responsibilities
----------------

- Evaluate aggregated semantic signals
- Produce proposal description

This module NEVER:

- executes actions
- modifies identity
- modifies runtime
- creates events
- writes memory

==========================================================
"""

from fanus.cognitive.ontology.ontology_registry import (
    OntologyRegistry,
)


class EvolutionPolicy:
    """
    Pure policy engine.

    Input:

        Aggregated semantic signals

    Output:

        Proposal payload

    No side effects.
    """

    def __init__(self):

        self.registry = OntologyRegistry()

        self.proposal = self.registry.get(
            "proposal"
        )

        self.action = self.registry.get(
            "action"
        )

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    def evaluate(
        self,
        signals: dict
    ):

        combined = signals.get(
            "combined",
            0.0
        )

        trend = signals.get(
            "trend",
            0.0
        )

        stability = signals.get(
            "stability",
            1.0
        )

        # ---------------------------------------------
        # RULE 1
        # ---------------------------------------------

        if stability < 0.30:

            return {

                "type":
                    self.proposal["REPAIR"],

                "action":
                    self.action["REDUCE"],

                "reason":
                    "critical stability"
            }

        # ---------------------------------------------
        # RULE 2
        # ---------------------------------------------

        if combined < 0.40:

            return {

                "type":
                    self.proposal["REPAIR"],

                "action":
                    self.action["REDUCE"],

                "reason":
                    "weak semantic state"
            }

        # ---------------------------------------------
        # RULE 3
        # ---------------------------------------------

        if combined < 0.70:

            return {

                "type":
                    self.proposal["LEARNING"],

                "action":
                    self.action["LEARN"],

                "reason":
                    "controlled learning"
            }

        # ---------------------------------------------
        # RULE 4
        # ---------------------------------------------

        if trend > 0.20:

            return {

                "type":
                    self.proposal["BOOST"],

                "action":
                    self.action["EXPAND"],

                "reason":
                    "positive semantic trend"
            }

        # ---------------------------------------------
        # DEFAULT
        # ---------------------------------------------

        return {

            "type":
                self.proposal["BOOST"],

            "action":
                self.action["EXPAND"],

            "reason":
                "stable semantic system"
        }
